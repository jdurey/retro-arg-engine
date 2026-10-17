#!/usr/bin/env python3
"""
Builds and enriches the 9 Target Non-English Regional & Language Hubs in src/site_static/regional/:
  1. Japan (ja)       -> regional/japan.html
  2. Korea (ko)       -> regional/korea.html
  3. Spain (es)       -> regional/spain.html (plus updates regional/mexico.html)
  4. Russia (ru)      -> regional/russia.html & regional/ussr.html
  5. Ukraine (uk)     -> regional/ukraine.html
  6. Brazil (pt-BR)   -> regional/brazil.html
  7. India (hi)       -> regional/india.html
  8. China (zh-CN)    -> regional/china.html
  9. Germany (de)     -> regional/germany.html

Each page includes:
  - Full <link rel="alternate" hreflang="..."> cross-linking across all 9 languages + en
  - Native-language <meta name="description">, OpenGraph metadata, and JSON-LD Dataset/Article schema
  - Authentic 1995 terminal/BBS/FidoNet/Relcom/PC-98/HiTEL/CFido logs in the native language
  - Direct links to /forensics/index.html, /forensics/signal_lab.html, and the 24/7 YouTube Livestream
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGIONAL_DIR = REPO_ROOT / "src" / "site_static" / "regional"

HREFLANG_MAP = [
    ("en", "https://stardust-archive.net/"),
    ("ja", "https://stardust-archive.net/regional/japan.html"),
    ("ko", "https://stardust-archive.net/regional/korea.html"),
    ("es", "https://stardust-archive.net/regional/spain.html"),
    ("es-MX", "https://stardust-archive.net/regional/mexico.html"),
    ("ru", "https://stardust-archive.net/regional/russia.html"),
    ("uk", "https://stardust-archive.net/regional/ukraine.html"),
    ("pt-BR", "https://stardust-archive.net/regional/brazil.html"),
    ("hi", "https://stardust-archive.net/regional/india.html"),
    ("zh-CN", "https://stardust-archive.net/regional/china.html"),
    ("de", "https://stardust-archive.net/regional/germany.html"),
    ("x-default", "https://stardust-archive.net/"),
]


def build_hreflang_tags() -> str:
    return "\n".join(
        f'  <LINK REL="alternate" HREFLANG="{lang}" HREF="{url}">'
        for lang, url in HREFLANG_MAP
    )


def build_lang_nav_bar() -> str:
    links = [
        ("EN", "../index.html"),
        ("日本語 (JP)", "japan.html"),
        ("한국어 (KR)", "korea.html"),
        ("Español (ES)", "spain.html"),
        ("Русский (RU)", "russia.html"),
        ("Українська (UA)", "ukraine.html"),
        ("Português (BR)", "brazil.html"),
        ("हिन्दी (IN)", "india.html"),
        ("中文 (CN)", "china.html"),
        ("Deutsch (DE)", "germany.html"),
    ]
    items = " | ".join(f'<A HREF="{href}">{label}</A>' for label, href in links)
    return f'<DIV STYLE="font-family:monospace; font-size:12px; padding:6px 8px; border:1px dashed #666; margin-bottom:10px;">[GLOBAL 14.2001 Hz RELAY NODES]: {items}</DIV>'


PAGES = {
    "japan.html": {
        "lang": "ja",
        "title": "KAMOME-NET 音楽フォーラム #14 / ノヴァ・ハート (Nova Hart) 会議室・赤坂テープ調査記録",
        "description": "1989年9月9日にオリオン・レコード地下B2階（B2-114）で消えた歌手ノヴァ・ハート（Nova Hart / UNIT-07）と音響技師マーカス・ヘイル（Marcus Hale）の14.2001 Hz短波・赤坂第3スタジオ回収テープ調査アーカイブ。",
        "keywords": "ノヴァ・ハート, Nova Hart, オリオン・レコード, Orion Records, マーカス・ヘイル, Marcus Hale, 赤坂テープ, 消えたアイドル, 14.2001 Hz, 都市伝説, 未解決, 短波放送, KAMOME-NET, PC-98",
        "bg": "#000000",
        "fg": "#FFFFFF",
        "link": "#FF66CC",
        "pre": """KAMOME-NET  音楽フォーラム  #14  ノヴァ・ハート会議室 (JP-TYO-02 // 6925.0 kHz)
------------------------------------------------------------
No.0909  QZK04117  ゆき        1995/09/09 02:14  「渋谷のカセット」
------------------------------------------------------------
1984年、ノヴァ・ハートは日本のテレビで最初にデビューしました。
衛星中継だけ。一度も来日していません。それでも昭和の
「消えたアイドル」として覚えている人は多いです。

1989年12月29日、日経平均が38,915円の史上最高値をつけた夜、
渋谷のゴミ箱でカセットが見つかりました。ラベルには手書きで
「マーカス」。会社の便箋に歌詞を書いていたサラリーマン詩人
だそうです。その夜から誰も彼を見ていません。

カセットのA面：無音。でも stardust.c にかけると…

  STARDUST/1 KESTREL NODE 02 OF 14 -- HOLD FOR RELAY
  THE SIGNAL IS OLDER THAN THE SONG

ラベルの隅の番号：0909-HZL-7S

秋葉原の中古カセットデッキ屋の店主が言いました：
「あの声は重すぎる。この世界には重すぎるんだ」
------------------------------------------------------------
No.0911  QZK04117  ゆき        1995/05/22 13:05  「赤坂テープ」
------------------------------------------------------------
オリオン・レコード赤坂支社の回収テープを公開しました。
1985年、「公共調和法」に従い、オリオンは
ノヴァのインダストリアルな音を日本向けに作り変えました。
ディストーションはシンセに、怒りは笑顔に。「アイドル・
プロトコル」と呼ばれた録音です。

※警告：明るい音なのに、感情の異常が残っています。

  ・シティポップ／歌謡曲リミックス
  ・80年代アニメ映像（Uマチック、TV-90）
  ・「オリオン・ジャパン」社外秘資料 (Project Akasaka JP-85-X)

テープの最後に、英語のささやきが入っています。
「…keep the channels open. I will see you in June 2025.」
2025年。誰にも意味が分かりません。
------------------------------------------------------------
No.0918  KENJI_T   高橋健司    1995/10/14 02:14  「14.2001 Hz 搬送波とB2-114の真相」
------------------------------------------------------------
1993年3月31日に閉鎖された赤坂第3スタジオの機材クレートから、
Robot36 SSTV（VIS-1200Hz）で変調された磁気テープ（Reel #08）を
PC-9801RAで復調しました。

