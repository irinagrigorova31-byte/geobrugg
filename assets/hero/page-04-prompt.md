# Hero-бриф — page-04 «Защита от камнепадов»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: динамический барьер из высокопрочной стальной сети на опорах улавливает падающий с откоса блок и гасит его энергию — «удар принят, объект под защитой».

Текущая обложка (hero) — реальное фото с сайта: `…/wp-content/uploads/2024/04/2.-rxe-2022-scaled.jpg` (барьер RXE®). Бриф нужен прежде всего для **og:image** (1200×630).

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of a dynamic rockfall protection barrier — a high-tensile steel ring/wire net stretched between steel posts with brake elements and anchors on a rocky slope — catching a falling boulder and absorbing its impact energy, the net deforming into a shallow pocket. Calm, technical, documentary mood — protection and engineering, not disaster. Clean composition, the barrier and caught boulder as the clear focal point slightly right of centre, generous negative space for cropping. Muted natural palette of rock grey and earth tones, with a deep engineering navy accent (#2b3a8c) in sky/shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный смонтированный объект, техника, команда);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без «строителя с планшетом»;
- не буквальная «камнепад убивает людей / разбитые машины» — тон спокойный, про улавливание, а не про бедствие.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: барьер с уловленным блоком крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/zashchita-ot-kamnepadov-hero.png`
  - `assets/hero/zashchita-ot-kamnepadov-og.png`

## 4. Alt-текст (RU)
Динамический барьер из высокопрочной стальной сети на опорах улавливает падающий блок скальной породы и гасит энергию удара. Спокойный инженерный кадр, передающий надёжность защиты от камнепадов.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-kamnepad-obval.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/zashchita-ot-kamnepadov-og.png`). Hero остаётся реальным фото барьера RXE®.
