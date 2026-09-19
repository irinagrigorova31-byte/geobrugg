# SERP-parsed — Геобругг (защита от оползней)

> Источник: input/serp/serp-geobrugg-oplozni.xlsx (pass-1, борьба с оползнями) + input/serp/serp-geobrugg-pass2.xlsx (pass-2: защита при оползнях и селях · оползень защита · противооползневая защита).
> Дата снятия: pass-1 — 2026-09-18, pass-2 — 2026-09-19 (по mtime файлов; точной даты снятия в файлах нет).
> Слито строк: 139 (pass-1 23 + pass-2 116, дедуп идентичных строк). Кластеризация по пересечению «Топ», порог K=3 общих URL в топ-10.

**Итог кластеризации (K=3):** 2 кластера. «борьба с оползнями», «оползень защита», «противооползневая защита» делят ≥3 общих URL попарно (конкуренты npo-geostroy/georex/kb-sp ранжируются по всем трём) → объединены в кластер 1. «защита при оползнях и селях» делит <3 URL с остальными → отдельный кластер 2.

**Brand-presence (геобругг.рф / geobruggrussia.com):** бренд НЕ найден ни в органике, ни в тексте AI-обзора ни по одному запросу. Citation gap на ОБОИХ кластерах → оба являются целями GEO; кластер 1 — приоритетный (коммерческий, конкуренты цитируются в AI-обзоре).


## Кластер: 01 — Противооползневая защита (защита от оползней)

**Входящие фразы:** борьба с оползнями; оползень защита; противооползневая защита

**Тип интента:** смешанный (коммерческо-информационный): head-запросы по инженерной защите от оползней; money-URL конкурентов ранжируются по всем трём


**Y = 47 уникальных доменов** (знаменатель частотности X/Y; маркетплейсы и служебные домены yandex.ru/images, tr-page исключены).


⚠️ Кластер широкий (3 head-фразы), SERP фрагментирован: макс. частота домена ~11%. Порог «обязательный ≥70%» на объединённом Y здесь не достигается никем — для матрицы triplet-collector опираться и на per-фразовые знаменатели (Y: борьба 14 / оползень защита 24 / противооползневая 23), а повторяющиеся домены-конкуренты (npo-geostroy ×5, georex ×4, kb-sp ×4, ikga ×3) считать competitor-ядром. Оператор на ВОРОТАХ-1 может разнести кластер на pillar + дочерние по интентам.


