#!/usr/bin/env python
"""Проверка текстов на гомоглифы и невидимые символы.

Реализация техчека из методики TRIPL: methodology/part-III-audit.md, раздел 6а.
Правило: в одном слове не должно быть двух алфавитов.

Уровни находок:
    КРИТИЧНО — алфавиты смешаны внутри одной непрерывной последовательности букв
               («аpple», «Mercedеs»). Сущность не опознаётся, артикул не находится.
    ВНИМАНИЕ — алфавиты разделены дефисом или подчёркиванием и каждая часть
               однородна («Wi-Fi», «HSK-курсы», «ССЫЛКА_НА_VK»), либо слово в белом
               списке. Отфильтровано, видно только с --strict.

Использование:
    python tools/homoglyph_check.py methodology/
    python tools/homoglyph_check.py methodology/ --all      # все текстовые файлы, любое расширение
    python tools/homoglyph_check.py methodology/ --strict   # без фильтрации, всё подряд
    python tools/homoglyph_check.py methodology/ --fix      # заменит невидимые символы

Пропущенное всегда перечисляется в конце отчёта: «проблем не найдено» не должно
читаться как «всё проверено».

По умолчанию ничего не правит — только отчёт. Гомоглифы не правятся никогда:
машина не знает, какая буква задумана, замена вслепую испортит артикулы.

Белый список: tools/homoglyph-whitelist.txt (по слову в строке, # — комментарий),
читается при запуске, если файл есть. Сравнение регистронезависимое.

Код возврата: 0 — чисто, 1 — найдены проблемы, 2 — проверка не выполнялась
(путь не существует, нет подходящих файлов, все файлы бинарные).
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

EXTENSIONS = {
    ".md", ".html", ".htm", ".json", ".jsonld", ".csv", ".tsv",
    ".txt", ".xml", ".svg", ".yaml", ".yml",
}

# Сколько пропущенных файлов перечислять поимённо, остальные — счётчиком.
LIST_LIMIT = 30

WHITELIST_PATH = Path(__file__).with_name("homoglyph-whitelist.txt")

# Невидимые символы: неразрывный пробел, мягкий перенос, zero-width space,
# word joiner, BOM. Значение — на что заменяется при --fix.
# Ключи заданы escape-последовательностями намеренно: literal-символы здесь
# невидимы и молча нормализуются редакторами (U+00A0 → обычный пробел),
# после чего чек считает все пробелы подряд.
INVISIBLE = {
    "\u00a0": " ",   # неразрывный пробел -> обычный
    "\u00ad": "",    # мягкий перенос
    "\u200b": "",    # zero-width space
    "\u2060": "",    # word joiner
    "\ufeff": "",    # BOM / zero-width no-break space
}

INVISIBLE_NAMES = {
    "\u00a0": "U+00A0 NO-BREAK SPACE",
    "\u00ad": "U+00AD SOFT HYPHEN",
    "\u200b": "U+200B ZERO WIDTH SPACE",
    "\u2060": "U+2060 WORD JOINER",
    "\ufeff": "U+FEFF ZERO WIDTH NO-BREAK SPACE (BOM)",
}

# Слово целиком, включая внутренние дефисы и подчёркивания: «Wi-Fi», «ССЫЛКА_НА_VK».
WORD_RE = re.compile(r"\w+(?:[-_]\w+)*")
SEGMENT_RE = re.compile(r"[-_]+")

# Буквы escape-последовательностей: \n, \t, а и т.п. (см. mixed_script).
ESCAPE_LETTERS = set("abfnrtvxuUN")

LEVEL_CRITICAL = "КРИТИЧНО"
LEVEL_WARNING = "ВНИМАНИЕ"


def script_of(char):
    """Алфавит символа по имени Unicode: LATIN, CYRILLIC, GREEK и т.д."""
    name = unicodedata.name(char, "")
    return name.split()[0] if name else "UNKNOWN"


def analyze_word(word):
    """Разбор слова по частям (дефис/подчёркивание — границы).

    Вернёт (все алфавиты слова, критично ли). Критично — если хотя бы одна часть
    сама по себе смешана; тогда разделителями смешение не объясняется.
    """
    all_scripts = set()
    critical = False
    for segment in SEGMENT_RE.split(word):
        scripts = {script_of(c) for c in segment if c.isalpha()}
        all_scripts |= scripts
        if len(scripts) > 1:
            critical = True
    return all_scripts, critical


def mixed_script(text):
    """Вернёт слова, где смешаны алфавиты: (слово, алфавиты, уровень)."""
    for match in WORD_RE.finditer(text):
        word = match.group()
        # В исходниках («\nГомоглифы», «а») обратный слэш не входит в \w,
        # и буква escape-последовательности прилипает к следующему слову.
        # Без этого любой .py с "\n" перед кириллицей даёт ложное КРИТИЧНО.
        if (
            match.start() > 0
            and text[match.start() - 1] == "\\"
            and len(word) > 1
            and word[0] in ESCAPE_LETTERS
        ):
            word = word[1:]
        scripts, critical = analyze_word(word)
        if len(scripts) > 1:
            yield word, sorted(scripts), LEVEL_CRITICAL if critical else LEVEL_WARNING


def load_whitelist(path=WHITELIST_PATH):
    """Слова-исключения, по одному в строке. # — комментарий. Регистр игнорируется."""
    if not path.is_file():
        return set()
    words = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            words.add(line.casefold())
    return words


