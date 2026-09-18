# PORTABILITY — переносимость движка + заметка о втором режиме письма

## A. Что сделано для кросс-платформенности (macOS / Windows / Linux)

Шаблон рассчитан на запуск и на Windows-сервере, и на mac-дев-боксе. Правки:

1. **`python3` → `python`** во всех промптах агентов, командах, доках и `CLAUDE.md`. На Windows
   `python` есть после установки с python.org; на macOS нужен алиас `alias python=python3`
   (см. `docs/SETUP.md`). Шебанги `#!/usr/bin/env python` в `tools/*.py` некритичны — скрипты
   зовутся как `python tools/x.py`, шебанг не участвует.
2. **Хуки** в `.claude/settings.local.json` вызывают `node .claude/skills/impeccable/scripts/hook.mjs`
   по ОТНОСИТЕЛЬНОМУ пути, без POSIX-guard `[ -f ] ||` и без `${CLAUDE_PROJECT_DIR}`-разворота в шелле.
   Работает в cmd/PowerShell/bash при CWD = корень проекта (штатно для хуков Claude Code); `hook.mjs`
   сам читает `CLAUDE_PROJECT_DIR` из env, где нужно. Условие: Node на PATH.
3. **Путь к Chrome** в layout-скилле — через env-переменную `$CHROME` (macOS/Windows/Linux варианты
   в `docs/SETUP.md` и в самом SKILL.md layout-скилла). Не хардкодить `/Applications/...`.
4. **Проверка ссылок** в `check.py` layout-скилла — на stdlib `urllib` вместо `curl -o /dev/null`
   (нет `curl`/`/dev/null` в cmd). Эталон для будущих layout-скиллов.
5. **Отчёт загрузчика** — флаг `python tools/fetch_pages.py --report <path>` пишет отчёт сам,
   вместо shell-`2>&1 | tee` (не работает в cmd).
6. **Bootstrap** — `tools/new_niche.py` (кросс-платформенный, pathlib), НЕ `.sh`.
7. **Абсолютные mac-пути** не несём: `.impeccable/hook.cache.json` (кэш самовосстанавливается),
   `settings.local.json.allow` очищен от `/private/tmp`, `/Users`, `md5 -q`, `chmod`, `command -v`.

**Переносимо как есть:** `tools/*.py` (pathlib/os.path.join/os.replace, явный utf-8/utf-8-sig),
`cache/pages/index.json` (относительные пути с прямыми слэшами резолвятся и на Windows).

**Проверка после переноса:** grep по шаблону не должен находить `python3`, `/Applications`,
`/dev/null`, `| tee`, `/Users/`, `md5 -q`, `chmod` (кроме файлов-справок, регенерируемых на нишу).

---

## B. Off-site ветка (внешние площадки под AI/GEO) — ПОСТРОЕНА в этом же шаблоне

СТАТУС: реализовано как ВТОРАЯ писательская ветка в ОДНОМ шаблоне (не отдельная сборка). Один проект,
один сбор, две ветки — разводит `data/citation-gaps.md` (gap-классификатор в domain-inventory): on-site
(своя страница цитируемее) vs off-site (размещение на чужих площадках). Отложена ТОЛЬКО одна вещь —
контент правил конкретных площадок (скиллы `external-<platform>`, pluggable, задаёт владелец инструкцией).

Агенты off-site: placement-strategist → external-tz-writer → external-copywriter → external-gist-auditor →
geo-monitor (+ homoglyph-checker). Команды: /tripl-ext-plan, /tripl-ext-write, /tripl-ext-monitor. Выход в
`external/`, И `.md`, И HTML-фрагмент (параметром). Подробности потока — `.claude/ORCHESTRATION.md §6б`.

Ниже — исходная карта шва (актуальна как описание архитектуры разведения on/off):

**Где живёт режим.** On-site-модель сосредоточена в `tz-writer` (структура ТЗ). `copywriter` —
тонкий исполнитель ТЗ, получает только пути. Значит режим = вариант ТЗ + носитель режима (аргумент
оркестратора + маркер в ТЗ) + подмена скилла. Generic-агенты уже не запекают on-site-допущения.

**onsite-ТЗ (как сейчас):** силос-перелинковка, План JSON-LD, Мета, 2-блочная модель HERO+витрина,
ВНЕШНИЕ ПОДТВЕРЖДЕНИЯ, NAP.

**external-ТЗ (будущее):** БЕЗ силоса/JSON-LD/меты/витрины; вместо — целевая площадка, формат
площадки, политика бэклинка на свой сайт, disclosure/авторство, CTA-правила. Контент правил — из
будущей инструкции, ляжет в новый скилл `external-<platform>` (аналог layout-скилла, но off-site).

**copywriter в external-режиме:** тот же исполнитель, грузит `external-<platform>` вместо on-site
layout, пропускает downstream (schema-markup/page-builder/layout); выход в отдельную папку `external/`;
поддержка И `.md`, И HTML-фрагмента (выбор параметром).

**gist-auditor:** движок III-6 переиспользуется; в external-режиме пропускается on-site-проверка
«непоставленных ссылок» и (уже отключённый) яндекс-carve-out.

**Общее для обоих режимов (без изменений):** serp-parser, triplet-collector, entity-mapper,
domain-inventory, niche-expert, `project-<slug>`, humanizer. Весь слой ПОНИМАНИЯ ниши
переиспользуется; расходятся только ДИЗАЙН ВЫХОДА (tz-writer) и доставка.

**Вывод:** структурной переделки под external НЕ потребуется — шов чистый. Когда придёт инструкция:
(1) новый скилл `external-<platform>`, (2) режим в tz-writer + маркер в ТЗ, (3) ветка в copywriter
(подмена скилла + пропуск downstream + выбор md/html), (4) пропуск on-site-проверок в gist-auditor,
(5) папка `external/`.