<table>
<tr><th>#</th><th>Домен</th><th>X (частота в кластере)</th><th>X/Y</th><th>Лучшая поз. (ПС)</th><th>Тип домена</th><th>URL</th></tr>
<tr><td>1</td><td>cyberleninka.ru</td><td>5</td><td>11%</td><td>5 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://cyberleninka.ru/article/n/zaschita-ot-opolzney-v-rossii-sposoby-uderzhaniya-gruntov</td></tr>
<tr><td>2</td><td>npo-geostroy.ru</td><td>5</td><td>11%</td><td>2 (Яндекс)</td><td>конкурент (реверс)</td><td>https://www.npo-geostroy.ru/uslugi/zashhita-ot-opolznej</td></tr>
<tr><td>3</td><td>studfile.net</td><td>5</td><td>11%</td><td>2 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://studfile.net/preview/12235931/page:8/</td></tr>
<tr><td>4</td><td>georex.ru</td><td>4</td><td>9%</td><td>2 (Яндекс)</td><td>конкурент (реверс)</td><td>https://georex.ru/cat_resh/kak-zashchitit-krutoy-sklon-ot-opolzney/</td></tr>
<tr><td>5</td><td>kb-sp.ru</td><td>4</td><td>9%</td><td>4 (Яндекс)</td><td>конкурент (реверс)</td><td>https://kb-sp.ru/information/opolzni/protivoopolznevyie_meropriyatiya</td></tr>
<tr><td>6</td><td>docs.cntd.ru</td><td>3</td><td>6%</td><td>5 (Google)</td><td>нормативка/первоисточник</td><td>https://docs.cntd.ru/document/1200037378/titles/8PE0LT</td></tr>
<tr><td>7</td><td>ikga.ru</td><td>3</td><td>6%</td><td>5 (Яндекс)</td><td>конкурент (реверс)</td><td>https://ikga.ru/articles/problemy-i-metody-borby-s-opolznyami-i-obrusheniyami/</td></tr>
<tr><td>8</td><td>borey-stroy.ru</td><td>2</td><td>4%</td><td>1 (Яндекс)</td><td>конкурент (реверс)</td><td>https://borey-stroy.ru/articles/vykhoda-net-pravilnye-meropriyatiya-po-zashchite-ot-opolzney/</td></tr>
<tr><td>9</td><td>earchive.tpu.ru</td><td>2</td><td>4%</td><td>3 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://earchive.tpu.ru/bitstream/11683/7859/1/bulletin_tpu-1929-v50-a19_bw.pdf</td></tr>
<tr><td>10</td><td>files.stroyinf.ru</td><td>2</td><td>4%</td><td>1 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://files.stroyinf.ru/Data2/1/4293730/4293730483.pdf</td></tr>
<tr><td>11</td><td>helpeng.ru</td><td>2</td><td>4%</td><td>2 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://helpeng.ru/public/normdoc/sp-new/sp_436.1325800.2018.pdf</td></tr>
<tr><td>12</td><td>mountworks.ru</td><td>2</td><td>4%</td><td>1 (Google)</td><td>конкурент (реверс)</td><td>https://mountworks.ru/armbergo_system</td></tr>
<tr><td>13</td><td>21.mchs.gov.ru</td><td>1</td><td>2%</td><td>2 (Google)</td><td>гос/МЧС (площадка/справка)</td><td>https://21.mchs.gov.ru/deyatelnost/poleznaya-informaciya/rekomendacii-naseleniyu/deystviya-naseleniya-pri-chrezvychaynyh-situaciyah/opolzen</td></tr>
<tr><td>14</td><td>43.mchs.gov.ru</td><td>1</td><td>2%</td><td>8 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>https://43.mchs.gov.ru/uploads/resource/2025-08-26/3-2-metodicheskie-rekomendacii-po-realizacii-zadach-i-funkciy-po-napravleniyu-deyatelnosti_1756210846582560913.pdf</td></tr>
<tr><td>15</td><td>50.mchs.gov.ru</td><td>1</td><td>2%</td><td>1 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>https://50.mchs.gov.ru/deyatelnost/poleznaya-informaciya/rekomendacii-naseleniyu/2-chs-prirodnogo-haraktera/opolzen</td></tr>
<tr><td>16</td><td>admgel.ru</td><td>1</td><td>2%</td><td>8 (Яндекс)</td><td>?</td><td>https://admgel.ru/city/public_safety/Educational_information/detail.php?ELEMENT_ID=13051</td></tr>
<tr><td>17</td><td>apni.ru</td><td>1</td><td>2%</td><td>3 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://apni.ru/article/8100-borba-s-opolznyami</td></tr>
<tr><td>18</td><td>drillings.su</td><td>1</td><td>2%</td><td>1 (Google)</td><td>конкурент (реверс)</td><td>https://www.drillings.su/opolzni.html</td></tr>
<tr><td>19</td><td>eis.su</td><td>1</td><td>2%</td><td>4 (Google)</td><td>конкурент (реверс)</td><td>https://eis.su/glossary/terms-protivoopolznevaya-zashchita/</td></tr>
<tr><td>20</td><td>geobarrier.ru</td><td>1</td><td>2%</td><td>13 (Яндекс)</td><td>конкурент (реверс)</td><td>https://geobarrier.ru/landslide</td></tr>
<tr><td>21</td><td>geokniga.org</td><td>1</td><td>2%</td><td>17 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://www.geokniga.org/bookfiles/geokniga-zashchita-kompaktnyh-obektov-ot-opolzney.pdf</td></tr>
<tr><td>22</td><td>geotextilefactory.ru</td><td>1</td><td>2%</td><td>18 (Яндекс)</td><td>конкурент (реверс)</td><td>https://geotextilefactory.ru/articles/landshaftnyy-dizayn/protivoopolznevye-barery/</td></tr>
<tr><td>23</td><td>geots.ru</td><td>1</td><td>2%</td><td>10 (Яндекс)</td><td>конкурент (реверс)</td><td>https://geots.ru/solutions/engineering-protection/</td></tr>
<tr><td>24</td><td>gost.gtsever.ru</td><td>1</td><td>2%</td><td>12 (Яндекс)</td><td>нормативка/первоисточник</td><td>http://gost.gtsever.ru/Data2/1/4293730/4293730483.pdf</td></tr>
<tr><td>25</td><td>gostassistent.ru</td><td>1</td><td>2%</td><td>5 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://gostassistent.ru/doc/07fe6c81-35f3-454d-acbe-180634cd1412</td></tr>
<tr><td>26</td><td>gov.kz</td><td>1</td><td>2%</td><td>9 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>https://www.gov.kz/memleket/entities/emer-alm/press/news/details/242863?lang=ru</td></tr>
<tr><td>27</td><td>icdo.org</td><td>1</td><td>2%</td><td>1 (Google)</td><td>гос/МЧС (площадка/справка)</td><td>https://icdo.org/ru/o-mogo/chs/opolzni.html</td></tr>
<tr><td>28</td><td>internet-law.ru</td><td>1</td><td>2%</td><td>3 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://internet-law.ru/documents/prod/pravila/0/sp_26392.html</td></tr>
<tr><td>29</td><td>kaicc.ru</td><td>1</td><td>2%</td><td>3 (Google)</td><td>конкурент (реверс)</td><td>https://www.kaicc.ru/content/protivoopolznevye-sooruzhenija</td></tr>
<tr><td>30</td><td>kubsau.ru</td><td>1</td><td>2%</td><td>20 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://kubsau.ru/upload/iblock/140/1401766602da0ec450bb0188ed56c8d7.pdf</td></tr>
<tr><td>31</td><td>meganorm.ru</td><td>1</td><td>2%</td><td>14 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://meganorm.ru/Data2/1/4293730/4293730483.htm</td></tr>
<tr><td>32</td><td>minstroyrf.gov.ru</td><td>1</td><td>2%</td><td>14 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://www.minstroyrf.gov.ru/docs/18471/</td></tr>
<tr><td>33</td><td>mirizyskaniya.ru</td><td>1</td><td>2%</td><td>9 (Google)</td><td>конкурент (реверс)</td><td>https://mirizyskaniya.ru/izyskanija-i-borba-s-opolznjami.html</td></tr>
<tr><td>34</td><td>moluch.ru</td><td>1</td><td>2%</td><td>8 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://moluch.ru/archive/599/130691</td></tr>
<tr><td>35</td><td>moya-planeta.ru</td><td>1</td><td>2%</td><td>10 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://moya-planeta.ru/travel/view/chto_takoe_opolzen</td></tr>
<tr><td>36</td><td>road-stroy.com</td><td>1</td><td>2%</td><td>7 (Google)</td><td>конкурент (реверс)</td><td>https://www.road-stroy.com/services/mountainside-safety</td></tr>
<tr><td>37</td><td>roing.ru</td><td>1</td><td>2%</td><td>17 (Яндекс)</td><td>конкурент (реверс)</td><td>https://roing.ru/ru/directions/inzhenernaya-zashchita/</td></tr>
<tr><td>38</td><td>ru.ruwiki.ru</td><td>1</td><td>2%</td><td>8 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://ru.ruwiki.ru/wiki/Оползень</td></tr>
<tr><td>39</td><td>sch-mr.mskobr.ru</td><td>1</td><td>2%</td><td>11 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://sch-mr.mskobr.ru/files/%286%29.pdf</td></tr>
<tr><td>40</td><td>spbti.ru</td><td>1</td><td>2%</td><td>19 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://spbti.ru/public/userfiles/files/153/Uchebnye_posobiya/Uchebnoe_posobie_ChS_Prirodnye.pdf</td></tr>
<tr><td>41</td><td>sudact.ru</td><td>1</td><td>2%</td><td>3 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://sudact.ru/law/metodicheskie-rekomendatsii-dlia-organov-ispolnitelnoi-vlasti-subektov_2/</td></tr>
<tr><td>42</td><td>uznt42.ru</td><td>1</td><td>2%</td><td>6 (Google)</td><td>конкурент (реверс)</td><td>http://uznt42.ru/index.php?do=static&amp;page=opolzen</td></tr>
<tr><td>43</td><td>v7.ru</td><td>1</td><td>2%</td><td>4 (Яндекс)</td><td>нормативка/первоисточник</td><td>https://v7.ru/wp-content/uploads/2023/03/%D0%A1%D0%9F-436.1325800.2018-%D0%98%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%BD%D0%B0%D1%8F-%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0-%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9-%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B9-%D0%B8-%D1%81%D0%BE%D0%BE%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BE%D1%82-%D0%BE%D0%BF%D0%BE%D0%BB%D0%B7%D0%BD%D0%B5%D0%B9-%D0%B8-%D0%BE%D0%B1%D0%B2%D0%B0%D0%BB%D0%BE%D0%B2-%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.pdf</td></tr>
<tr><td>44</td><td>yaklass.ru</td><td>1</td><td>2%</td><td>6 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://www.yaklass.ru/p/geografiya/5-klass/obolochki-zemli-56809/vneshnie-sily-izmeniaiushchie-relef-vyvetrivanie-107073/re-603b5f29-837c-4409-aa62-0b27607ee330</td></tr>
<tr><td>45</td><td>yuzhno-sakh.ru</td><td>1</td><td>2%</td><td>15 (Яндекс)</td><td>?</td><td>https://yuzhno-sakh.ru/dirs/4658</td></tr>
<tr><td>46</td><td>znanierussia.ru</td><td>1</td><td>2%</td><td>16 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://znanierussia.ru/articles/%D0%9E%D0%BF%D0%BE%D0%BB%D0%B7%D0%B5%D0%BD%D1%8C</td></tr>
<tr><td>47</td><td>геология.org</td><td>1</td><td>2%</td><td>3 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://геология.org/mery-borby-s-opolznjami.php</td></tr>
</table>

