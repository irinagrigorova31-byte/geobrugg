# Hero-бриф — page-01 «Противооползневая защита»

Источник стиля: `input/brand.md` (дизайн-система Геобругг). Метафора: устойчивый горный склон, удержанный гибкой стальной сеткой, — «инженерная защита держит склон».

## 1. Prompt (EN, для генератора)

A wide, editorial engineering illustration of a steep mountain slope stabilized by a high-tensile steel wire mesh net anchored to the rockface; the mesh follows the terrain and holds soil and loose rock in place. Calm, technical, documentary mood — safety and engineering, not advertising. Clean composition with open sky, the protected slope as the clear focal point slightly right of centre, generous negative space around it for cropping. Muted natural palette of rock grey and earth tones, with a deep engineering navy accent (#2b3a8c) in sky/shadow grading and a single restrained red accent (#e31e24) as a small marker; white/light negative space (#ffffff). Flat-realistic illustration with subtle depth, precise linework, no glossy gradients. Horizontal 16:9 framing.

## 2. Negative prompt (чего быть НЕ должно)
- без текста и надписей на изображении;
- без стоковых клише: рукопожатия, лампочки, безликие человечки, glow-градиенты «как у всех»;
- без реальных объектов клиента (конкретный офис, техника, команда, реальный смонтированный объект Геобругг);
- без чужих логотипов и брендов конкурентов;
- без людей крупным планом, без касок-стокового «строителя с планшетом»;
- не буквальная «катастрофа/обвал с жертвами» — тон спокойный, про защиту, а не про бедствие.

## 3. Техтребования исполнителю (RU)
- Нужны два кадра: **hero** (широкая обложка страницы) и **og:image ровно 1200×630 px**.
- og:image **кадрировать из композиции, не растягивать hero**: главный элемент (склон под сеткой) крупно, минимум деталей, узнаётся в ленте на ширине ~300px.
- Формат — **PNG или JPG, не SVG** (соцсети SVG в превью не рендерят). Вес og:image — **до 300 КБ**.
- Палитра — из дизайн-системы: фон/светлое `#ffffff`, инженерный синий `#2b3a8c`, тёмный `#141414`, красный `#e31e24` — только точечным акцентом.
- **Логотип:** при желании наложить свой знак Геобругг из `assets/brand/` (пиксель-в-пиксель, без искажений) в угол; чужие логотипы — нельзя. Логотипов в `assets/brand/` сейчас нет — если понадобится оверлей, взять из брендбука.
- Имена файлов (латиница, по slug статьи):
  - `assets/hero/protivoopolznevaya-zashchita-hero.png`
  - `assets/hero/protivoopolznevaya-zashchita-og.png`

## 4. Alt-текст (RU)
Горный склон, укреплённый гибкой стальной сеткой на анкерах: сетка повторяет рельеф и удерживает грунт и породу. Спокойный инженерный кадр, передающий надёжность защиты от оползней.

## 5. Пометка для page-builder
og:image ляжет по пути: **`assets/hero/protivoopolznevaya-zashchita-og.png`** (1200×630, PNG). Вёрстка ставит `<meta property="og:image">` на этот путь заранее; PNG человек догенерит по брифу позже.
