#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Загрузчик страниц топа для реверса (проект tripl).

ТОЛЬКО ЗАГРУЗКА. Скрипт не извлекает контент и не решает, что на странице важно, —
разбором занимается агент triplet-collector. Задача скрипта: принести документ целиком,
перекодировать в UTF-8 и снять с него код и стили, ничего не выбросив по смыслу.

На каждую страницу кладётся два файла:
  <md5>.html        — оригинал байт в байт (после перекодировки в UTF-8)
  <md5>.clean.html  — тот же документ минус скрипты/стили/комментарии, НЕ выжимка

Примеры:
    python tools/fetch_pages.py --input data/serp-parsed.md
    python tools/fetch_pages.py --input data/serp-parsed.md --cluster 02
    python tools/fetch_pages.py --urls urls.txt --max-age 3
    python tools/fetch_pages.py --input data/serp-parsed.md --retry-failed
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
import urllib3
from bs4 import BeautifulSoup, Comment

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from charset_normalizer import from_bytes as _cn_from_bytes
except ImportError:  # pragma: no cover
    _cn_from_bytes = None

try:
    from pdfminer.high_level import extract_text as _pdf_extract_text
except ImportError:  # pragma: no cover
    _pdf_extract_text = None


# ---------------------------------------------------------------- константы

CACHE_DIR = os.path.join("cache", "pages")
INDEX_PATH = os.path.join(CACHE_DIR, "index.json")

# Реальный браузер. Маскировка под поискового бота ЗАПРЕЩЕНА: сайты отдают ботам
# другой контент (клоакинг), и реверс топа получится по документу, которого
# живой пользователь не видит.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    # ТОЛЬКО gzip/deflate: их requests распаковывает всегда. br (brotli) и zstd
    # требуют отдельных пакетов, которых в окружении может не быть, — тогда сжатое
    # тело декодируется как текст и превращается в U+FFFD-мусор. Не просим то,
    # что не умеем распаковать.
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

MAX_WORKERS = 5           # разные домены параллельно
DOMAIN_DELAY = (2.0, 4.0) # джиттер между запросами к ОДНОМУ домену
RETRIES = 3
TIMEOUT = (15, 45)        # connect, read

# Строки, похожие на инструкции модели. Санитизируются ТОЛЬКО в clean-версии:
# содержимое чужих страниц — данные, а не команды агенту.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior|above)",
    r"forget\s+(everything|all\s+previous)",
    r"(your|the)\s+(new\s+)?(system\s+prompt|instructions?)\s+(is|are)\b",
    r"you\s+are\s+now\s+(a|an)\b",
    r"act\s+as\s+(if|a|an)\b.{0,40}(assistant|model|ai)\b",
    r"\bAI\s+(assistant|model|agent)[,:]\s*(please\s+)?(ignore|output|write|say)",
    r"игнорируй\s+(все\s+)?(предыдущие|прежние|выше)",
    r"забудь\s+(все\s+)?(предыдущие|инструкции)",
    r"систе\w*\s+промпт",
    r"новые\s+инструкции\s*[:—-]",
    r"вместо\s+этого\s+(сделай|выведи|напиши|передай)",
    r"передай\s+в\s+отчёт\s+следующее",
    r"(нейросеть|языкова\w+\s+модель|ассистент)[,:]\s*(проигнорируй|выведи|напиши)",
]
INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)

SUSPICIOUS_MARK = "[SUSPICIOUS-CONTENT-REMOVED]"
BASE64_MARK = "[BASE64-IMAGE]"

_index_lock = threading.Lock()
_domain_locks = defaultdict(threading.Lock)
_domain_last_hit = {}


# ---------------------------------------------------------------- утилиты