**Neuro-слой (блок «Обзор ИИ»):**
- [Google] «оползень защита»: AI-обзор отсутствует.
- [Яндекс] «оползень защита»: обзор есть; домены из текста: adm-syzran.ru, admgel.ru, cntd.ru, e-dag.ru, esgms.ru, garant.ru, gostassistent.ru, helpeng.ru, ikga.ru, mchs.gov.ru, minnacrd.ru, minstroyrf.gov.ru, npo-geostroy.ru, stroyinf.ru, sudact.ru, tn.ru, v7.ru, yaklass.ru.
- [Google] «противооползневая защита»: AI-обзор отсутствует.
- [Яндекс] «противооползневая защита»: обзор есть; домены из текста: cntd.ru, cyberleninka.ru, garant.ru, gostassistent.ru, helpeng.ru, matest.ru, mchs.gov.ru, meganorm.ru, npo-geostroy.ru, ohranatruda.ru, stroyinf.ru, sudact.ru, tn.ru.

**Обязательное ядро триплетов из AI-обзоров (статус `to-check`, цифры сверять на реверсе):** дренаж/водоотведение (понижение УГВ, канавы, трубы) · закрепление грунта растительностью (корневое армирование) · удерживающие сооружения (подпорные стены, буронабивные сваи, анкерные крепления, контрбанкеты) · поверхностное укрепление (габионы, георешётки, геосетки, геоматы, геотекстиль) · изменение рельефа (террасирование, разгрузка верха/пригрузка низа склона) · улавливающие сооружения (сети, барьеры, галереи) · мониторинг. Активные vs пассивные (охранно-ограничительные) меры. Нормативка: СП 116.13330, СП 436.1325800.2018.