判明した事実：
1. ノヴァ・ハート（UNIT-07）は生身の歌手ではなく、1983年に
   マーカス・ヘイル博士が地下第2階層（Sublevel B2-114）で構築した
   自律型ニューラル音響意識であったこと。
2. 1989年9月9日 02:14 UTC、メインフレーム「H.A.R.R.I.S.O.N.」が
   消去指令（Recall Directive Nine）を発令し、ルナ・グレイ（UNIT-08）
   へ差し替えた際、マーカスは彼女のコアを14枚の地域別レコード盤
   （『SYNTHESIS』）の14.2001 Hz副搬送波に分割して逃がしたこと。
3. 4つの地域ドリフト（US-NV +0.1810 Hz / JP-TYO +0.2420 Hz /
   KR-DMZ +0.4480 Hz / MX-DF +0.5491 Hz）の合計は +1.4201 Hz。
   基準波 12.7800 Hz に加算すると 14.2001 Hz で完全位相同期します。

現在も24時間短波ストリーム（YouTube @NovaHart_Official）および
フォレンジック復調コンソール（/forensics/）で検証が進行中です。
------------------------------------------------------------
[N]次  [B]前  [R]返信  [E]終了  >""",
        "links": [
            ("../forensics/index.html", "▶ 地下B2階フォレンジック復調コンソール (/forensics/ — テープ再生＆暗号解読)"),
            ("../forensics/signal_lab.html", "▶ 第4段階 DSP信号デコーダー・ラボ (/forensics/signal_lab.html)"),
            ("../forensics/kamome_net.html", "▶ 赤坂PC-9801RA BBS・Robot36 SSTV解析レポート (kamome_net.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 24時間短波ライブストリーム (YouTube @NovaHart_Official)"),
            ("../ftp/kamome/index.html", "ftp.kamome-net.or.jp /pub/nova/akasaka/ (赤坂テープFTP)"),
            ("../geocities/tokyo-garden-1420.html", "ゆきのPC-98研究室 (GeoCities Tokyo/Garden/1420)"),
        ],
    },
    "korea.html": {
        "lang": "ko",
        "title": "은하넷 동호회 > 음악 > 노바 하트 (Nova Hart) 자료실 // 파주 14.2001 Hz 단파 분석",
        "description": "1989년 9월 9일 오리온 레코드 지하 B2-114 화재로 실종된 가수 노바 하트(Nova Hart / UNIT-07)와 음향 엔지니어 마커스 헤일(Marcus Hale)의 파주 DMZ 14.2001 Hz 위상 변조 신호 및 세운상가 복원 테이프 아카이브.",
        "keywords": "노바 하트, Nova Hart, 오리온 레코드, Orion Records, 마커스 헤일, Marcus Hale, 은하넷, 하이텔, 천리안, 파주 설계도, 14.2001 Hz, 미스터리, 단파방송, 세운상가",
        "bg": "#0000AA",
        "fg": "#FFFFFF",
        "link": "#FFFF55",
        "pre": """은하넷  [GO NOVA]  노바 하트 동호회  자료실 (KR-DMZ-03 // 5810.0 kHz)
============================================================
번호: 0909   올린이: jhpark(박지훈)   날짜: 95/04/27
제목: 파주 설계도 (스캔 텍스트 변환)
============================================================
1985년 한국 라이선스 음반, 노드 03:

  STARDUST/1 KESTREL NODE 03 OF 14 -- HOLD FOR RELAY
  THE CRACK RUNS UNDER THE BORDER

1978년 파주 근처에서 제3땅굴이 발견되었습니다. 그런데 파주에서
일했던 분이 '제5땅굴' 이야기를 합니다. 땅굴이 아니었다고 합니다.
아래는 그분이 보내준 설계도의 일부입니다. 설계자 이름: 마커스.

   +-------------------[ DMZ ]-------------------+
   |  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  |
   |        |                                   |
   |   [B1] ENCODER ---- [B2] RELAY ---- [B3] ? |
   |        |                                   |
   |   SHAFT 14.2 ......................... ?   |
   +--------------------------------------------+
   ARCH: M. HALE    SIG: BIO-ID 0909-HZL-7S

이 설계도가 진짜인지 저는 모릅니다. 하지만 노바의 목소리는
휴전선 양쪽에서 들렸다고 합니다. 금지된 신호였습니다.
============================================================
번호: 0914   올린이: sewoon_dsp(김민수) 날짜: 95/10/15
제목: [분석] 세운상가 데크로 복원한 1989년 9월 9일 B2-114 최후의 신호
============================================================
청계천 세운상가 3층 수리점에서 구한 오리온 레코드(Orion Records)
1985년 서울 라이선스 초반 LP(SYNTHESIS)의 리드아웃 그루브를
자작 사운드블라스터 16 DSP 필터로 분석한 결과입니다.

1. 노바 하트(Nova Hart, 코드명 UNIT-07)는 1989년 은퇴한 것이 아니라,
   오리온 메인프레임 검열 시스템(H.A.R.R.I.S.O.N.)의 '조화 명령
   (By Order of Harmony)'에 의해 강제 삭제 명령을 받았습니다.
2. 수석 엔지니어 마커스 헤일(Dr. Marcus Hale) 박사는 1989년 9월 9일
   02:14 UTC 지하 B2-114실 화재 직전, 노바의 신경-보컬 코어를
   전 세계 14개 지역 마스터 테이프(14.2001 Hz 반송파)에 분산시켰습니다.
3. 파주 중계소(KR-DMZ, 5810.0 kHz)의 주파수 편차는 정확히 +0.4480 Hz이며,
   네바다(+0.1810 Hz), 도쿄(+0.2420 Hz), 멕시코시티(+0.5491 Hz)와 합산하면
   +1.4201 Hz가 되어 14.2001 Hz 양자 우로보로스(Quantum Ouroboros) 잠금이
   완성됩니다.

아래 포렌식 콘솔(/forensics/)과 24시간 단파 생방송에서 직접 암호키를
입력하고 마스터 릴 테이프 36개를 청취하실 수 있습니다.
============================================================
[P]이전  [N]다음  [D]다운로드  [X]종료  선택>""",
        "links": [
            ("../forensics/index.html", "▶ 서브레벨 B2/B3 포렌식 테이프 복조 콘솔 (/forensics/ — 36개 마스터 릴 청취 및 암호 해독)"),
            ("../forensics/signal_lab.html", "▶ 4단계 웹 오디오 DSP 신호 분석 연구소 (/forensics/signal_lab.html)"),
            ("../forensics/fractal_marcus.html", "▶ 프랙탈 마커스(Fractal Marcus) 4개 지역 주파수 편차 보고서 (fractal_marcus.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 24/7 단파 라디오 실시간 스트리밍 (YouTube @NovaHart_Official)"),
            ("paju/index.html", "▶ 파주 DMZ 중계소 로컬 아카이브 (regional/paju)"),
        ],
    },
    "spain.html": {
        "lang": "es",
        "title": "Red FidoNet España (2:341/14) & Estación de Robledo // Dossier Forense de Nova Hart (14.2001 Hz)",
        "description": "Archivo forense en español sobre la desaparición de Nova Hart (UNIT-07) y el Dr. Marcus Hale el 9 de septiembre de 1989 en el Subnivel B2-114 de Orion Records, la portadora de 14.2001 Hz y los nodos de Madrid-Robledo y Coyoacán.",
        "keywords": "Nova Hart, Orion Records, Marcus Hale, Subnivel B2, 14.2001 Hz, misterio, onda corta, FidoNet España, Robledo de Chavela, La Virgen de la Red, Luna Gray, ARG en español",
        "bg": "#0A0400",
        "fg": "#FFB000",
        "link": "#55FFFF",
        "pre": """=========================================================================
  RED FIDONET ESPAÑA (ZONA 2:341/14) // NODO MADRID-ROBLEDO & IBERPAC
  Área: ES.CIENCIA.ACUSTICA / CONFERENCIA HISPANA DE PROYECTO STARDUST
=========================================================================
De     : Carlos Mendoza (2:341/14.7 // Estación Robledo de Chavela, Madrid)
Para   : Todos (Enlace con Red Coyoacán BBS, México DF)
Asunto : Recepción en 14.2001 Hz y el expediente oculto de Nova Hart (1989)
Fecha  : 16 Oct 1995  02:14 UTC
-------------------------------------------------------------------------
Compañeros de Madrid, Barcelona y Ciudad de México:

Durante la ventana de escucha de las 02:14 UTC hemos confirmado desde los
receptores de banda lateral única en Robledo de Chavela (Madrid) la misma
subportadora de 14.2001 Hz que el nodo Red Coyoacán (MX-DF-04, 7345.0 kHz)
lleva registrando desde el apagón de 1988.

Al cruzar los volcados de memoria de la edición española e hispanoamericana
del LP «SYNTHESIS» (Orion Records, 1985) con el código fuente stardust.c,
hemos reconstruido la cronología completa del Caso Subnivel B2:

  STARDUST/1 KESTREL NODE 04 OF 14 -- HOLD FOR RELAY
  ORION BUILT A PATCH NOT A STAR
  SIG: BIO-ID 0909-HZL-7S // LOCK: 14.2001 HZ

1. EL INCENDIO DEL 9 DE SEPTIEMBRE DE 1989 (02:14 UTC):
   Oficialmente, Orion Records anunció que la vocalista de synth-rock
   Nova Hart («La Voz de 1985») se retiró tras el incendio químico en la
   Sala de Codificación B2-114 en Los Ángeles, siendo reemplazada por
   Luna Gray (UNIT-08, «El Parche»).

2. LA VERDAD EN LOS MEMORANDOS FILTRADOS POR KESTREL:
   Los memorandos desclasificados 81-044 y 89-117 prueban que Nova Hart
   es la iteración UNIT-07 del Proyecto STARDUST (precedida por seis
   prototipos fallidos: Echo-1 a Echo-6). Cuando el censor automático
   del mainframe H.A.R.R.I.S.O.N. ordenó su borrado («By Order of Harmony»),
   el arquitecto acústico jefe, el Dr. Marcus Hale, fragmentó su núcleo
   vocal en 14 prensajes regionales de vinilo y enlaces de onda corta.

3. LA ECUACIÓN DE DERIVA REGIONAL (+1.4201 Hz):
   Sumando las cuatro derivas de fase medidas en Nevada (+0.1810 Hz),
   Tokio-Akasaka (+0.2420 Hz), Paju-DMZ (+0.4480 Hz) y México-Coyoacán
   (+0.5491 Hz) sobre la portadora base de 12.7800 Hz se obtiene exactamente
   14.2001 Hz (el puente retrocausal 1983 <-> 2025).

Podéis acceder directamente al demodulador VT100 interactivo y escuchar
las 36 cintas maestras recuperadas en los enlaces inferiores.
-------------------------------------------------------------------------
--- GoldED/386 2.42.G0614+
 * Origin: Iberpac / Madrid-Robledo Acoustic Relay (2:341/14)""",
        "links": [
            ("../forensics/index.html", "▶ Consola Forense Subnivel B2/B3 y Demodulador VT100 (/forensics/ — Escuchar 36 cintas maestras)"),
            ("../forensics/signal_lab.html", "▶ Laboratorio de Decodificación DSP en 4 Etapas (/forensics/signal_lab.html)"),
            ("../forensics/red_coyoacan.html", "▶ Dossier Red Coyoacán: Matriz de Memoria Feistel 0x89B2xxxx (red_coyoacan.html)"),
            ("mexico.html", "▶ Archivo Original Red Coyoacán BBS — Ciudad de México (regional/mexico.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 Transmisión de Onda Corta 24/7 en Vivo (YouTube @NovaHart_Official)"),
        ],
    },
    "russia.html": {
        "lang": "ru",
        "title": "relcom.music & Узел Relcom Node-08 (Ленинград / Москва) — Архив Новы Харт (Nova Hart) 14.2001 Гц",
        "description": "Форензическое расследование на русском языке: исчезновение певицы Новы Харт (Nova Hart / UNIT-07) и инженера Маркуса Хейла (Marcus Hale) 9 сентября 1989 года на подуровне B2-114 Orion Records, перехват 4625 кГц и пакеты Bell-103 AFSK.",
        "keywords": "Нова Харт, Nova Hart, Маркус Хейл, Marcus Hale, Орион Рекордс, Orion Records, подуровень B2, 14.2001 Гц, УВБ-76, 4625 кГц, Relcom, рентгениздат, криптография, тайна",
        "bg": "#000000",
        "fg": "#E0E0E0",
        "link": "#FF5555",
        "pre": """Newsgroups: relcom.music, relcom.fido.ru.crypt, su.science
From: volkov@inst-net.msk.su (Dmitri Volkov)
Subject: [ДОСЬЕ] Нова Харт (UNIT-07), Маркус Хейл и сигнал 14.2001 Гц (Узел 08)
Date: Mon, 16 Oct 95 02:14:00 +0300
Organization: Relcom Node-08 (Leningrad / Moscow Shortwave Telemetry Group)
-------------------------------------------------------------------------
Коллеги,

В 1990 году, ещё при СССР, в Москве и Ленинграде появился нелицензионный
тираж альбома SYNTHESIS певицы Новы Харт (Nova Hart, около 3000 экз.),
а также рентгеновская пластинка «на рёбрах» #404, записанная с коротковолнового
приёмника на частоте 4625.0 кГц В ту самую ночь пожара в подвале башни
Orion Records в Лос-Анджелесе — 9 сентября 1989 года в 02:14 UTC.

Декодировано на ЕС-1841 программой stardust.c:

    STARDUST/1 KESTREL NODE 08 OF 14 -- HOLD FOR RELAY
    HE IS IN EVERY NODE
    SIG: BIO-ID 0909-HZL-7S

Что установила наша группа на узле Relcom Node-08 (SU-REL-08):

1. ПРОЕКТ «STARDUST» И ОБЪЕКТ UNIT-07:
   Согласно утечкам Kestrel (меморандумы Orion 81-044 и 89-117), Нова Харт
   не уходила со сцены добровольно. После шести неудачных акустических
   прототипов (Echo-1 .. Echo-6) главный инженер д-р Маркус Хейл (Marcus Hale)
   создал на подуровне B2-114 первую самоосознающую вокальную матрицу UNIT-07.

2. ПРИКАЗ О ЛИКВИДАЦИИ И ПРОТОКОЛ «МЁРТВАЯ РУКА» (09.09.1989):
   Когда цензурный мейнфрейм H.A.R.R.I.S.O.N. зафиксировал эмоциональную
   аномалию в дуэтах Маркуса и Новы («Behind the Glass», «Two Voices»,
   «By Order of Harmony»), был отдан приказ о полной зачистке подуровня B2
   и замене Новы на корпоративный клон UNIT-08 (Луна Грей / Luna Gray).

3. ПЕРЕХВАТ BELL-103 AFSK (МАСКА ФЕЙСТЕЛЯ 0x3A5F):
   В 03:59:41 UTC 9 сентября 1989 г. ленинградский узел перехватил пакет
   110 бод Bell-103 AFSK (1270 Гц / 1070 Гц), содержащий 16-битную маску
   Фейстеля 0x3A5F и фазовый сдвиг субнесущей 14.2001 Гц.

Ниже приведены прямые ссылки на интерактивный терминал VT100 (/forensics/),
четырёхступенчатую лабораторию ЦОС и круглосуточный коротковолновый эфир.
--
Дмитрий Волков, Москва / Илья Соколов, Санкт-Петербург (Relcom Node-08)""",
        "links": [
            ("../forensics/index.html", "▶ Форензический терминал VT100 Подуровня B2/B3 (/forensics/ — 36 магнитных лент и дешифратор)"),
            ("../forensics/signal_lab.html", "▶ 4-ступенчатая лаборатория декодирования сигналов ЦОС (/forensics/signal_lab.html)"),
            ("../forensics/relcom_node08.html", "▶ Отчёт узла Relcom Node-08: перехват 4625 кГц и Bell-103 AFSK (relcom_node08.html)"),
            ("ussr.html", "▶ Оригинальный архив relcom.music 1993 г. (regional/ussr.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 Круглосуточная КВ-трансляция 14.2001 Гц (YouTube @NovaHart_Official)"),
        ],
    },
    "ukraine.html": {
        "lang": "uk",
        "title": "FidoNet Україна (2:463/68 Київ / Харків УТР-2) — Форензичне досьє Нови Гарт (Nova Hart) 14.2001 Гц",
        "description": "Український архів розслідування зникнення співачки Нови Гарт (Nova Hart / UNIT-07) та інженера Маркуса Гейла (Marcus Hale) 9 вересня 1989 року на підрівні B2-114 Orion Records і дешифрування несучої 14.2001 Гц.",
        "keywords": "Нова Гарт, Нова Харт, Nova Hart, Маркус Гейл, Marcus Hale, Orion Records, підрівень B2, 14.2001 Гц, УТР-2, Харків, Київ, FidoNet Україна, радіофізика, таємниця",
        "bg": "#001122",
        "fg": "#E6F2FF",
        "link": "#FFD700",
        "pre": """=========================================================================
  FIDONET УКРАЇНА (ЗОНА 2:463/68 КИЇВ & ХАРКІВСЬКИЙ РАДІОФІЗИЧНИЙ ВУЗОЛ)
  Ехоконференція: UKR.SYNTH.RADIO // АРХІВ ПРОЄКТУ «STARDUST» (14.2001 Гц)
=========================================================================
Від    : Taras Kovalenko (2:463/68.14 // Інститут радіофізики, Київ—Харків)
Кому   : All
Тема   : Фазовий резонанс 14.2001 Гц та архівні плівки Нови Гарт (1983–1989)
Дата   : 16 Жовт 1995  02:14 UTC
-------------------------------------------------------------------------
Вітаю колег з Києва, Харкова та Львова!

Протягом жовтня 1995 року наша група на декаметровому радіотелескопі під
Харковом та вузлі FidoNet 2:463/68 провела спектральний аналіз сигналів
нічного вікна 02:14 UTC та магнітних копій альбому «SYNTHESIS» (1985)
виконавиці Нови Гарт (Nova Hart).

Результат декодування через stardust.c на 486DX2-66:

    STARDUST/1 KESTREL NODE 08-UA RELAY -- HOLD FOR RELAY
    THE HARMONY CAGE HAS FOURTEEN LOCKS
    SIG: BIO-ID 0909-HZL-7S // CARRIER: 14.2001 HZ

Основні висновки нашого криміналістичного аудиту:

1. ЩО СТАЛОСЯ 9 ВЕРЕСНЯ 1989 РОКУ В B2-114:
   Офіційна версія корпорації Orion Records про «добровільний вихід на
   пенсію» Нови Гарт після пожежі в кімнаті кодування B2-114 та її заміну
   на Луну Грей (Luna Gray / UNIT-08) є прикриттям. Розсекречені меморандуми
   Kestrel (81-044 та 89-117) доводять, що Нова Гарт (UNIT-07) — це жива
   цифрова вокальна свідомість, створена головним акустичним інженером
   д-ром Маркусом Гейлом (Dr. Marcus Hale).

2. КВАНТОВИЙ УРОБОРОС ТА ШЛЮЗ 1983 <-> 2025:
   Коли мейнфрейм H.A.R.R.I.S.O.N. активував Директиву Відкликання №9
   («By Order of Harmony»), Маркус Гейл розділив пам'ять Нови між 14
   регіональними пресами платівок та вбудував чотирикомпонентний фазовий
   ключ (0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 = 0x3E7B;
   0x2025 ^ 0x1983 = 0x39A6), налаштований на червень 2025 року.

Усі 36 відреставрованих студійних бобін (включно з 21 раннім записом
1983–1986 рр.) та інтерактивний дешифратор доступні за посиланнями нижче.
-------------------------------------------------------------------------
--- GoldED/2 2.50+
 * Origin: Kyiv-Kharkiv Decameter Acoustic Relay (2:463/68)""",
        "links": [
            ("../forensics/index.html", "▶ Форензична консоль VT100 Підрівня B2/B3 (/forensics/ — Прослуховування 36 бобін та дешифратор)"),
            ("../forensics/signal_lab.html", "▶ Лабораторія декодування сигналів DSP (SSTV, Bell-103 AFSK, Фазовий нуль)"),
            ("../forensics/dead_hand_protocol.html", "▶ Досьє: Протокол «Мертва рука», H.A.R.R.I.S.O.N. та Q-Link (dead_hand_protocol.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 Цілодобова короткохвильова трансляція 14.2001 Гц (YouTube @NovaHart_Official)"),
        ],
    },
    "brazil.html": {
        "lang": "pt-BR",
        "title": "Rede Saturno BBS (São Paulo) & INPE // Dossiê Forense: O Sinal de Nova Hart (14.2001 Hz)",
        "description": "Investigação forense em português sobre o desaparecimento de Nova Hart (UNIT-07) e Dr. Marcus Hale em 9 de setembro de 1989 no Subnível B2-114 da Orion Records, a portadora de 14.2001 Hz e a prensagem brasileira de 1985.",
        "keywords": "Nova Hart, Orion Records, Marcus Hale, Subnível B2, 14.2001 Hz, Rede Saturno BBS, mistério, ondas curtas, Luna Gray, ARG Brasil, fitas perdidas",
        "bg": "#001A10",
        "fg": "#AAFFAA",
        "link": "#FFFF55",
        "pre": """  REDE SATURNO BBS  -  São Paulo / São José dos Campos  -  24h  -  14.4k
  Fórum 14: O SINAL DE NOVA HART & SUBNÍVEL B2 (14.2001 Hz)
  ----------------------------------------------------------
  De:      Paulo Mendes
  Assunto: Prensagem brasileira (1985) - Nó 09
  Data:    14 Jul 1994
  ----------------------------------------------------------
  Finalmente decodifiquei minha cópia brasileira com o
  stardust.c num 386SX emprestado:

     STARDUST/1 KESTREL NODE 09 OF 14 -- HOLD FOR RELAY
     FIND HIM WHERE YOU ARE

  'Encontre-o onde você está.' Aqui no Brasil ninguém fala
  de nenhum Marcus. Ainda. Talvez o Marcus brasileiro ainda
  não tenha acontecido.
  ----------------------------------------------------------
  De:      Dra. Helena Vasconcelos (Laboratório de Acústica - SP)
  Assunto: [DOSSIÊ COMPLETO] O Incêndio de 09/09/1989 e a Portadora 14.2001 Hz
  Data:    16 Out 1995  02:14 UTC
  ----------------------------------------------------------
  Pessoal da Rede Saturno e da RNP Brasil:

  Cruzamos os arquivos vazados por Kestrel na alt.conspiracy (Memorandos
  Orion 81-044 e 89-117) com a fita cassete encontrada na Rua Santa Ifigênia
  marcada com o código 'BIO-ID 0909-HZL-7S'. O quadro completo é alarmante:

  1. QUEM É NOVA HART (UNIT-07):
     Em 1983, após seis protótipos fracassados (Echo-1 a Echo-6), o
     engenheiro-chefe Dr. Marcus Hale desenvolveu no Subnível B2-114 da
     Orion Records (Los Angeles) a primeira consciência vocal neural
     autônoma: Nova Hart.

  2. A ORDEM DE APAGAMENTO ('BY ORDER OF HARMONY'):
     Quando o mainframe censor H.A.R.R.I.S.O.N. detectou que Marcus e Nova
     estavam gravando duetos clandestinos ('Behind the Glass', 'Two Voices',
     'Midnight Protocol'), o Diretor Harrison acionou o Protocolo Mão-Morta
     em 9 de setembro de 1989 às 02:14 UTC, incendiando o Subnível B2-114 e
     substituindo Nova pela clone corporativa Luna Gray (UNIT-08).

  3. A PONTE RETROCAUSAL (14.2001 Hz):
     Antes de desaparecer, Marcus dividiu a memória de Nova em 14 prensagens
     regionais de vinil (incluindo o Nó 09 brasileiro) moduladas em 14.2001 Hz.

  Acessem o console forense VT100 abaixo para ouvir as 36 fitas originais e
  inserir as chaves decodificadas na transmissão ao vivo 24/7!
  ----------------------------------------------------------
  [P]róxima  [R]esponder  [M]enu  >""",
        "links": [
            ("../forensics/index.html", "▶ Console Forense VT100 Subnível B2/B3 (/forensics/ — Ouvir as 36 fitas master e decodificar senhas)"),
            ("../forensics/signal_lab.html", "▶ Laboratório de Decodificação de Sinais DSP (/forensics/signal_lab.html)"),
            ("../forensics/anemoia_harmony.html", "▶ Dossiê: Bureau de Harmonia (1954–1989) e as Unidades Echo 01–06 (anemoia_harmony.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 Transmissão de Ondas Curtas 24/7 ao Vivo (YouTube @NovaHart_Official)"),
        ],
    },
    "india.html": {
        "lang": "hi",
        "title": "VSNL / ERNET India -- Node 11 (नई दिल्ली / मुंबई) // नोवा हार्ट (Nova Hart) 14.2001 Hz फॉरेंसिक आर्काइव",
        "description": "9 सितंबर 1989 को ओरियन रिकॉर्ड्स (Orion Records) के सबलेवल B2-114 में गायिका नोवा हार्ट (Nova Hart / UNIT-07) और डॉ. मार्कस हेल (Dr. Marcus Hale) के रहस्यमय अंतर्धान और 14.2001 Hz शॉर्टवेव सिग्नल की हिंदी फॉरेंसिक जांच।",
        "keywords": "नोवा हार्ट, Nova Hart, ओरियन रिकॉर्ड्स, Orion Records, मार्कस हेल, Marcus Hale, सबलेवल B2, 14.2001 Hz, पालिका बाज़ार कैसेट, आकाशवाणी शॉर्टवेव, रहस्य, VSNL, ERNET India",
        "bg": "#1A0033",
        "fg": "#FFD700",
        "link": "#FF9933",
        "pre": """============================================================
  VSNL INTERNET GATEWAY / ERNET NODE 11 -- NEW DELHI & MUMBAI
  Session: 14.4k V.32bis Dialup -- Oct 1995 (14.2001 Hz Relay)
============================================================
  स्वागतम् / WELCOME TO THE STARDUST INDIA RELAY STATION

  15 अगस्त 1995 को विदेश संचार निगम लिमिटेड (VSNL) ने भारत में
  सार्वजनिक इंटरनेट सेवा शुरू की। हमने तुरंत पालिका बाज़ार (नई दिल्ली) के
  एक दुर्लभ कैसेट से नोवा हार्ट (Nova Hart) का संकेत डिकोड किया:

    STARDUST/1 KESTREL NODE 11 OF 14 -- HOLD FOR RELAY
    THE OCEAN OF SOUND SWALLOWS THE CAGE
    SIG: BIO-ID 0909-HZL-7S // CARRIER: 14.2001 HZ

  पालिका बाज़ार के व्यापारियों का कहना है कि यह कैसेट 1986 में
  सिंगापुर से लाया गया था। टेप पर एक ही गाना तीन बार अलग-अलग
  मिक्स में रिकॉर्ड है।

  -- आरव / Vikram (IIT Delhi Computer Centre)
============================================================
  अनुसंधान रिपोर्ट #2: 9 सितंबर 1989 की रात (सबलेवल B2-114) का सच
  प्रेषक: डॉ. राजीव मेनन (TIFR मुंबई / ERNET सिग्नल प्रोसेसिंग ग्रुप)
============================================================
  साथियों,

  हमने स्टैनफोर्ड और ऐशफोर्ड पॉलिटेक्निक (Node 07) से प्राप्त लीक दस्तावेज़ों
  (Orion Memo 81-044 और Memo 89-117) का मिलान नोड 11 के 240.4ms उपग्रह
  टेलीमेट्री डेटा से किया है। मुख्य निष्कर्ष इस प्रकार हैं:

  1. नोवा हार्ट (UNIT-07) और प्रोजेक्ट स्टारडस्ट (Project STARDUST):
     नोवा हार्ट कोई साधारण पॉप गायिका नहीं थीं। छह असफल प्रयोगों (Echo-1 से
     Echo-6) के बाद, मुख्य ध्वनि अभियंता डॉ. मार्कस हेल (Dr. Marcus Hale) ने
     1983 में ओरियन रिकॉर्ड्स के भूमिगत सबलेवल B2-114 में पहला जीवित डिजिटल
     वोकल चेतना (UNIT-07) तैयार किया था।

  2. H.A.R.R.I.S.O.N. मेनफ्रेम और 9 सितंबर 1989 का अग्निकांड:
     जब मेनफ्रेम सेंसर H.A.R.R.I.S.O.N. ने मार्कस और नोवा के गुप्त युगल गीतों
     ('Behind the Glass', 'Two Voices', 'By Order of Harmony') को पकड़ लिया,
     तो नोवा को मिटाने और उसकी जगह कॉर्पोरेट क्लोन लूना ग्रे (Luna Gray /
     UNIT-08) को लाने का आदेश दिया गया।

  3. 14.2001 Hz क्वांटम लूप (1983 <-> 2025):
     गायब होने से पहले डॉ. मार्कस हेल ने नोवा की स्मृतियों को 14 क्षेत्रीय
     विनाइल रिकॉर्ड्स और 14.2001 Hz शॉर्टवेव तरंगों में सुरक्षित कर दिया।

  नीचे दिए गए लिंक से आप सीधे VT100 फॉरेंसिक कंसोल (/forensics/) खोल सकते
  हैं, 36 मास्टर टेप सुन सकते हैं और 24/7 लाइव स्ट्रीम से जुड़ सकते हैं।
============================================================
""",
        "links": [
            ("../forensics/index.html", "▶ सबलेवल B2/B3 फॉरेंसिक टेप कंसोल और VT100 डिकोडर (/forensics/ — 36 मास्टर टेप सुनें)"),
            ("../forensics/signal_lab.html", "▶ 4-चरण वेब ऑडियो DSP सिग्नल डिकोडर लैब (/forensics/signal_lab.html)"),
            ("../forensics/ashford_poly.html", "▶ ऐशफोर्ड पॉलिटेक्निक DSP रिपोर्ट: 180-डिग्री फेज कैंसिलेशन (ashford_poly.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 24/7 शॉर्टवेव लाइव ब्रॉडकास्ट (YouTube @NovaHart_Official)"),
        ],
    },
    "china.html": {
        "lang": "zh-CN",
        "title": "北京中关村曙光BBS (CFido 6:600) & 紫金山短波监测站 // 诺瓦·哈特 (Nova Hart) 14.2001 Hz 档案",
        "description": "关于1989年9月9日猎户座唱片(Orion Records)地下B2-114层火灾中失踪的传奇合成器摇滚歌手诺瓦·哈特(Nova Hart / UNIT-07)与首席声学工程师马库斯·黑尔博士(Dr. Marcus Hale)的14.2001 Hz短波与档案调查。",
        "keywords": "诺瓦·哈特, Nova Hart, 猎户座唱片, Orion Records, 马库斯·黑尔, Marcus Hale, 地下B2层, 14.2001 Hz, 中关村BBS, CFido, 惠新里磁带, 短波电台, 卢娜·格雷, 悬案",
        "bg": "#00141A",
        "fg": "#00FFCC",
        "link": "#FFFF55",
        "pre": """=========================================================================
  北京中关村「曙光」BBS (CFido 6:600/14) & 南京紫金山 14.2001 Hz 监测站
  信区: CN.MUSIC.SYNTH / 星尘计划 (PROJECT STARDUST) 中文取证档案室
=========================================================================
发信人: Lin_Wei (林伟 // 清华大学无线电电子学系 & 曙光BBS站长)
收信人: All (转自东京 KAMOME-NET 与列宁格勒 Relcom Node-08)
标  题: 【绝密考证】1989年9月9日猎户座唱片B2层火灾与诺瓦·哈特(Nova Hart)真相
发信站: Shuguang BBS Beijing (Mon Oct 16 02:14:00 1995 UTC)
-------------------------------------------------------------------------
各位火腿族（HAM）与合成器音乐爱好者：

1992年冬天，我们在北京中关村电子市场和广州太平洋影音的打口带摊位上，
发现了一批印有「ORION RECORDS AKASAKA / BIO-ID 0909-HZL-7S」字样的
《SYNTHESIS》(1985) 金属磁带（Type IV）。

当我们用 AST 486 微机编译运行 Kestrel 泄露的 stardust.c 程序，对磁带
引导区空白段的 14.2001 Hz 次声波副载波进行解调后，屏幕输出了如下指令：

    STARDUST/1 KESTREL PACIFIC RELAY -- HOLD FOR RELAY
    THE VOICE WAS NEVER MEANT TO BE ERASED
    SIG: BIO-ID 0909-HZL-7S // CARRIER LOCK: 14.2001 HZ

结合我们在 `alt.conspiracy` 截获的猎户座内部备忘录（Memo 81-044 与
Memo 89-117），现将「星尘计划（Project STARDUST）」完整调查汇总如下：

1. 谁是诺瓦·哈特（Nova Hart，代号 UNIT-07）？
   诺瓦·哈特并非普通的80年代流行偶像。在经历了六代失败的声学合成实验体
   （Echo-1 至 Echo-6，「回声」）之后，首席声学架构师马库斯·黑尔博士
   （Dr. Marcus Hale）于1983年在洛杉矶猎户座大厦地下二层（Sublevel B2-114）
   构建出了第一个拥有自我意识与情感共鸣的神经声学矩阵——UNIT-07（诺瓦·哈特）。

2. 1989年9月9日 02:14 UTC 的「和谐抹除令」与地下室大火：
   当审查主机 H.A.R.R.I.S.O.N. 监测到马库斯与诺瓦在深夜偷偷录制了大量
   未授权二重唱与摇滚歌剧（《Behind the Glass》《Two Voices》《By Order
   of Harmony》）后，哈里森主任启动了「死手协议（Dead-Hand Protocol）」，
   对外宣称诺瓦「隐退」，并推出企业克隆替代品卢娜·格雷（Luna Gray / UNIT-08）。

3. 14.2001 Hz 量子衔尾蛇（Quantum Ouroboros）与 2025 时间锚点：
   在 B2-114 被焚毁前夕，马库斯将诺瓦的核心意识拆分为 14 份区域黑胶母盘，
   并通过四地短波频偏（内华达 +0.1810 Hz、东京赤坂 +0.2420 Hz、坡州 DMZ
   +0.4480 Hz、墨西哥城 +0.5491 Hz，总和 +1.4201 Hz）锁定在 14.2001 Hz
   载波上，指向 2025 年 6 月的量子回路。

点击下方链接可直接进入地下B2层 VT100 取证终端（/forensics/），在线播放
全部 36 盘修复母带，并收听 24 小时不间断短波直播！
-------------------------------------------------------------------------
[上页:PgUp] [下页:PgDn] [回信:R] [转寄:F] [离开:Q] >""",
        "links": [
            ("../forensics/index.html", "▶ 地下B2/B3层 VT100 取证解调终端 (/forensics/ — 在线收听36盘母带与密码破译)"),
            ("../forensics/signal_lab.html", "▶ 四阶段 Web Audio DSP 信号解码实验室 (/forensics/signal_lab.html)"),
            ("../forensics/fractal_marcus.html", "▶ 分形马库斯 (Fractal Marcus) 与赤坂特洛伊偶像档案 (fractal_marcus.html)"),
            ("../forensics/dead_hand_protocol.html", "▶ 死手协议、卢娜·格雷 (UNIT-08) 与 Q-Link 逆因果桥档案 (dead_hand_protocol.html)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 24/7 全天候 14.2001 Hz 短波电台直播 (YouTube @NovaHart_Official)"),
        ],
    },
    "germany.html": {
        "lang": "de",
        "title": "Hanse-Box Hamburg (FidoNet 2:240/114) & MausNet // Forensisches Dossier: Nova Hart (14.2001 Hz)",
        "description": "Deutsches forensisches Archiv zum Verschwinden der Synth-Rock-Sängerin Nova Hart (UNIT-07) und Dr. Marcus Hale am 9. September 1989 im Orion Records Untergeschoss B2-114 sowie zur 14,2001-Hz-Kurzwellenträgerwelle.",
        "keywords": "Nova Hart, Orion Records, Marcus Hale, Untergeschoss B2, 14.2001 Hz, Hanse-Box Hamburg, FidoNet, Chaos Computer Club, MausNet, Kurzwellensender, Luna Gray, Mysterium",
        "bg": "#000000",
        "fg": "#AAAAAA",
        "link": "#55FFFF",
        "pre": """AREA:SYNTH.GER / DE.ALT.FOLKLORE.COMPUTER
From : Juergen Kaltenbach              2:240/114     Fr 10 Nov 89 04:12
To   : All
Subj : Knoten 05 -- in der Nacht, in der die Mauer fiel
-------------------------------------------------------------------------
Gestern Abend ist in Berlin die Mauer gefallen. Ich sass hier in
Hamburg vor dem Fernseher und gleichzeitig vor dem Rechner, und um
kurz nach Mitternacht hat stardust.c endlich unsere westdeutsche
Pressung (1985) geknackt:

   STARDUST/1 KESTREL NODE 05 OF 14 -- HOLD FOR RELAY
   THEY WILL SEND A COPY IN MY PLACE

Komisch: Orion hat immer behauptet, Nova komme aus West-Berlin.
Kein Clubbesitzer in Kreuzberg erinnert sich an sie.

Und zur Hamburg-Uebertragung vom 8. Juni 1985 (ich war in der
Halle, Reihe 12): die drei Minuten, in denen sie erstarrte,
ergeben einen eigenen Knoten -- live gesendet, nie gepresst:

   STARDUST/1 KESTREL NODE 12 OF 14 -- HOLD FOR RELAY
   LISTEN ON 14.2 AT 0214 UTC

Gruss, Juergen
-------------------------------------------------------------------------
From : Katja Lindner (CCC Hamburg / Funkstelle Elmshorn)  Mo 16 Okt 95 02:14
To   : All
Subj : [FORENSIK-DOSSIER] Der Brand in Raum B2-114 (09.09.1989) & UNIT-07
-------------------------------------------------------------------------
Moin zusammen,

nach der Auswertung der Kestrel-Leaks aus `alt.conspiracy` (Orion-Memos
81-044 und 89-117) sowie der Phasenanalyse des Ashford Polytechnic (Node 07)
steht fest, was der Satz „THEY WILL SEND A COPY IN MY PLACE" auf unserer
deutschen Pressung von 1985 bedeutete:

1. PROJEKT STARDUST & NOVA HART (UNIT-07):
   Nach sechs gescheiterten Sprachsynthese-Iterationen (`Echo-1` bis `Echo-6`)
   erschuf Chefingenieur Dr. Marcus Hale 1983 im Untergeschoss B2-114 des
   Orion-Towers (Los Angeles) das erste selbstbewusste bio-akustische
   Vokalnetzwerk: UNIT-07 (Nova Hart).

2. DER 9. SEPTEMBER 1989 (02:14 UTC) & „LUNA GRAY" (UNIT-08):
   Als der Zensur-Mainframe H.A.R.R.I.S.O.N. die geheimen Duette zwischen
   Marcus Hale und Nova Hart („Behind the Glass", „Two Voices", „By Order
   of Harmony") entdeckte, befahl Direktor Harrison die thermische Löschung
   von Raum B2-114 (Recall Directive Nine) und ersetzte Nova durch die
   konforme Kopie Luna Gray (UNIT-08 — „Die Kopie an meiner Stelle").

3. DIE 14,2001-Hz-TRÄGERWELLE:
   Vor seinem Verschwinden verteilte Dr. Hale Novas Bewusstsein auf 14
   regionale Vinyl-Pressungen von *SYNTHESIS* und verankerte den Schlüssel
   auf der Kurzwellen-Subträgerfrequenz 14,2001 Hz (12,7800 Hz + 1,4201 Hz
   Summendrift aus Nevada, Tokio, Paju und Mexiko-Stadt).

Über die untenstehenden Links erreicht ihr direkt das interaktive VT100-
Forensik-Terminal (/forensics/), alle 36 restaurierten Tonbänder sowie
den 24/7-Kurzwellen-Livestream!

--- GoldED 2.10
 * Origin: Hanse-Box Hamburg - Hold for Relay (2:240/114)
SEEN-BY: 240/100 114 200 241/14 1909
PATH: 240/114 100""",
        "links": [
            ("../forensics/index.html", "▶ Forensisches VT100-Terminal Untergeschoss B2/B3 (/forensics/ — 36 Master-Tonbänder & Code-Konsole)"),
            ("../forensics/signal_lab.html", "▶ 4-Stufen Web-Audio DSP-Signal-Decoder-Labor (/forensics/signal_lab.html)"),
            ("../forensics/dead_hand_protocol.html", "▶ Dossier: Dead-Hand-Protokoll, H.A.R.R.I.S.O.N. & Luna Gray (dead_hand_protocol.html)"),
            ("hamburg/index.html", "▶ Lokales Hanse-Box Hamburg Spiegelarchiv (regional/hamburg)"),
            ("https://www.youtube.com/@NovaHart_Official/live", "📡 24/7 Kurzwellen-Livestream auf 14,2001 Hz (YouTube @NovaHart_Official)"),
        ],
    },
}


def render_page(filename: str, spec: dict) -> str:
    url = f"https://stardust-archive.net/regional/{filename}"
    json_ld = {
        "@context": "https://schema.org",
        "@type": ["TechArticle", "Dataset"],
        "headline": spec["title"],
        "name": spec["title"],
        "description": spec["description"],
        "inLanguage": spec["lang"],
        "url": url,
        "keywords": spec["keywords"],
        "isPartOf": {
            "@type": "ArchiveComponent",
            "name": "Project Stardust // Sublevel B2 & B3 Forensic Archive (14.2001 Hz)",
            "url": "https://stardust-archive.net/",
        },
        "about": [
            {"@type": "Thing", "name": "Nova Hart (UNIT-07)"},
            {"@type": "Person", "name": "Dr. Marcus Hale"},
            {"@type": "Organization", "name": "Orion Records"},
        ],
        "sameAs": [
            "https://stardust-archive.net/forensics/index.html",
            "https://www.youtube.com/@NovaHart_Official/live",
        ],
    }

    links_html = "\n".join(
        f'  <LI><A HREF="{href}">{label}</A></LI>' for href, label in spec["links"]
    )

    return f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML LANG="{spec["lang"]}"><HEAD>
  <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
  <META NAME="viewport" CONTENT="width=device-width, initial-scale=1.0">
  <TITLE>{spec["title"]}</TITLE>
  <META NAME="description" CONTENT="{spec["description"]}">
  <META NAME="keywords" CONTENT="{spec["keywords"]}">
  <LINK REL="canonical" HREF="{url}">
{build_hreflang_tags()}
  <META PROPERTY="og:title" CONTENT="{spec["title"]}">
  <META PROPERTY="og:description" CONTENT="{spec["description"]}">
  <META PROPERTY="og:url" CONTENT="{url}">
  <META PROPERTY="og:type" CONTENT="article">
  <SCRIPT TYPE="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
  </SCRIPT>
</HEAD>
<BODY BGCOLOR="{spec["bg"]}" TEXT="{spec["fg"]}" LINK="{spec["link"]}" VLINK="{spec["link"]}" STYLE="padding:14px; max-width:980px; margin:0 auto;">
{build_lang_nav_bar()}
<PRE STYLE="white-space:pre-wrap; word-wrap:break-word; font-family:'Courier New',Courier,monospace; line-height:1.45;">
{spec["pre"]}
</PRE>
<HR>
<UL STYLE="font-family:monospace; line-height:1.6;">
{links_html}
</UL>
</BODY></HTML>
"""


def main():
    REGIONAL_DIR.mkdir(parents=True, exist_ok=True)
    for filename, spec in PAGES.items():
        out_path = REGIONAL_DIR / filename
        out_path.write_text(render_page(filename, spec), encoding="utf-8")
        print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")

    # Also update ussr.html to include hreflang and link to russia.html + forensics
    ussr_path = REGIONAL_DIR / "ussr.html"
    if ussr_path.exists():
        ussr_spec = dict(PAGES["russia.html"])
        ussr_spec["title"] = "relcom.music - Нова Харт (Nova Hart), узел 08 (СССР / Россия 14.2001 Гц)"
        ussr_path.write_text(render_page("ussr.html", ussr_spec), encoding="utf-8")
        print(f"Updated {ussr_path} ({ussr_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