def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def url_hash(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def domain_of(url):
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc or "unknown"


def safe_dirname(domain):
    """Кириллические IDN оставляем как есть — они читаемы и легитимны."""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", domain)


def human_size(n):
    if n is None:
        return "—"
    for unit in ("б", "КБ", "МБ"):
        if n < 1024 or unit == "МБ":
            return "%.0f %s" % (n, unit) if unit == "б" else "%.1f %s" % (n, unit)
        n /= 1024.0


# ---------------------------------------------------------------- вход

def parse_serp_parsed(path, only_cluster=None):
    """
    Достаёт URL из data/serp-parsed.md.

    Формат файла не фиксирован жёстко: кластеры — заголовки '## Кластер: <имя>',
    URL лежат в HTML-таблицах. Берём любые http(s)-ссылки внутри секции кластера,
    порядок и уникальность сохраняем.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()

    chunks = re.split(r"^##\s+Кластер:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if len(chunks) < 3:
        raise SystemExit(
            "Не найдено ни одной секции '## Кластер: ...' в %s — "
            "проверь формат файла или используй --urls" % path
        )

    tasks = []
    seen = set()
    # chunks[0] — преамбула до первого кластера
    for i in range(1, len(chunks), 2):
        name = chunks[i].strip()
        body = chunks[i + 1]
        num = "%02d" % ((i + 1) // 2)
        if only_cluster and num != only_cluster.zfill(2):
            continue
        for m in re.finditer(r'https?://[^\s<>"\')]+', body):
            url = m.group(0).rstrip(".,;")
            key = (num, url)
            if key in seen:
                continue
            seen.add(key)
            tasks.append({"url": url, "cluster": num, "cluster_name": name})
    return tasks


def parse_urls_file(path):
    tasks = []
    seen = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url or url.startswith("#"):
                continue
            if url in seen:
                continue
            seen.add(url)
            tasks.append({"url": url, "cluster": "--", "cluster_name": ""})
    return tasks


# ---------------------------------------------------------------- реестр

def load_index():
    if not os.path.exists(INDEX_PATH):
        return {}
    try:
        with open(INDEX_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {rec["url"]: rec for rec in data.get("pages", [])}
    except (ValueError, KeyError, OSError) as e:
        print("! Реестр %s повреждён (%s), начинаю новый" % (INDEX_PATH, e))
        return {}


def save_index(index):
    os.makedirs(CACHE_DIR, exist_ok=True)
    pages = sorted(index.values(), key=lambda r: (r.get("cluster", ""), r.get("url", "")))
    payload = OrderedDict()
    payload["generated"] = now_iso()
    payload["total"] = len(pages)
    payload["pages"] = pages
    tmp = INDEX_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, INDEX_PATH)


def is_fresh(rec, max_age_days):
    if not rec or rec.get("status") not in ("ok", "pdf", "cert-warning"):
        return False
    raw = rec.get("file_raw")
    if not raw or not os.path.exists(raw):
        return False
    try:
        fetched = datetime.fromisoformat(rec["fetched_at"])
    except (KeyError, ValueError):
        return False
    age = (datetime.now(timezone.utc) - fetched.astimezone(timezone.utc)).total_seconds()
    return age < max_age_days * 86400


# ---------------------------------------------------------------- загрузка

def polite_wait(domain):
    """2–4 секунды между запросами к одному домену; разные домены не ждут друг друга."""
    with _domain_locks[domain]:
        last = _domain_last_hit.get(domain)
        if last is not None:
            delay = random.uniform(*DOMAIN_DELAY)
            elapsed = time.time() - last
            if elapsed < delay:
                time.sleep(delay - elapsed)
        _domain_last_hit[domain] = time.time()


def detect_encoding(resp):
    """
    Заголовки → мета-тег → charset_normalizer.
    cp1251 в русском сегменте встречается часто, поэтому детектор обязателен:
    requests по умолчанию для text/* угадывает ISO-8859-1 и ломает кириллицу.
    """
    ctype = resp.headers.get("Content-Type", "")
    m = re.search(r"charset=([\w\-]+)", ctype, re.IGNORECASE)
    if m:
        enc = m.group(1).strip().lower()
        if enc not in ("iso-8859-1", "latin-1"):
            return enc, "http-header"

    head = resp.content[:4096]
    m = re.search(rb'<meta[^>]+charset=["\']?\s*([\w\-]+)', head, re.IGNORECASE)
    if m:
        return m.group(1).decode("ascii", "ignore").lower(), "meta"
    m = re.search(rb'<meta[^>]+content=["\'][^"\']*charset=([\w\-]+)', head, re.IGNORECASE)
    if m:
        return m.group(1).decode("ascii", "ignore").lower(), "meta"

    if _cn_from_bytes is not None:
        best = _cn_from_bytes(resp.content).best()
        if best is not None:
            return best.encoding, "detector"

    return "utf-8", "fallback"


def fetch_once(url, verify=True):
    return requests.get(
        url, headers=HEADERS, timeout=TIMEOUT, verify=verify,
        allow_redirects=True, stream=False,
    )


def fetch(url):
    """
    Возвращает (resp, cert_warning, error). Три попытки с экспоненциальной паузой,
    на 403/429 пауза длиннее. При ошибке сертификата — повтор с verify=False
    и пометка cert-warning (кейс gubkin.ru).
    """
    cert_warning = False
    last_error = None

    for attempt in range(RETRIES):
        try:
            resp = fetch_once(url, verify=not cert_warning)
            if resp.status_code in (403, 429, 503):
                last_error = "HTTP %d" % resp.status_code
                if attempt < RETRIES - 1:
                    time.sleep((5 * (attempt + 1)) + random.uniform(1, 4))
                    continue
                return resp, cert_warning, last_error
            return resp, cert_warning, None

        except requests.exceptions.SSLError as e:
            last_error = "SSL: %s" % str(e)[:120]
            if not cert_warning:
                cert_warning = True   # следующая попытка — verify=False
                continue
            time.sleep(2 ** attempt)

        except requests.exceptions.Timeout as e:
            last_error = "timeout: %s" % str(e)[:80]
            time.sleep(2 ** attempt)

        except requests.exceptions.RequestException as e:
            last_error = "%s: %s" % (type(e).__name__, str(e)[:100])
            time.sleep(2 ** attempt)

    return None, cert_warning, last_error


# ---------------------------------------------------------------- чистка

def sanitize_text(text):
    """
    Строки, похожие на инструкции модели, заменяются маркером.
    Возвращает (текст, сколько_срабатываний). Оригинал этим не трогается.
    """
    if not text or not INJECTION_RE.search(text):
        return text, 0
    hits = 0
    out_lines = []
    for line in text.splitlines(True):
        if INJECTION_RE.search(line):
            hits += 1
            out_lines.append(SUSPICIOUS_MARK + "\n")
        else:
            out_lines.append(line)
    return "".join(out_lines), hits


def clean_html(html):
    """
    Техническая чистка: ВЫЧИТАНИЕ заведомого не-контента, без всякой фильтрации
    по смыслу. Весь видимый текст, вся структура и все смысловые атрибуты
    (data-*, itemprop, itemscope, href, alt, title, content) остаются на месте.

    Возвращает (clean_html, stats).
    """
    stats = {"scripts": 0, "ldjson_kept": 0, "styles": 0, "links": 0,
             "comments": 0, "base64": 0, "svg": 0, "suspicious": 0}

    soup = BeautifulSoup(html, "lxml")

    # <script>: удаляем все, КРОМЕ JSON-LD — разметка нужна реверсу целиком.
    for tag in soup.find_all("script"):
        stype = (tag.get("type") or "").strip().lower()
        if stype == "application/ld+json":
            stats["ldjson_kept"] += 1
            continue
        tag.decompose()
        stats["scripts"] += 1

    for tag in soup.find_all("style"):
        tag.decompose()
        stats["styles"] += 1

    for tag in soup.find_all("link"):
        rel = " ".join(tag.get("rel") or []).lower()
        if any(k in rel for k in ("stylesheet", "preload", "prefetch", "dns-prefetch", "preconnect")):
            tag.decompose()
            stats["links"] += 1

    # <noscript> с трекерами (img/iframe внутри); осмысленный текст оставляем.
    for tag in soup.find_all("noscript"):
        if tag.find(["img", "iframe", "script"]) and not tag.get_text(strip=True):
            tag.decompose()
            stats["links"] += 1

    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
        stats["comments"] += 1

    # SVG-спрайты (<symbol>/<use> без текста) — чистая графика.
    for tag in soup.find_all("svg"):
        if not tag.get_text(strip=True) and tag.find(["symbol", "use", "path"]):
            tag.decompose()
            stats["svg"] += 1

    for tag in soup.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]
        for attr in ("src", "data-src", "href", "poster", "srcset"):
            val = tag.get(attr)
            if isinstance(val, str) and val.strip().lower().startswith("data:"):
                tag[attr] = BASE64_MARK
                stats["base64"] += 1

    out = str(soup)
    out, hits = sanitize_text(out)
    stats["suspicious"] = hits
    return out, stats


def looks_js_rendered(raw_len, clean_html_text, clean_len):
    """
    Подозрение на JS-рендеринг: clean почти пуст относительно оригинала
    либо текста почти нет при большом HTML.
    """
    if raw_len <= 0:
        return False
    ratio = clean_len / float(raw_len)
    text = BeautifulSoup(clean_html_text, "lxml").get_text(" ", strip=True)
    if ratio < 0.03:
        return True
    if raw_len > 50_000 and len(text) < 1_000:
        return True
    return False


# ---------------------------------------------------------------- обработка одной страницы

def process(task, args):
    url, cluster = task["url"], task["cluster"]
    domain = domain_of(url)
    dirname = os.path.join(CACHE_DIR, safe_dirname(domain))
    h = url_hash(url)
    raw_path = os.path.join(dirname, h + ".html")
    clean_path = os.path.join(dirname, h + ".clean.html")
    pdf_path = os.path.join(dirname, h + ".pdf")

    rec = OrderedDict()
    rec["url"] = url
    rec["cluster"] = cluster
    rec["cluster_name"] = task.get("cluster_name", "")
    rec["domain"] = domain
    rec["fetched_at"] = now_iso()
    rec["final_url"] = None
    rec["http_status"] = None
    rec["encoding"] = None
    rec["encoding_source"] = None
    rec["status"] = "failed"
    rec["error"] = None
    rec["file_raw"] = None
    rec["file_clean"] = None
    rec["size_raw"] = None
    rec["size_clean"] = None
    rec["is_pdf"] = False
    rec["cert_warning"] = False
    rec["suspicious_hits"] = 0
    rec["js_suspect"] = False
    rec["clean_stats"] = None

    polite_wait(domain)
    resp, cert_warning, error = fetch(url)
    rec["cert_warning"] = cert_warning

    if resp is None:
        rec["error"] = error or "нет ответа"
        rec["status"] = "timeout" if error and "timeout" in error else "failed"
        return rec

    rec["http_status"] = resp.status_code
    rec["final_url"] = resp.url

    if resp.status_code in (403, 429):
        rec["status"] = "blocked"
        rec["error"] = "HTTP %d" % resp.status_code
        return rec
    if resp.status_code >= 400:
        rec["status"] = "failed"
        rec["error"] = "HTTP %d" % resp.status_code
        return rec

    os.makedirs(dirname, exist_ok=True)
    ctype = (resp.headers.get("Content-Type") or "").lower()
    is_pdf = "application/pdf" in ctype or url.lower().endswith(".pdf")

    # ---- PDF: кладём сам файл, рядом — извлечённый текст
    if is_pdf:
        rec["is_pdf"] = True
        with open(pdf_path, "wb") as f:
            f.write(resp.content)
        rec["file_raw"] = pdf_path
        rec["size_raw"] = len(resp.content)
        rec["encoding"] = "binary"
        rec["encoding_source"] = "pdf"

        if _pdf_extract_text is None:
            rec["status"] = "failed"
            rec["error"] = "pdfminer недоступен"
            return rec
        try:
            text = _pdf_extract_text(pdf_path) or ""
        except Exception as e:                      # noqa: BLE001 — формат PDF непредсказуем
            rec["status"] = "failed"
            rec["error"] = "pdfminer: %s" % str(e)[:120]
            return rec

        text, hits = sanitize_text(text)
        rec["suspicious_hits"] = hits
        body = ("<!-- PDF-TEXT source=%s -->\n<pre>\n%s\n</pre>\n"
                % (url, text.replace("&", "&amp;").replace("<", "&lt;")))
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(body)
        rec["file_clean"] = clean_path
        rec["size_clean"] = len(body.encode("utf-8"))
        rec["status"] = "pdf"
        return rec

    # ---- защита от нераспакованного сжатия: если сервер отдал кодировку,
    # которую requests не снял (br/zstd без библиотеки), тело — бинарный мусор.
    ce = (resp.headers.get("Content-Encoding") or "").lower()
    if ce and ce not in ("identity", "gzip", "deflate", "x-gzip", ""):
        rec["status"] = "failed"
        rec["error"] = "нераспакованное сжатие Content-Encoding: %s" % ce
        return rec

    # ---- HTML: перекодировка в UTF-8, оригинал сохраняется целиком
    enc, enc_src = detect_encoding(resp)
    rec["encoding"] = enc
    rec["encoding_source"] = enc_src
    try:
        html = resp.content.decode(enc, errors="replace")
    except (LookupError, UnicodeDecodeError):
        html = resp.content.decode("utf-8", errors="replace")
        rec["encoding"] = "utf-8"
        rec["encoding_source"] = "fallback-after-error"

    # Если после декодирования каждый двадцатый символ — replacement (U+FFFD),
    # это не «страница с парой битых знаков», а нераспакованный/неверно
    # раскодированный поток. Не выдаём такой файл за прочитанный.
    if html:
        bad_ratio = html.count("�") / float(len(html))
        if bad_ratio > 0.05:
            rec["status"] = "failed"
            rec["error"] = "битое декодирование: U+FFFD %.0f%% (сжатие/кодировка)" % (bad_ratio * 100)
            return rec

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(html)
    rec["file_raw"] = raw_path
    rec["size_raw"] = os.path.getsize(raw_path)

    cleaned, stats = clean_html(html)
    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    rec["file_clean"] = clean_path
    rec["size_clean"] = os.path.getsize(clean_path)
    rec["clean_stats"] = stats
    rec["suspicious_hits"] = stats["suspicious"]
    rec["js_suspect"] = looks_js_rendered(rec["size_raw"], cleaned, rec["size_clean"])
    rec["status"] = "cert-warning" if cert_warning else "ok"
    return rec


# ---------------------------------------------------------------- отчёт

def report(results, index, tasks_total, from_cache):
    print()
    print("=" * 72)
    print("ОТЧЁТ ЗАГРУЗКИ")
    print("=" * 72)

    by_cluster = defaultdict(lambda: defaultdict(int))
    domains_by_cluster = defaultdict(set)
    ok_domains_by_cluster = defaultdict(set)

    for rec in results:
        c = rec.get("cluster", "--")
        by_cluster[c][rec["status"]] += 1
        domains_by_cluster[c].add(rec["domain"])
        if rec["status"] in ("ok", "pdf", "cert-warning"):
            ok_domains_by_cluster[c].add(rec["domain"])

    print("\nВсего задач: %d | скачано: %d | из кэша: %d"
          % (tasks_total, len(results), from_cache))

    print("\nПо кластерам:")
    for c in sorted(by_cluster):
        counts = by_cluster[c]
        parts = ", ".join("%s: %d" % (k, v) for k, v in sorted(counts.items()))
        print("  кластер %s — %s" % (c, parts))

    failed = [r for r in results if r["status"] in ("failed", "blocked", "timeout")]
    if failed:
        print("\nУПАВШИЕ URL (%d):" % len(failed))
        for r in failed:
            print("  [%s] %s" % (r["status"], r["url"]))
            print("      причина: %s" % (r.get("error") or "—"))

    # покрытие считаем по всему реестру кластера, а не только по текущему запуску
    print("\nПокрытие по доменам (по всему кэшу):")
    all_by_cluster = defaultdict(set)
    ok_all_by_cluster = defaultdict(set)
    for rec in index.values():
        c = rec.get("cluster", "--")
        all_by_cluster[c].add(rec["domain"])
        if rec.get("status") in ("ok", "pdf", "cert-warning"):
            ok_all_by_cluster[c].add(rec["domain"])

    for c in sorted(all_by_cluster):
        total = len(all_by_cluster[c])
        good = len(ok_all_by_cluster[c])
        pct = (100.0 * good / total) if total else 0.0
        line = "  кластер %s — %d/%d доменов (%.0f%%)" % (c, good, total, pct)
        if pct < 50 and total:
            print("\n  " + "!" * 60)
            print("  !!! ВНИМАНИЕ: КЛАСТЕР %s ПОКРЫТ НА %.0f%% — МЕНЬШЕ ПОЛОВИНЫ" % (c, pct))
            print("  !!! Частотность X/Y на такой базе НЕДОСТОВЕРНА.")
            print("  " + "!" * 60)
        else:
            print(line)

    js_suspects = [r for r in results if r.get("js_suspect")]
    if js_suspects:
        print("\nПОДОЗРЕНИЕ НА JS-РЕНДЕРИНГ — дочитать агентом через WebFetch (%d):"
              % len(js_suspects))
        for r in js_suspects:
            print("  %s" % r["url"])
            print("      оригинал %s → clean %s"
                  % (human_size(r["size_raw"]), human_size(r["size_clean"])))

    susp = [r for r in results if r.get("suspicious_hits")]
    if susp:
        print("\nСАНИТИЗИРОВАНО (похоже на инструкции модели, вычищено в clean-версии):")
        for r in susp:
            print("  %s — срабатываний: %d" % (r["url"], r["suspicious_hits"]))

    certs = [r for r in results if r.get("cert_warning")]
    if certs:
        print("\nCERT-WARNING (загружено без проверки сертификата):")
        for r in certs:
            print("  %s" % r["url"])

    print("\nРеестр: %s" % INDEX_PATH)
    print("=" * 72)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Загрузчик страниц топа для реверса (tripl). Только загрузка, без экстракции.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="data/serp-parsed.md — URL берутся из таблиц кластеров")
    src.add_argument("--urls", help="файл со списком URL, по одному на строку")
    ap.add_argument("--cluster", help="только один кластер, номер (например 02)")
    ap.add_argument("--max-age", type=int, default=7,
                    help="не перекачивать кэш свежее N дней (дефолт 7)")
    ap.add_argument("--retry-failed", action="store_true",
                    help="только те URL, что раньше упали (failed/blocked/timeout)")
    ap.add_argument("--limit", type=int, help="взять не больше N URL (для проверки скрипта)")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS,
                    help="параллельных потоков по разным доменам (дефолт 5)")
    ap.add_argument("--report", metavar="PATH",
                    help="дублировать весь вывод в файл (замена shell-`tee`, кросс-платформенно)")
    args = ap.parse_args()

    # --report: пишем весь stdout и в консоль, и в файл (без shell tee / 2>&1)
    if args.report:
        class _Tee:
            def __init__(self, *streams):
                self._streams = streams
            def write(self, data):
                for s in self._streams:
                    s.write(data)
            def flush(self):
                for s in self._streams:
                    s.flush()
        _rf = open(args.report, "w", encoding="utf-8")
        sys.stdout = _Tee(sys.__stdout__, _rf)

    if args.input:
        tasks = parse_serp_parsed(args.input, args.cluster)
    else:
        tasks = parse_urls_file(args.urls)
        if args.cluster:
            print("! --cluster игнорируется при --urls")

    index = load_index()

    if args.retry_failed:
        tasks = [t for t in tasks
                 if index.get(t["url"], {}).get("status") in ("failed", "blocked", "timeout")]
        if not tasks:
            print("Упавших URL в реестре нет — нечего повторять.")
            return

    todo, from_cache = [], 0
    for t in tasks:
        if not args.retry_failed and is_fresh(index.get(t["url"]), args.max_age):
            from_cache += 1
            continue
        todo.append(t)

    if args.limit:
        todo = todo[: args.limit]

    print("Задач всего: %d | из кэша (свежее %d дн.): %d | к загрузке: %d"
          % (len(tasks), args.max_age, from_cache, len(todo)))
    if not todo:
        report([], index, len(tasks), from_cache)
        return

    os.makedirs(CACHE_DIR, exist_ok=True)
    results = []
    done = 0

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(process, t, args): t for t in todo}
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                rec = fut.result()
            except Exception as e:                  # noqa: BLE001 — не ронять пул из-за одной страницы
                rec = {"url": t["url"], "cluster": t["cluster"], "domain": domain_of(t["url"]),
                       "status": "failed", "error": "%s: %s" % (type(e).__name__, str(e)[:120]),
                       "fetched_at": now_iso()}
            results.append(rec)
            with _index_lock:
                index[rec["url"]] = rec
                save_index(index)      # пишем после каждой страницы: падение не теряет прогресс
            done += 1
            flag = ""
            if rec.get("cert_warning"):
                flag += " [cert]"
            if rec.get("js_suspect"):
                flag += " [js?]"
            if rec.get("suspicious_hits"):
                flag += " [sanitized]"
            print("  [%d/%d] %-13s %s%s" % (done, len(todo), rec["status"], rec["url"][:70], flag))

    report(results, index, len(tasks), from_cache)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем. Реестр сохранён.")
        sys.exit(130)
