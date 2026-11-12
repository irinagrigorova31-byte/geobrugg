# Hero-бриф — page-08 «Защитные ограждения для автоспорта (FIA)»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: улавливающее ограждение (catch fence) из высокопрочной стальной сети вдоль гоночной трассы поглощает удар и удерживает автомобиль и обломки — «трасса и зрители под защитой».

Текущая обложка (hero) — реальное фото с сайта: `…/wp-content/uploads/2024/04/3.-fia-debris-fence-2021-1-scaled.jpg` (FIA debris fence). Бриф нужен прежде всего для **og:image** (1200×630).

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of a motorsport catch fence — a high-tensile steel wire mesh stretched on posts along the edge of a race circuit run-off area — designed to absorb impact and retain a car and debris. Calm, technical, documentary trackside mood — safety barrier and engineering, not a crash scene or race advertising. Clean composition, the fence line as the clear focal point slightly right of centre, run-off and sky as generous negative space for cropping. Muted palette of asphalt grey, kerb tones and steel, with a deep engineering navy accent (#2b3a8c) in shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента и без узнаваемых реальных трасс/командных ливрей;
- без чужих логотипов, брендов спонсоров и автопроизводителей;
- без людей крупным планом, без гонщиков и болидов конкретных команд;
- не буквальная «авария с огнём и пострадавшими» — тон спокойный, про улавливающее ограждение, а не про крушение.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: линия ограждения крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/motorsport-fia-hero.png`
  - `assets/hero/motorsport-fia-og.png`

## 4. Alt-текст (RU)
Улавливающее ограждение из высокопрочной стальной сети вдоль гоночной трассы, рассчитанное на поглощение удара и удержание автомобиля и обломков. Спокойный инженерный кадр, передающий надёжность защитных ограждений для автоспорта.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-motorsport-fia.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/motorsport-fia-og.png`). Hero остаётся реальным фото FIA debris fence.