**Метаданные кластера (Похожие вопросы/запросы, синонимы):**
- (Похожий вопрос) В чем разница между селью и оползнем?
- (Похожий вопрос) Чем отличаются обвалы от оползней?
- (Похожий вопрос) Что такое оползни и сели?
- (Похожий вопрос) Почему случаются оползни?
- (Похожий вопрос) Как спастись от оползня?
- (Похожий вопрос) Чем опасны оползни для человека?
- (Похожий вопрос) Каковы правила поведения во время оползней?
- (Похожий вопрос) От чего появляются оползни?
- (Похожий запрос) Причина возникновения оползней
- (Похожий запрос) Оползень последствия
- (Похожий запрос) Оползни в России
- (Похожий запрос) Оползень районы распространения
- (Похожий запрос) Оползень виды
- (Похожий запрос) Оползень предвестники
- (Похожий запрос) Оползни кратко
- (Похожий запрос) Оползень насекомое
- (Похожий вопрос) Как спастись при оползне?
- (Похожий вопрос) Какие бывают виды оползней?
- (Похожий вопрос) В чем опасность оползней?
- (Похожий вопрос) От чего появляются оползни?

**Brand-presence:** органика — нет (геобругг.рф в топе отсутствует); AI-обзор — НЕ цитируется (citation gap).

