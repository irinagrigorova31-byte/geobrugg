# Hero-бриф — page-03 «Защита от снежных лавин»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: ряды снегоудерживающих барьеров/сеток в зоне зарождения лавины удерживают снежный покров на крутом склоне — «снег остаётся в очаге, лавина не сходит».

Текущая обложка (hero) — реальное фото с сайта: `…/wp-content/uploads/2024/04/9.-spider®-avalanche-2018-scaled.jpg` (SPIDER® Avalanche). Бриф нужен прежде всего для **og:image** (1200×630).

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of rows of flexible steel snow-retention barriers and nets installed across a high alpine starting zone, holding the snowpack in place on a steep slope above a valley. Calm, technical, documentary winter mood — prevention and engineering, not avalanche drama. Clean composition, the barrier line as the clear focal point slightly right of centre, generous negative space of open snow and sky for cropping. Muted winter palette of snow white, rock grey and cold blue shadow, with a deep engineering navy accent (#2b3a8c) in the shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный смонтированный объект, техника, команда);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без лыжников/сноубордистов и курортного глянца;
- не буквальная «сходящая лавина накрывает людей» — тон спокойный, про удержание снега, а не про бедствие.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: линия барьеров на склоне крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/zashchita-ot-lavin-hero.png`
  - `assets/hero/zashchita-ot-lavin-og.png`

## 4. Alt-текст (RU)
Ряды снегоудерживающих барьеров в зоне зарождения лавины удерживают снежный покров на крутом склоне. Спокойный зимний инженерный кадр, передающий надёжность противолавинной защиты.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-laviny.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/zashchita-ot-lavin-og.png`). Hero остаётся реальным фото SPIDER® Avalanche.
