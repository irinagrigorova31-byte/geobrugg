---
description: Off-site ветка, шаг 2 — тексты под площадки. external-tz-writer → external-copywriter (волнами) → external-gist-auditor (петля) → homoglyph → external/.
---

Выполни ШАГ ПИСЬМА off-site-ветки. Аргументы: $ARGUMENTS

Предусловия:
1. Есть `data/placement-plan.md` (утверждён на воротах /tripl-ext-plan)?
2. Для каждой целевой площадки есть скилл `.claude/skills/external-<platform>/SKILL.md` с ПРАВИЛАМИ площадки?
   Если скилл пустой (шаблон external-PLATFORM) или отсутствует — ПОКАЖИ это как блокер: правила площадки задаёт
   владелец (pluggable-слот). Без них external-tz-writer/copywriter оставят требования площадки заглушкой
   `[ТРЕБУЕТСЯ: правила площадки <platform>]`, а не выдумают.
3. Проектный скилл ниши project-<slug> и humanizer на месте.

Порядок (по каждому размещению из placement-plan.md):
1. **external-tz-writer** → `data/tz-ext/tz-NN.md`: площадка + её формат/TOS (из external-<platform>), какой
   цитируемый факт засеять (own + статус верификации), политика бэклинка, disclosure/авторство, требования
   извлекаемости/атрибуции. БЕЗ силоса/JSON-LD/меты/витрины.
2. **external-copywriter** ВОЛНАМИ по 2-3 (не залпом; лимиты API) → тексты в `external/`. Грузит humanizer +
   project-<slug> + external-<platform>. Выход И `.md`, И HTML-фрагмент (по параметру в ТЗ). Downstream on-site пропускает.
3. **external-gist-auditor** по каждому тексту → `review/audit-ext-NN.md`. Петля правок ≤3: III-6 + off-site-проверки
   (цитируемость, атрибуция бренду, TOS-безопасность/нет самопиара, disclosure, бэклинк-политика).
4. **homoglyph-checker** по `external/` — финальный техчек текста.

Правила ведения — как в on-site: после каждого этапа проверяй файлы; упал агент — один повтор; волнами; заглушки
`[ТРЕБУЕТСЯ]` не выдумывать. В конце — сводка: сколько размещений написано/прошло аудит, где открытые заглушки
(правила площадки / данные клиента), что осталось.