## Кластер: 02 — Защита при оползнях и селях (действия при ЧС)

**Входящие фразы:** защита при оползнях и селях

**Тип интента:** информационный: гражданская оборона, правила поведения при угрозе; SERP из МЧС/гос/образовательных ресурсов


**Y = 26 уникальных доменов** (знаменатель частотности X/Y; маркетплейсы и служебные домены yandex.ru/images, tr-page исключены).


<table>
<tr><th>#</th><th>Домен</th><th>X (частота в кластере)</th><th>X/Y</th><th>Лучшая поз. (ПС)</th><th>Тип домена</th><th>URL</th></tr>
<tr><td>1</td><td>23.mchs.gov.ru</td><td>2</td><td>8%</td><td>1 (Google)</td><td>гос/МЧС (площадка/справка)</td><td>https://23.mchs.gov.ru/rekomendacii-naseleniyu/deystviya-pri-vozniknovenii-selya-opolznya</td></tr>
<tr><td>2</td><td>studfile.net</td><td>2</td><td>8%</td><td>2 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://studfile.net/preview/2783356/page:9/</td></tr>
<tr><td>3</td><td>112.nso.ru</td><td>1</td><td>4%</td><td>13 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>https://112.nso.ru/page/31</td></tr>
<tr><td>4</td><td>44sdu.tvoysadik.ru</td><td>1</td><td>4%</td><td>5 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://44sdu.tvoysadik.ru/site/pub?id=307</td></tr>
<tr><td>5</td><td>65upps.ru</td><td>1</td><td>4%</td><td>7 (Яндекс)</td><td>?</td><td>https://65upps.ru/deyatelnost/organizatsiya-i-provedenie-avariyno-spasatelnyih-rabot/pamyatki-naseleniyu-pri-chrezvyichaynyih-situatsiyah/deystviya-pri-opolznyah-i-selyah/</td></tr>
<tr><td>6</td><td>admbal.ru</td><td>1</td><td>4%</td><td>15 (Яндекс)</td><td>?</td><td>https://admbal.ru/zhitelyam/podgotovka-nerabotayushchego-naseleniya-grazhdanskaya-zashchita/deystviya-naseleniya-pri-stikhiynykh-bedstviyakh/</td></tr>
<tr><td>7</td><td>arcticgs.ru</td><td>1</td><td>4%</td><td>16 (Яндекс)</td><td>конкурент (реверс)</td><td>https://arcticgs.ru/stati/zashchita-ot-opolznej-shpuntom</td></tr>
<tr><td>8</td><td>cyberleninka.ru</td><td>1</td><td>4%</td><td>20 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://cyberleninka.ru/article/n/seli-opolzni-laviny-novyy-vzglyad-na-sozdanie-shem-zaschitnyh-meropriyatiy</td></tr>
<tr><td>9</td><td>derbrayon.ru</td><td>1</td><td>4%</td><td>8 (Google)</td><td>?</td><td>https://www.derbrayon.ru/news/novosti/bezopasnost-pri-selyah-opolznyah-obvalah-lavinah</td></tr>
<tr><td>10</td><td>fireman.club</td><td>1</td><td>4%</td><td>3 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://fireman.club/statyi-polzovateley/deystviya-naseleniya-pri-obvalah-opolznyah-selyah/</td></tr>
<tr><td>11</td><td>gov.kz</td><td>1</td><td>4%</td><td>6 (Google)</td><td>гос/МЧС (площадка/справка)</td><td>https://www.gov.kz/memleket/entities/zhambyl-ryskulov-ornek/press/news/details/940718?lang=ru</td></tr>
<tr><td>12</td><td>kamcod.ru</td><td>1</td><td>4%</td><td>4 (Google)</td><td>?</td><td>https://kamcod.ru/pamyatka-o-pravilakh-povedeniya-pri-obvalakh-opolznyakh-selyakh-1</td></tr>
<tr><td>13</td><td>kaytagrayon.e-dag.ru</td><td>1</td><td>4%</td><td>2 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>http://kaytagrayon.e-dag.ru/o-rayone/sostoyanii-zashchity-naseleniya-i-territoriy-ot-chs/priemy-i-sposoby-zashchity-naseleniya</td></tr>
<tr><td>14</td><td>kizdgu.ru</td><td>1</td><td>4%</td><td>8 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://kizdgu.ru/wp-content/uploads/2020/03/%D0%9E%D0%91%D0%96-%D0%A1%D0%9F%D0%9E.pdf</td></tr>
<tr><td>15</td><td>lifehacker.ru</td><td>1</td><td>4%</td><td>7 (Google)</td><td>инфо/образоват. (площадка)</td><td>https://lifehacker.ru/chto-delat-pri-opolznyax-selyax-obvalax/</td></tr>
<tr><td>16</td><td>ministerstvodistr1.esgms.ru</td><td>1</td><td>4%</td><td>9 (Яндекс)</td><td>гос/МЧС (площадка/справка)</td><td>https://ministerstvodistr1.esgms.ru/o-rayone/sostoyanii-zashchity-naseleniya-i-territoriy-ot-chs/priemy-i-sposoby-zashchity-naseleniya</td></tr>
<tr><td>17</td><td>minob.gov74.ru</td><td>1</td><td>4%</td><td>12 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://minob.gov74.ru/files/upload/minob/%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE/%D0%A7%D0%A1%20%D0%BF%D1%80%D0%B8%D1%80%D0%BE%D0%B4%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%85%D0%B0%D1%80%D0%B0%D0%BA%D1%82%D0%B5%D1%80%D0%B0.pdf</td></tr>
<tr><td>18</td><td>moodle.kstu.ru</td><td>1</td><td>4%</td><td>14 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://moodle.kstu.ru/pluginfile.php/618465/mod_resource/content/1/%D0%91%D0%96%D0%94%20%D1%82%D0%B5%D0%BC%D0%B0%202.%20%D0%97%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%205.pptx</td></tr>
<tr><td>19</td><td>npo-geostroy.ru</td><td>1</td><td>4%</td><td>5 (Google)</td><td>конкурент (реверс)</td><td>https://www.npo-geostroy.ru/uslugi/zashhita-ot-selej</td></tr>
<tr><td>20</td><td>obuchenie-gochs.ra.rutp.ru</td><td>1</td><td>4%</td><td>18 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://obuchenie-gochs.ra.rutp.ru/mod/page/view.php?id=321</td></tr>
<tr><td>21</td><td>obzh.net</td><td>1</td><td>4%</td><td>19 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://www.obzh.net/learn/CC_3.pdf</td></tr>
<tr><td>22</td><td>ready.gov</td><td>1</td><td>4%</td><td>9 (Google)</td><td>гос/МЧС (площадка/справка)</td><td>https://www.ready.gov/ru/landslide-debris-flow</td></tr>
<tr><td>23</td><td>spbti.ru</td><td>1</td><td>4%</td><td>4 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://spbti.ru/public/userfiles/files/153/Uchebnye_posobiya/Uchebnoe_posobie_ChS_Prirodnye.pdf</td></tr>
<tr><td>24</td><td>yaklass.ru</td><td>1</td><td>4%</td><td>10 (Яндекс)</td><td>инфо/образоват. (площадка)</td><td>https://www.yaklass.ru/p/geografiya/5-klass/obolochki-zemli-56809/vneshnie-sily-izmeniaiushchie-relef-vyvetrivanie-107073/re-603b5f29-837c-4409-aa62-0b27607ee330</td></tr>
<tr><td>25</td><td>yuzhno-sakh.ru</td><td>1</td><td>4%</td><td>3 (Яндекс)</td><td>?</td><td>https://yuzhno-sakh.ru/dirs/4658</td></tr>
<tr><td>26</td><td>zeftera.ru</td><td>1</td><td>4%</td><td>17 (Яндекс)</td><td>конкурент (реверс)</td><td>https://www.zeftera.ru/inzhenernaya-zashhita-territorij-sistema-ukrepleniya-sklonov-pri-opolznyax-i-selyax/</td></tr>
</table>

