#!/usr/bin/env python
"""Bootstrap новой ниши tripl из чистого шаблона (кросс-платформенно: macOS/Windows/Linux).

Копирует движок шаблона в отдельную папку ниши, заполняет блок «ПАРАМЕТРЫ ЭТОЙ НИШИ»
в CLAUDE.md значениями из аргументов, оставляет data/output-папки пустыми. Project-скилл
и layout-скилл НЕ создаются — их генерит niche-expert на первом прогоне.

Пример:
    python tools/new_niche.py \
        --slug barcelona-boats \
        --niche-name "yacht charter" \
        --domain example.com \
        --lang "English (US/UK)" \
        --market "Google / Europe" \
        --page-type "commercial landings" \
        --humanizer base \
        [--client-brief path/to/about.md] \
        [--template .] [--dest ../tripl-<slug>]

Ничего в сети не делает; только файловые операции через pathlib/shutil.
"""

import argparse
import shutil
import sys
from pathlib import Path

# Файлы/папки движка, которые НЕСЁМ в новую нишу.
ENGINE = [
    ".claude/agents",
    ".claude/commands",
    ".claude/skills/humanizer",
    ".claude/skills/impeccable",
    ".claude/skills/external-PLATFORM",   # пустой шаблон правил площадки (off-site), клонируется в external-<platform>
    ".claude/ORCHESTRATION.md",
    ".claude/PIPELINE.md",
    ".claude/settings.local.json",
    "tools",
    "methodology",
    "CLAUDE.md",
    "input/company.md",   # пустой owned-шаблон (patch v2) — оператор заполняет на нишу
    "input/backlinks.md", # off-site бэклинки от оператора (целевой URL · анкор, follow)
    "input/prompts.md",   # prompt-set: ключи + ИИ-промпты для таргетинга цитирования (опц., оператор)
    "input/brand.md",     # дизайн-система проекта (палитра/шрифты/логотип/тон) — читает hero-maker и layout
    "data/interlinks.md", # кокон-карта (силосы + граф внутренних ссылок) — скелет, tz-writer заполняет
    "data/authorities.md", # реестр авторитетных первоисточников ниши (on-site ссылки) — ведёт niche-expert
]

# Пустые каркасы data/output, которые создаём в новой нише.
EMPTY_DIRS = [
    "input", "input/serp", "input/reviews", "data", "data/tz", "data/tz-ext", "drafts", "preview",
    "delivery", "review", "cache", "cache/pages", "assets", "assets/hero", "assets/brand", "docs",
    "output",     # serp-prep пишет output/to-parse.txt
    "external",   # off-site-ветка: готовые тексты под чужие площадки
]

# Токены-плейсхолдеры в шаблонном CLAUDE.md.
TOKENS = ["SLUG", "NICHE_NAME", "DOMAIN", "LANG", "MARKET", "PAGE_TYPE", "HUMANIZER", "CLIENT_BRIEF"]

ABOUT_STUB = """# Карточка клиента / бриф (заполнить)

Домен: {domain}
Ниша: {niche_name}

<!-- Замените этот файл реальным брифом клиента, либо запустите с --client-brief. -->
"""


def copy_engine(template: Path, dest: Path) -> None:
    for rel in ENGINE:
        src = template / rel
        dst = dest / rel
        if not src.exists():
            print(f"! пропуск (нет в шаблоне): {rel}", file=sys.stderr)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(
                src, dst,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", "hook.cache.json"),
            )
        else:
            shutil.copy2(src, dst)


def make_empty_dirs(dest: Path) -> None:
    for d in EMPTY_DIRS:
        p = dest / d
        p.mkdir(parents=True, exist_ok=True)
        (p / ".gitkeep").touch()


def fill_claude_md(dest: Path, values: dict) -> None:
    claude = dest / "CLAUDE.md"
    text = claude.read_text(encoding="utf-8")
    for tok in TOKENS:
        text = text.replace("{{" + tok + "}}", values.get(tok, ""))
    claude.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Bootstrap новой ниши tripl из шаблона.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--slug", required=True, help="короткий slug ниши, напр. barcelona-boats")
    ap.add_argument("--niche-name", required=True, help="человекочитаемое имя ниши")
    ap.add_argument("--domain", required=True, help="домен клиента")
    ap.add_argument("--lang", required=True, help='язык вывода, напр. "English (US/UK)"')
    ap.add_argument("--market", required=True, help='рынок, напр. "Google / Europe" или "Яндекс / РФ"')
    ap.add_argument("--page-type", required=True, help='тип страниц, напр. "commercial landings"')
    ap.add_argument("--humanizer", default="base", choices=["base", "ru-adapt"],
                    help="вариант humanizer (base = базовый EN; ru-adapt = русская адаптация)")
    ap.add_argument("--client-brief", type=Path, default=None,
                    help="путь к готовому брифу → скопируется в input/about.md")
    ap.add_argument("--template", type=Path, default=Path(__file__).resolve().parent.parent,
                    help="папка шаблона (дефолт — родитель этого скрипта)")
    ap.add_argument("--dest", type=Path, default=None,
                    help="папка новой ниши (дефолт — ../tripl-<slug> рядом с шаблоном)")
    args = ap.parse_args()

    template = args.template.resolve()
    dest = (args.dest or template.parent / f"tripl-{args.slug}").resolve()

    if not (template / "CLAUDE.md").exists():
        print(f"! не похоже на шаблон tripl: {template} (нет CLAUDE.md)", file=sys.stderr)
        return 1
    if dest.exists():
        print(f"! папка уже существует, не перезаписываю: {dest}", file=sys.stderr)
        return 1

    dest.mkdir(parents=True)
    copy_engine(template, dest)
    make_empty_dirs(dest)

    fill_claude_md(dest, {
        "SLUG": args.slug,
        "NICHE_NAME": args.niche_name,
        "DOMAIN": args.domain,
        "LANG": args.lang,
        "MARKET": args.market,
        "PAGE_TYPE": args.page_type,
        "HUMANIZER": args.humanizer,
        "CLIENT_BRIEF": args.domain,
    })

    about = dest / "input" / "about.md"
    if args.client_brief and args.client_brief.exists():
        shutil.copy2(args.client_brief, about)
    else:
        about.write_text(ABOUT_STUB.format(domain=args.domain, niche_name=args.niche_name),
                         encoding="utf-8")
    (dest / "input" / "keywords.md").write_text(
        "# Ключевые запросы (заполнить или положить топ в input/serp/)\n", encoding="utf-8")

    print(f"Ниша создана: {dest}")
    print("Дальше:")
    print(f"  1. Заполнить input/company.md (owned-карточка бизнеса).")
    print(f"  2. Положить сырой топ в input/serp/ (Фраза;URL;позиция, utf-8-sig, ';').")
    print(f"  3. Открыть папку в Claude Code и запустить /tripl-collect.")
    print(f"  (project-скилл и layout-скилл сгенерит niche-expert на первом прогоне.)")
    print(f"  (off-site: бэклинки на свой сайт — в input/backlinks.md (целевой URL · анкор, follow).)")
    print(f"  (кокон-карту data/interlinks.md ведёт tz-writer — скелет уже на месте.)")
    print(f"  (опц. prompt-set: ключи + ИИ-промпты для таргетинга цитат — в input/prompts.md.)")
    print(f"  (опц. дизайн-система: палитра/шрифты/логотип/тон — в input/brand.md (+ assets/brand/);")
    print(f"        заполни на старте, чтобы обложки вышли в фирменном стиле — читает hero-maker.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
