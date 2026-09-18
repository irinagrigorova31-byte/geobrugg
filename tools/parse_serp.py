#!/usr/bin/env python
"""Парсер выгрузки SERP для serp-parser (методика TRIPL, часть III, раздел 2).

Вход: CSV/XLSX. Поддержаны два формата:
  A) сырой топ-20: колонки Кластер(Группа) / Фраза / URL — частота домена
     выводится как число URL этого домена до схлопывания;
  B) сводка shared-URL: те же колонки + опциональная колонка Частота
     (в скольких запросах кластера встретился данный URL). Тогда каждая
     строка — один уникальный URL, а Частота несёт силу конкурента.
  C) patch v2: сырой топ БЕЗ колонки Кластер — «Фраза ; URL ; позиция».
     Тогда группировка идёт по ФРАЗЕ (провизорно), в выводе флаг
     needs_agent_clustering=true, а intersection_matrix даёт overlap
     ФРАЗА×ФРАЗА для кластеризации агентом serp-parser.

Делает:
  - кластеризацию фраз по группам;
  - схлопывание URL по ХОСТУ (netloc без www) внутри кластера
    (одна строка — один домен); ccTLD-варианты (.com / .co.uk) остаются
    разными хостами — это разные документы, способные со-ранжироваться;
  - по каждому домену: url_count (сколько URL схлопнуто) и, если задана
    колонка частоты, freq_max / freq_sum / список URL с их частотой;
  - исключение маркетплейсов из фиксированного списка (Ozon, WB и т.п.);
    профильные яхт-маркетплейсы (getmyboat, clickandboat, ...) НЕ в списке
    и не исключаются;
  - Y = число уникальных доменов в кластере после чисток;
  - матрицу пересечений доменных множеств между всеми парами кластеров
    (Jaccard = |A∩B| / |A∪B|).

Использование:
    python tools/parse_serp.py <путь> \
        [--encoding utf-8-sig] [--delimiter ';'] \
        [--col-cluster Кластер] [--col-phrase Фраза] [--col-url URL] \
        [--col-freq Частота] [--sheet 0] [--out-json <путь>]

Скрипт только парсит и агрегирует; текстовый отчёт data/serp-parsed.md
собирает вызывающий агент (serp-parser) вручную на основе JSON-вывода.
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

MARKETPLACE_DOMAINS = {
    "ozon.ru": "маркетплейс (Ozon)",
    "wildberries.ru": "маркетплейс (Wildberries)",
    "market.yandex.ru": "маркетплейс (Яндекс.Маркет)",
    "avito.ru": "маркетплейс (Авито)",
}


def normalize_domain(url: str) -> str:
    """Хост без www для схлопывания дублей. ccTLD-варианты не сливаются."""
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def read_csv(path, encoding, delimiter, col_cluster, col_phrase, col_url, col_freq):
    with open(path, encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames
        # Кластер теперь ОПЦИОНАЛЕН: patch v2 подаёт «Фраза;URL;позиция» без него,
        # кластеризацию делает агент serp-parser по пересечению выдачи. Если колонки
        # Кластер нет — группируем по фразе (провизорный кластер = фраза).
        required = [col_phrase, col_url]
        missing = [c for c in required if c not in fieldnames]
        if missing:
            raise ValueError(
                f"Не найдены колонки {missing} в файле {path}. "
                f"Фактические заголовки: {fieldnames}"
            )
        has_cluster = col_cluster in (fieldnames or [])
        has_freq = col_freq is not None and col_freq in fieldnames
        rows = []
        for row in reader:
            freq = None
            if has_freq:
                raw = (row.get(col_freq) or "").strip()
                freq = int(raw) if raw.isdigit() else None
            phrase = (row[col_phrase] or "").strip()
            cluster = (row[col_cluster] or "").strip() if has_cluster else phrase
            rows.append({
                "cluster": cluster,
                "phrase": phrase,
                "url": (row[col_url] or "").strip(),
                "freq": freq,
                "position": (row.get("позиция") or row.get("position") or "").strip(),
            })
    return rows, fieldnames, has_freq, has_cluster


def read_xlsx(path, sheet, col_cluster, col_phrase, col_url, col_freq):
    import pandas as pd

    df = pd.read_excel(path, sheet_name=sheet, dtype=str)
    required = [col_phrase, col_url]           # Кластер опционален (см. read_csv)
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Не найдены колонки {missing} в файле {path}. "
            f"Фактические заголовки: {list(df.columns)}"
        )
    has_cluster = col_cluster in list(df.columns)
    has_freq = col_freq is not None and col_freq in df.columns
    rows = []
    for _, r in df.iterrows():
        freq = None
        if has_freq:
            raw = str(r.get(col_freq) or "").strip()
            freq = int(raw) if raw.isdigit() else None
        phrase = str(r[col_phrase] or "").strip()
        cluster = str(r[col_cluster] or "").strip() if has_cluster else phrase
        rows.append({
            "cluster": cluster,
            "phrase": phrase,
            "url": str(r[col_url] or "").strip(),
            "freq": freq,
            "position": str(r.get("позиция") or r.get("position") or "").strip(),
        })
    return rows, list(df.columns), has_freq, has_cluster


def build_clusters(rows):
    clusters = defaultdict(lambda: {"phrases": set(), "urls": []})
    for row in rows:
        if not row["url"]:
            continue
        clusters[row["cluster"]]["phrases"].add(row["phrase"])
        clusters[row["cluster"]]["urls"].append((row["url"], row["freq"]))

    result = {}
    for cluster, data in clusters.items():
        by_domain = defaultdict(list)  # dom -> list of (url, freq)
        for url, freq in data["urls"]:
            by_domain[normalize_domain(url)].append((url, freq))

        kept, excluded = [], []
        for dom, urls in by_domain.items():
            freqs = [f for (_, f) in urls if f is not None]
            entry = {
                "domain": dom,
                "url": urls[0][0],
                "url_count": len(urls),
                "urls": [{"url": u, "freq": f} for (u, f) in urls],
                "freq_max": max(freqs) if freqs else None,
                "freq_sum": sum(freqs) if freqs else None,
            }
            if dom in MARKETPLACE_DOMAINS:
                entry["reason"] = MARKETPLACE_DOMAINS[dom]
                excluded.append(entry)
            else:
                kept.append(entry)

        def sort_key(e):
            return (-(e["freq_max"] or 0), -e["url_count"], e["domain"])
        kept.sort(key=sort_key)

        result[cluster] = {
            "phrases": sorted(data["phrases"]),
            "urls_total_raw": len(data["urls"]),
            "domains_kept": kept,
            "domains_excluded": excluded,
            "Y": len(kept),
        }
    return result


def intersection_matrix(clusters):
    names = sorted(clusters.keys())
    domain_sets = {n: set(d["domain"] for d in clusters[n]["domains_kept"]) for n in names}
    matrix, pairs = {}, []
    for a in names:
        matrix[a] = {}
        for b in names:
            if a == b:
                matrix[a][b] = 1.0
                continue
            sa, sb = domain_sets[a], domain_sets[b]
            union = sa | sb
            matrix[a][b] = len(sa & sb) / len(union) if union else 0.0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if matrix[a][b] >= 0.70:
                pairs.append({
                    "a": a, "b": b, "fraction": matrix[a][b],
                    "shared_domains": sorted(domain_sets[a] & domain_sets[b]),
                })
    # общие домены по всем парам (для отчёта, даже ниже порога)
    shared_all = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared_all[f"{a}|{b}"] = sorted(domain_sets[a] & domain_sets[b])
    return names, matrix, pairs, shared_all


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--encoding", default="utf-8-sig")
    ap.add_argument("--delimiter", default=";")
    ap.add_argument("--col-cluster", default="Кластер")
    ap.add_argument("--col-phrase", default="Фраза")
    ap.add_argument("--col-url", default="URL")
    ap.add_argument("--col-freq", default="Частота")
    ap.add_argument("--sheet", default=0)
    ap.add_argument("--out-json", type=Path, default=None)
    args = ap.parse_args()

    path = args.path
    if not path.exists():
        print(f"Файл не найден: {path}", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() in (".xlsx", ".xls"):
        rows, headers, has_freq, has_cluster = read_xlsx(path, args.sheet, args.col_cluster, args.col_phrase, args.col_url, args.col_freq)
    else:
        rows, headers, has_freq, has_cluster = read_csv(path, args.encoding, args.delimiter, args.col_cluster, args.col_phrase, args.col_url, args.col_freq)

    clusters = build_clusters(rows)
    names, matrix, pairs, shared_all = intersection_matrix(clusters)

    # Без входной колонки Кластер группировка идёт по ФРАЗЕ (провизорно), а матрица
    # пересечений становится сигналом overlap ФРАЗА×ФРАЗА для кластеризации агентом.
    clustered_by = "input-column" if has_cluster else "phrase-provisional"

    out = {
        "source_file": str(path),
        "headers": headers,
        "freq_column_used": has_freq,
        "clustered_by": clustered_by,
        "needs_agent_clustering": not has_cluster,
        "n_rows": len(rows),
        "n_clusters": len(clusters),
        "clusters": clusters,
        "intersection_matrix": matrix,
        "shared_domains_all_pairs": shared_all,
        "merge_candidates_ge_70pct": pairs,
    }

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out_json:
        args.out_json.write_text(text, encoding="utf-8")
        print(f"Сохранено: {args.out_json}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