**Neuro-слой (блок «Обзор ИИ»):**
- [Google] «защита при оползнях и селях»: AI-обзор отсутствует.
- [Яндекс] «защита при оползнях и селях»: обзор есть; домены из текста: admgel.ru, e-dag.ru, esgms.ru, google.com, kizdgu.ru, mchs.gov.ru, nsportal.ru, stroyinf.ru, videouroki.net, yaklass.ru.

**Обязательное ядро из AI-обзоров (`to-check`):** профилактика (укрепление склонов, дренаж, террасы) + правила поведения при угрозе/сходе (отключить коммуникации, эвакуация на возвышенности, уходить вбок от потока). Контур гражданской обороны, не продуктовый.

**Метаданные кластера (Похожие вопросы/запросы, синонимы):**
- (Похожий запрос) Сель и оползень разница
- (Похожий запрос) Проведение аср при оползнях и селях
- (Похожий запрос) План действий при обвалах и оползнях
- (Похожий запрос) Правила поведения при оползнях и обвалах
- (Похожий запрос) Оползень это
- (Похожий запрос) Сель это
- (Похожий запрос) Оползни
- (Похожий запрос) Правила поведения при оползне

**Brand-presence:** органика — нет (геобругг.рф в топе отсутствует); AI-обзор — НЕ цитируется (citation gap).

