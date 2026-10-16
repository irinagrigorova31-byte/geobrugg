# Hero-бриф — page-05 «Защита склонов от эрозии»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: тонкая высокопрочная стальная сеть вместе с противоэрозионным матом прижимает поверхность откоса, сквозь неё пробивается молодая зелень — «склон закреплён и зарастает».

Текущая обложка (hero) — реальное фото с сайта (укреплённая насыпь, Мирафлорес). Бриф нужен прежде всего для **og:image** (1200×630).

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of a graded road or railway embankment surfaced with a thin high-tensile steel wire mesh over a three-dimensional erosion-control mat pinned by toothed plates and anchors; fresh green vegetation grows up through the mesh, stabilizing the soil. Calm, technical, documentary mood — stabilization and greening, not advertising. Clean composition, the meshed slope as the clear focal point slightly right of centre, generous negative space of sky for cropping. Muted natural palette of earth brown, rock grey and soft green, with a deep engineering navy accent (#2b3a8c) in shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный смонтированный объект, техника, команда);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без «строителя с планшетом»;
- не буквальная «оплывший размытый склон с жертвами» — тон спокойный, про закрепление и озеленение.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: укреплённый зарастающий откос крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/zashchita-ot-erozii-hero.png`
  - `assets/hero/zashchita-ot-erozii-og.png`

## 4. Alt-текст (RU)
Откос, закреплённый тонкой высокопрочной стальной сетью поверх противоэрозионного мата; сквозь сетку пробивается молодая зелень. Спокойный инженерный кадр, передающий защиту склона от эрозии и его озеленение.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-zashchita-ot-erozii.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/zashchita-ot-erozii-og.png`). Hero остаётся реальным фото укреплённой насыпи.
