# Hero-бриф — page-02 «Защита от селей»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: гибкий стальной барьер поперёк горного русла задерживает селевую массу и пропускает воду — «инженерная защита гасит селевой поток».

Текущая обложка страницы (hero) — реальное фото с сайта: `…/wp-content/uploads/2024/04/11.-ux180-h6-2013-scaled.jpg` (барьер UX®). Бриф нужен прежде всего для **og:image** (1200×630), а также как опция для кастомной обложки.

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of a flexible high-tensile steel ring-net debris-flow barrier spanning a steep mountain gully; the net bulges as it retains boulders, mud and woody debris while clear water drains through the mesh. Calm, technical, documentary mood — containment and engineering, not disaster. Clean composition with the barrier as the clear focal point slightly right of centre, generous negative space for cropping. Muted natural palette of rock grey, wet earth and water tones, with a deep engineering navy accent (#2b3a8c) in shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный смонтированный объект Геобругг, техника, команда);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без «строителя с планшетом»;
- не буквальная «катастрофа с жертвами, затопленный посёлок» — тон спокойный, про удержание потока, а не про бедствие.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции, не растягивать hero**: барьер в русле крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании наложить знак Геобругг из брендбука (пиксель-в-пиксель) в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/zashchita-ot-selej-hero.png`
  - `assets/hero/zashchita-ot-selej-og.png`

## 4. Alt-текст (RU)
Гибкий стальной барьер поперёк горного русла задерживает селевую массу и обломки, пропуская воду сквозь сетку. Спокойный инженерный кадр, передающий надёжность защиты от селевых потоков.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-seli.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/zashchita-ot-selej-og.png`, если складываем в репозиторий). Hero остаётся реальным фото барьера UX®.