def is_binary(path, chunk=8192):
    """Бинарный ли файл: нулевой байт или неразбираемый UTF-8 в начале файла."""
    try:
        raw = path.read_bytes()[:chunk]
    except OSError:
        return True
    if b"\x00" in raw:
        return True
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        # Обрыв многобайтового символа на границе чанка — не признак бинарника.
        return exc.start < len(raw) - 4
    return False


def collect_files(root, check_all=False):
    """Вернёт (файлы к проверке, пропущенные по расширению).

    Явно указанный файл проверяется всегда, независимо от расширения.
    Ничего не пропускается молча: пропущенное возвращается вызывающему для отчёта.
    """
    if root.is_file():
        return [root], []
    if not root.is_dir():
        return [], []
    targets, skipped = [], []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if check_all or path.suffix.lower() in EXTENSIONS:
            targets.append(path)
        else:
            skipped.append(path)
    return targets, skipped


def check_file(path, whitelist):
    """Вернёт (находки-гомоглифы, счётчик невидимых символов, ошибка чтения).

    Находка: (строка, слово, алфавиты, уровень, причина фильтрации или None).
    Фильтрация здесь только помечается — решение о показе принимает вызывающий.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        return [], {}, str(exc)

    homoglyphs = []
    invisible = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        for word, scripts, level in mixed_script(line):
            if word.casefold() in whitelist:
                reason = "в белом списке"
            elif level == LEVEL_WARNING:
                reason = "разделено дефисом/подчёркиванием, части однородны"
            else:
                reason = None
            homoglyphs.append((lineno, word, scripts, level, reason))
        for char in INVISIBLE:
            count = line.count(char)
            if count:
                entry = invisible.setdefault(char, {"total": 0, "lines": []})
                entry["total"] += count
                entry["lines"].append(lineno)
    return homoglyphs, invisible, None


def fix_file(path):
    """Заменит невидимые символы по таблице INVISIBLE. Вернёт число замен."""
    text = path.read_text(encoding="utf-8")
    replaced = 0
    for char, repl in INVISIBLE.items():
        count = text.count(char)
        if count:
            text = text.replace(char, repl)
            replaced += count
    if replaced:
        path.write_text(text, encoding="utf-8")
    return replaced


def rel(path, root):
    try:
        return path.relative_to(root if root.is_dir() else root.parent)
    except ValueError:
        return path


def main():
    parser = argparse.ArgumentParser(
        description="Проверка на гомоглифы (смешанные алфавиты в слове) и невидимые символы.",
    )
    parser.add_argument("path", help="файл или папка (папка обходится рекурсивно)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="отключить фильтрацию: показать всё, включая дефисные составные и белый список",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="проверять все текстовые файлы независимо от расширения; бинарные пропускать",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="заменить невидимые символы в файлах; гомоглифы не правятся никогда",
    )
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"ОШИБКА: путь не существует: {root}", file=sys.stderr)
        print("Ничего не проверено.", file=sys.stderr)
        return 2

    files, skipped_ext = collect_files(root, args.all)
    if not files:
        print(f"ОШИБКА: в {root} нечего проверять — ни одного подходящего файла.", file=sys.stderr)
        if skipped_ext:
            print(
                f"Пропущено по расширению: {len(skipped_ext)}."
                " Прогнать по всем текстовым файлам: --all",
                file=sys.stderr,
            )
        else:
            print("Каталог пуст.", file=sys.stderr)
        print("Это НЕ значит «проблем не найдено» — проверка не выполнялась.", file=sys.stderr)
        return 2

    whitelist = set() if args.strict else load_whitelist()
    skipped_binary = []

    shown_critical = 0
    shown_warning = 0
    filtered = 0
    total_invisible = 0
    total_fixed = 0
    files_with_issues = 0
    unreadable = []

    scope = "все текстовые файлы (--all)" if args.all else ", ".join(sorted(EXTENSIONS))
    print(f"Проверка: {root}  (охват: {scope})")
    mode = "строгий, без фильтрации" if args.strict else f"белый список: {len(whitelist)} сл."
    print(f"Режим: {mode}")
    print("=" * 78)

    for path in files:
        if is_binary(path):
            skipped_binary.append(path)
            continue
        homoglyphs, invisible, error = check_file(path, whitelist)
        if error:
            unreadable.append((path, error))
            continue

        visible = [f for f in homoglyphs if args.strict or f[4] is None]
        filtered += len(homoglyphs) - len(visible)
        invisible_count = sum(e["total"] for e in invisible.values())
        if not visible and not invisible_count:
            continue

        files_with_issues += 1
        total_invisible += invisible_count
        name = rel(path, root)

        for lineno, word, scripts, level, reason in visible:
            if level == LEVEL_CRITICAL:
                shown_critical += 1
            else:
                shown_warning += 1
            note = f"  [{reason}]" if reason else ""
            print(f"{level:9} {name}:{lineno}: {word} : смешаны {' + '.join(scripts)}{note}")

        for char, entry in invisible.items():
            lines = entry["lines"]
            shown = ", ".join(str(n) for n in lines[:10])
            if len(lines) > 10:
                shown += f", … (+{len(lines) - 10})"
            print(
                f"{LEVEL_CRITICAL:9} {name}: невидимый символ {INVISIBLE_NAMES[char]}"
                f" × {entry['total']} : строки {shown}"
            )

        if args.fix and invisible_count:
            fixed = fix_file(path)
            total_fixed += fixed
            print(f"{'ИСПРАВЛЕНО':9} {name}: невидимых символов заменено: {fixed}")

    checked = len(files) - len(skipped_binary)

    print("=" * 78)
    print(f"Проверено файлов: {checked}")
    print(f"Файлов с проблемами: {files_with_issues}")
    print(f"КРИТИЧНО (смешение внутри слова): {shown_critical}")
    if args.strict:
        print(f"ВНИМАНИЕ (разделители/белый список): {shown_warning}")
    else:
        print(f"Отфильтровано ложных срабатываний: {filtered}" + (" (показать: --strict)" if filtered else ""))
    print(f"Невидимых символов: {total_invisible}")
    if args.fix:
        print(f"Заменено невидимых символов: {total_fixed}")
    elif total_invisible:
        print("Ничего не изменено. Для замены невидимых символов: --fix")
    if unreadable:
        print(f"Не удалось прочитать: {len(unreadable)}")
        for path, error in unreadable:
            print(f"  {rel(path, root)}: {error}")

    if shown_critical:
        print("\nГомоглифы не правятся автоматически — проверить вручную:")
        print("подмена может быть намеренным примером (см. раздел 6а про IDN-домены).")
        print(f"Осознанные исключения вносить в {WHITELIST_PATH.name}.")

    report_skipped(root, skipped_ext, skipped_binary, checked, args.all)

    if checked == 0:
        print(
            "\nОШИБКА: не проверено НИ ОДНОГО файла — все отсеяны как бинарные.",
            file=sys.stderr,
        )
        return 2

    return 1 if (shown_critical or shown_warning or total_invisible) else 0


def report_skipped(root, skipped_ext, skipped_binary, checked, check_all):
    """Отчёт о непроверенном. Молчаливого пропуска быть не должно."""
    total = len(skipped_ext) + len(skipped_binary)
    print(f"\nПропущено файлов: {total}")
    if not total:
        return

    print("!" * 78)
    print(f"!!  ВНИМАНИЕ: НЕ ПРОВЕРЕНО ФАЙЛОВ — {total}")
    print(f"!!  Итог выше относится ТОЛЬКО к проверенным файлам: {checked}")
    print("!!  «Проблем не найдено» ≠ «всё проверено».")
    print("!" * 78)

    if skipped_ext:
        by_ext = {}
        for path in skipped_ext:
            by_ext.setdefault(path.suffix.lower() or "(без расширения)", []).append(path)
        summary = ", ".join(f"{ext} × {len(v)}" for ext, v in sorted(by_ext.items()))
        print(f"\nПропущено по расширению: {len(skipped_ext)} — {summary}")
        for path in skipped_ext[:LIST_LIMIT]:
            print(f"    {rel(path, root)}")
        if len(skipped_ext) > LIST_LIMIT:
            print(f"    … ещё {len(skipped_ext) - LIST_LIMIT}")
        if not check_all:
            print("  Проверить их тоже: --all")

    if skipped_binary:
        print(f"\nПропущено как бинарные: {len(skipped_binary)}")
        for path in skipped_binary[:LIST_LIMIT]:
            print(f"    {rel(path, root)}")
        if len(skipped_binary) > LIST_LIMIT:
            print(f"    … ещё {len(skipped_binary) - LIST_LIMIT}")


if __name__ == "__main__":
    sys.exit(main())
