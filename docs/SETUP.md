# SETUP — установка и разворачивание tripl (macOS / Windows / Linux)

Этот файл написан так, чтобы уже выполненные шаги можно было пропускать. Прочитай раздел
под свою ОС, поставь недостающее, дальше — «Новая ниша».

---

## 1. Пререквизиты

| Что | Зачем | Проверка |
|---|---|---|
| **Python 3.9+** на PATH как `python` | все агенты вызывают `python tools/*.py` | `python --version` |
| **Node.js** | impeccable-хук дизайн-проверки (`.claude/skills/impeccable/scripts/hook.mjs`) | `node --version` |
| **Google Chrome** | render-проверка layout-скилла (headless-скриншот) | путь ниже |
| **pip-зависимости** | загрузчик топа и парсеры | см. п.3 |

### macOS
- Python обычно есть как `python3`. Движок зовёт `python` → добавь алиас в `~/.zshrc`:
  `alias python=python3` (или поставь python.org/pyenv, дающий `python`).
- Node: `brew install node`. Chrome: обычная установка.
- `export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`.

### Windows (сервер — основная цель)
- Python с python.org → при установке галочка «Add python.exe to PATH». Даёт `python` и `py`.
- Node.js LTS с nodejs.org (даёт `node` на PATH).
- Google Chrome — обычная установка.
- `setx CHROME "C:\Program Files\Google\Chrome\Application\chrome.exe"` (в PowerShell: `$env:CHROME`).
- Всё в проекте использует относительные пути и `python` — bash не нужен; команды идут в PowerShell/cmd.

### Linux
- `python`/`python3` из пакетов; Node из nodesource; `google-chrome` на PATH.
- `export CHROME=google-chrome`.

---

## 2. pip-зависимости

```
python -m pip install requests urllib3 beautifulsoup4
```

Опционально (улучшают загрузчик, не обязательны):
```
python -m pip install charset_normalizer pdfminer.six
```

`tools/homoglyph_check.py`, `tools/parse_serp.py`, `tools/new_niche.py`, `check.py` layout-скилла —
на stdlib, доп. пакетов не требуют. `requests`/`bs4` нужны только `tools/fetch_pages.py`.

Проверка: `python tools/parse_serp.py --help`, `python tools/fetch_pages.py --help`, `node --version`.

---

## 3. Перенос шаблона на Windows-сервер

1. Скопировать папку `tripl-template` целиком на сервер (напр. `C:\claude\tripl-template`).
2. Пройти п.1–2 (Python/Node/Chrome/pip).
3. Проверить: из корня шаблона `python tools\parse_serp.py --help` печатает справку.
4. Дальше — «Новая ниша».

Шаблон уже переносим: нет `.sh`-скриптов, `python3` заменён на `python`, хуки в
`.claude/settings.local.json` вызывают `node` по относительному пути (работает в cmd/PowerShell/bash),
пути в коде — через `pathlib`/`os.path.join`. Детали переносимости — `docs/PORTABILITY.md`.

---

## 4. Новая ниша

Из папки шаблона:

```
python tools/new_niche.py --slug <slug> --niche-name "<имя ниши>" --domain <домен> \
    --lang "<язык вывода>" --market "<рынок>" --page-type "<тип страниц>" \
    --humanizer <base|ru-adapt> [--client-brief <путь к брифу>]
```

Пример:
```
python tools/new_niche.py --slug barcelona-boats --niche-name "yacht charter" \
    --domain example.com --lang "English (US/UK)" --market "Google / Europe" \
    --page-type "commercial landings" --humanizer base
```

Создаст `../tripl-<slug>/` с движком, заполненным блоком ниши в `CLAUDE.md` и пустыми data/output.
Дальше по подсказке скрипта: заполнить `input/company.md`, положить топ в `input/serp/`, открыть
папку в Claude Code и запустить `/tripl-collect`. project-скилл и layout-скилл сгенерит `niche-expert`
на первом прогоне.

Windows: `python tools\new_niche.py ...` (обратные слэши в пути — скрипт нормализует сам).