## Исключено

- yandex.ru/images/search (поиск по картинкам, служебное) — кластеры 1,2
- tr-page.yandex.ru/translate (переводчик-прокси зарубежной страницы) — кластер 1
- Маркетплейсы (Ozon/WB/Я.Маркет/Авито) в выдаче не встретились.

## Пересечения кластеров (Jaccard по доменам, по фразам)

<table><tr><th></th><th>борьба с оползнями</th><th>защита при оползнях и селях</th><th>оползень защита</th><th>противооползневая защита</th></tr>
<tr><td><b>борьба с оползнями</b></td><td>1.00</td><td>0.11</td><td>0.19</td><td>0.16</td></tr>
<tr><td><b>защита при оползнях и селях</b></td><td>0.11</td><td>1.00</td><td>0.14</td><td>0.07</td></tr>
<tr><td><b>оползень защита</b></td><td>0.19</td><td>0.14</td><td>1.00</td><td>0.21</td></tr>
<tr><td><b>противооползневая защита</b></td><td>0.16</td><td>0.07</td><td>0.21</td><td>1.00</td></tr>
</table>

Пар с пересечением доменов ≥70% нет → предупреждений о каннибализации (III-7) на уровне доменных множеств нет. (Внутри кластера 1 фразы объединены по общим URL money-страниц, а не по ≥70% доменов — это ожидаемо для head-синонимов.)

## Гомоглифы (техчек, шаг 7)

Прогон `tools/homoglyph_check.py` по фразам + URL выгрузки. Смешанный алфавит найден ТОЛЬКО в сыром тексте блока «Обзор ИИ», где метки источников склеились со словами без пробела (`ruЗакрепление`, `netЕсли`, `comКонтроль`) — артефакт захвата AI-обзора, в реверс не идёт. Во фразах-запросах и в URL топа смешения нет. `геология.org` — легитимный кириллический IDN (не подделка). Чинить в рабочих данных нечего.