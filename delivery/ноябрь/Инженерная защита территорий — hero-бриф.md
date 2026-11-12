# Hero-бриф — статья «Инженерная защита территорий: принципы, методы и нормативная база»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: инженерная защита территории — склон и объекты инфраструктуры под защитой высокопрочных стальных систем (укреплённый сеткой склон над дорогой/зданиями), спокойный инженерный кадр, а не катастрофа.

Текущая обложка (hero/og) — реальное фото с сайта: `…/wp-content/uploads/2024/12/2017.-sistema-ukrepleniya-sklonov.jpg`. Бриф нужен прежде всего для **og:image** (1200×630) и опционально для уникального hero.

## 1. Prompt (EN, для генератора)
A wide, editorial engineering illustration of territorial protection works: a steep slope above a road and buildings stabilised by a high-tensile steel wire mesh with anchors, with subtle hints of other engineering-protection measures (a catchment barrier, a drainage channel). Calm, technical, documentary mood — infrastructure kept safe by engineering, not a disaster scene. Clean composition, the protected slope as the clear focal point slightly left of centre, sky and valley as generous negative space for cropping. Muted palette of rock grey, vegetation and steel, with a deep engineering navy accent (#2b3a8c) in shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных узнаваемых объектов, логотипов и брендов (своих и чужих);
- без сцен разрушения, жертв, огня и крови — тон спокойный, про защиту, а не про катастрофу;
- не путать тему: это защита территории от природных процессов, а НЕ охрана периметра/СКУД и не защита информации.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: укреплённый склон крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/inzhenernaya-zashchita-territoriy-hero.png`
  - `assets/hero/inzhenernaya-zashchita-territoriy-og.png`

## 4. Alt-текст (RU)
Склон над дорогой и зданиями, укреплённый высокопрочной стальной сеткой с анкерами, — пример инженерной защиты территории от опасных геологических процессов. Спокойный инженерный кадр.

## 5. Пометка для page-builder
В статье hero и `og:image` сейчас указывают на реальное фото `…/2017.-sistema-ukrepleniya-sklonov.jpg`. Готовый PNG/JPG по брифу выложить на боевом сайте и при необходимости заменить путь на `assets/hero/inzhenernaya-zashchita-territoriy-og.png` (1200×630).
