# Hero-бриф — page-07 «Укрепление сводов тоннелей»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: высокопрочная стальная сеть прижата анкерами к своду подземной выработки как поверхностная крепь под набрызг-бетон — «свод держит сеть, порода не вываливается».

Текущая обложка (hero) — реальное фото с сайта: `…/wp-content/uploads/2024/04/7.-minax®-80-3-2018-scaled.jpg` (сеть MINAX® 80/3). Бриф нужен прежде всего для **og:image** (1200×630).

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of the vault of an underground tunnel or mine drift lined with a high-tensile steel wire mesh fixed to the rock by rock bolts and bearing plates, serving as surface support beneath shotcrete; the mesh hugs the irregular rock arch and holds loose rock. Calm, technical, documentary underground mood, lit by cool work lighting — ground support and engineering, not advertising. Clean composition, the meshed vault as the clear focal point, perspective receding into the tunnel, generous negative space for cropping. Muted underground palette of rock grey and dark earth, with a deep engineering navy accent (#2b3a8c) in shadow grading and a single restrained red accent (#e31e24) as a small marker; light negative space where lit (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный смонтированный объект, техника, команда);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без «шахтёра с планшетом»;
- не буквальная «обрушение свода с жертвами» — тон спокойный, про крепь, а не про аварию.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции**: сеть на своде крупно, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG**. Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании знак Геобругг из брендбука в угол; чужие логотипы — нельзя.
- Имена файлов (латиница, по slug):
  - `assets/hero/ukreplenie-svodov-tonnelej-hero.png`
  - `assets/hero/ukreplenie-svodov-tonnelej-og.png`

## 4. Alt-текст (RU)
Свод подземной выработки, укреплённый высокопрочной стальной сетью на анкерах как поверхностная крепь под набрызг-бетон. Спокойный инженерный кадр, передающий надёжность крепи сводов тоннелей и шахт.

## 5. Пометка для page-builder
В странице уже стоит `<meta property="og:image">` на путь **`…/wp-content/uploads/og-tunneli.jpg`** (1200×630). Готовый PNG/JPG по брифу выложить по этому пути на боевом сайте (либо заменить путь на `assets/hero/ukreplenie-svodov-tonnelej-og.png`). Hero остаётся реальным фото сети MINAX® 80/3.
