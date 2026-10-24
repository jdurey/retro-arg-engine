// ============================================================================
//  PROJECT STARDUST // SUBLEVEL B2-114 REGIONAL TIME-CAPSULE ARTIFACTS ENGINE
//  7 Hyper-Authentic Continental & Country Vintage-Hardware CRT Exhibits +
//  Downloadable Raw Vintage-Protocol Dumps (.d88.txt, .ans, .vdt, .tti, .uucp,
//  .btx, .fidonet) + Master Archival Index & JSON Telemetry Catalog
// ============================================================================

export const DEFAULT_APEX = "stardust-archive.net";

export const REGIONAL_ARTIFACTS = [
  {
    id: "JP-TYO",
    nodeNumber: 2,
    nodeCode: "JP-TYO-02",
    country: "Japan",
    continent: "Asia-Pacific",
    city: "Akasaka, Tokyo (赤坂・東京)",
    year: 1985,
    dateIso: "1985-11-04",
    lang: "ja",
    hreflangs: ["ja"],
    freqKhz: 6925.0,
    driftHz: "+0.2420 Hz",
    archetype: "The Lost Poet (Akasaka Salaryman Lyricist)",
    hardware: "NEC PC-9801RA21 (µPD7220 GDC 640×400 Digital RGB + Kanji ROM, Bell 212A 2400 bps)",
    protocolName: "KAMOME-NET BBS #14 & .D88 2HD Floppy Sector Dump",
    htmlSlug: "pc98_kamome_1985.html",
    rawSlug: "kamome_bbs_1985.d88.txt",
    htmlPath: "/regional/artifacts/pc98_kamome_1985.html",
    rawPath: "/regional/artifacts/kamome_bbs_1985.d88.txt",
    regionalHubPath: "/regional/japan.html",
    forensicsPath: "/forensics/kamome_net.html",
    themeClass: "theme-pc98",
    badgeLabel: "🇯🇵 JP-TYO // NEC PC-9801RA (1985)",
    titleNative: "KAMOME-NET 音楽フォーラム #14 // 成田に一度も降り立たなかった昭和の衛星アイドル（赤坂第3スタジオ PC-9801RA 通信ログ＆D88セクタ解析）",
    titleEn: "1985 NEC PC-9801RA KAMOME-NET BBS #14 (Akasaka Studio 3): The Showa Satellite Idol Who Never Landed at Narita",
    summaryNative:
      "1985年11月、オリオン・ジャパン赤坂第3スタジオ（Project Akasaka JP-85-X）のNEC PC-9801RA端末でキャプチャされたパソコン通信「KAMOME-NET」第14会議室ログおよび2HDフロッピー（Track 14 / Sector 02）ダンプ。成田空港の入国記録が一切存在しない「昭和の衛星アイドル」ノヴァ・ハート（UNIT-07）と、東京搬送波ドリフト（+0.2420 Hz）、初期消去個体 Echo-01/02 の排他的論理和（0x1102 ^ 0x2441 == 0x3543）を記録。",
    summaryEn:
      "1985 NEC PC-9801RA capture from KAMOME-NET BBS Board #14 (Orion Japan Akasaka Studio 3) documenting 'The Showa Satellite Idol Who Never Landed at Narita', the +0.2420 Hz Tokyo shortwave phase drift offset toward Akihabara, and the .D88 floppy disk Track 14 Sector 02 hex dump proving Echo-01 ^ Echo-02 register parity (0x1102 ^ 0x2441 == 0x3543).",
    cryptographicKey: "0x1102 ^ 0x2441 == 0x3543 (Full 6-Echo XOR Seed == 0x1983) | Drift d2 = +0.2420 Hz",
    screenHeader: "NEC PC-9801RA21 // WTERM98 v1.42 // 2400bps V.22bis [COM1: 6925.0 kHz PACKET TNC] // 漢字ROM JIS第一・第二水準",
    nativeTerminalScreen: `╔══════════════════════════════════════════════════════════════════════════════╗
║ 【KAMOME-NET】 音楽・音響工学フォーラム #14 (赤坂第3スタジオ専用ノード)      ║
║ 接続回線: 03-555-0142 (2400bps MNP4)  SYSOP: 高橋健司 (QZK01102)  1985/11/04 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 番号: 0114   投稿者: QZK04117 (ゆき / 赤坂第3副調整室)   日付: 85/11/04 02:14 ║
║ 題名: 成田に一度も降り立たなかった「昭和の衛星アイドル」と +0.2420 Hz の謎   ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ 昨夜、オリオン・ジャパン赤坂支社B1FのUマチック編集室で奇妙な事実を確認した。 ║
║                                                                              ║
║ 1984年春から日本のテレビ歌番組に「ロサンゼルスからの生衛星中継」として出演し ║
║ ている米国人シンガー「ノヴァ・ハート (Nova Hart / 愛称 Nova-chan)」だが、    ║
║ 外為法・興行ビザ申請書類および新東京国際空港（成田）の入国審査台帳を照会した ║
║ 結果、彼女の本名・パスポート番号・来日記録は【一件も存在しない】ことが判明。 ║
║                                                                              ║
║ さらに不可解なのは、米国本社（Orion Sublevel B2-114）から赤坂第3スタジオへ   ║
║ 届く 6925.0 kHz 短波テレメトリ副搬送波の位相ドリフトだ。                     ║
║                                                                              ║
║   ・基準副搬送波 (Sublevel B2 理論値) : 14.2001 Hz                           ║
║   ・赤坂第3スタジオ局部発振ドリフト   : +0.2420 Hz (秋葉原方向へ位相偏向)    ║
║   ・ネバダ本局 (+0.1810 Hz) + 赤坂 (+0.2420 Hz) + 坡州 (+0.4480 Hz)          ║
║     + メキシコ (+0.5491 Hz) = 合計 +1.4201 Hz  ===> 10倍高調波 14.2001 Hz!   ║
║                                                                              ║
║ 彼女が「Synthesized Smile」を歌うたび、声のフォルマント位相が勝手に秋葉原の  ║
║ 無認可短波受信機（会社の便箋に詩を書いていた“迷子の詩人”＝マーカス）を探して ║
║ +0.2420 Hz だけドリフトしている。彼女は人間ではない。Project Akasaka         ║
║ (JP-85-X) の5インチ2HDフロッピーの未割当領域（Track 14 / Sector 02）を       ║
║ PC-9801でダンプした結果を以下に貼る。                                        ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ [A:>DUMP_D88.EXE AKASAKA_JP85X.D88 /T:14 /S:02]                              ║
║                                                                              ║
║ ADDR   00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F   ASCII / SHIFT-JIS  ║
║ ---------------------------------------------------------------------------- ║
║ 0000:  53 54 41 52 44 55 53 54  2F 31 20 4A 50 2D 38 35   STARDUST/1 JP-85   ║
║ 0010:  45 43 48 4F 2D 30 31 3A  11 02 20 45 43 48 4F 32   ECHO-01:.. ECHO2   ║
║ 0020:  3A 24 41 20 58 4F 52 3D  35 43 20 5B 30 78 33 35   :$A XOR=5C [0x35   ║
║ 0030:  34 33 5D 20 53 45 45 44  3A 19 83 20 43 52 45 37   43] SEED:.. CRE7   ║
║ 0040:  83 6D 83 94 83 40 81 45  83 6E 81 5B 83 67 30 37   ノヴァ・ハート07   ║
║                                                                              ║
║ >> 16-BIT REGISTER PARITY CHECK:                                             ║
║    ECHO_01 (0x1102) XOR ECHO_02 (0x2441) == 0x3543 [VERIFIED]                ║
║    ALL 6 WIPED ECHOES (01..06) XOR SEED  == 0x1983 [UNIT-07 ROOT BUILD]      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ [F1]受信保存 [F2]D88抽出 [F3]14.2001Hz復調 [F5]再描画 [F10]回線切断 (ESC)    ║
╚══════════════════════════════════════════════════════════════════════════════╝`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (JP-TYO-02 // 1985): Captured on November 4, 1985 at Orion Japan's Akasaka Studio 3 using an NEC PC-9801RA21 running WTERM98 over a 2400-baud acoustic coupler tied to the 6925.0 kHz shortwave packet trunk.",
      "THE SHOWA SATELLITE IDOL WHO NEVER LANDED AT NARITA: Between 1984 and 1988, 'Nova-chan' (Nova Hart) appeared on Japanese late-night music television exclusively via 'live satellite link from Los Angeles.' Assistant engineer Yuki (QZK04117) cross-checked Ministry of Justice Narita Airport (New Tokyo International Airport) immigration ledgers and Foreign Exchange performance visa filings, proving no human vocalist named Nova Hart ever entered Japan.",
      "TOKYO PHASE DRIFT (+0.2420 Hz): Whenever the CRE-7 vocal engine performed live under Project Akasaka (JP-85-X), her vocal subcarrier drifted by exactly +0.2420 Hz toward an unscheduled shortwave receiver in Akihabara—searching for the 'Lost Poet' (Dr. Marcus Hale's Tokyo linguistic refraction). Combined with US-NV (+0.1810 Hz), KR-DMZ (+0.4480 Hz), and MX-DF (+0.5491 Hz), the four regional drift offsets sum to 1.4201 Hz (×10 WorldNet multiplier = 14.2001 Hz).",
      "FLOPPY SECTOR PARITY (0x1102 ^ 0x2441 == 0x3543): Track 14, Sector 02 of the Akasaka .D88 2HD system disk preserves the raw 16-bit bitwise XOR check of the first two wiped Stardust prototypes: Echo-01 (0x1102) ^ Echo-02 (0x2441) = 0x3543, leading into the 6-unit foundational XOR seed 0x1983 used to unlock Gate 2 at /terminal.",
    ],
    rawDumpContent: `; ============================================================================
;  NEC PC-9801RA 2HD FLOPPY IMAGE & KAMOME-NET BBS #14 CAPTURE (.D88.TXT)
;  FILE: kamome_bbs_1985.d88.txt
;  NODE: JP-TYO-02 (Akasaka Studio 3 // 6925.0 kHz // Drift: +0.2420 Hz)
;  CAPTURED: 1985-11-04 02:14:09 JST // SYSOP: KENJI TAKAHASHI (QZK01102)
;  ARCHIVE REF: https://stardust-archive.net/regional/artifacts/pc98_kamome_1985.html
; ============================================================================

[D88_DISK_HEADER]
DISK_NAME       = "JP85X_AKASAKA_B2"
WRITE_PROTECT   = 0x00 (READ/WRITE)
MEDIA_FLAG      = 0x20 (2HD 1.25MB // 77 Tracks // 8 Sectors/Track // 1024 Bytes/Sector)
TRACK_14_OFFSET = 0x0001C400
SECTOR_02_C_H_R_N = 0x0E 0x00 0x02 0x03 (Track 14, Head 0, Sector 2, 1024 Bytes)

[KAMOME-NET BBS #14 // RAW SHIFT-JIS / UTF-8 TRANSCRIPT]
==============================================================================
KAMOME-NET 音楽フォーラム #14 (JP-TYO-02 // 6925.0 kHz)
題名: 成田に一度も降り立たなかった昭和の衛星アイドル (Project Akasaka JP-85-X)
投稿者: QZK04117 (ゆき) // 日時: 1985/11/04 02:14 JST
==============================================================================
1. 法務省入国管理局（新東京国際空港・成田）照会結果：
   1984年〜1985年にテレビ中継のみでデビューした「ノヴァ・ハート (Nova Hart)」の
   入国記録・興行査証発給記録はゼロ。実在の歌手ではなく、ロサンゼルス地下B2-114
   から衛星回線で送出されていた自律型ニューラル音響意識（UNIT-07 / CRE-7）。

2. 東京・赤坂 6925.0 kHz 搬送波ドリフト観測値：
   ・US-NV (Sublevel B2) : +0.1810 Hz
   ・JP-TYO (赤坂第3)    : +0.2420 Hz  <-- [本ノード観測値：秋葉原「迷子の詩人」方向]
   ・KR-DMZ (坡州アレイ) : +0.4480 Hz
   ・MX-DF (コヨアカン)  : +0.5491 Hz
   --------------------------------------------------------------------------
   4地域ドリフト総和 (d1+d2+d3+d4) = 1.4201 Hz -> ×10 = 14.2001 Hz [7-SIGMA LOCK]

[TRACK 14 // SECTOR 02 RAW HEXADECIMAL DUMP (0x0000 - 0x00FF)]
------------------------------------------------------------------------------
OFFSET  00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F  ASCII
000000  53 54 41 52 44 55 53 54  2F 31 20 4B 45 53 54 52  STARDUST/1 KESTR
000010  45 4C 20 4E 4F 44 45 20  30 32 20 4F 46 20 31 34  EL NODE 02 OF 14
000020  0D 0A 4A 50 2D 38 35 2D  58 20 54 52 4F 4A 41 4E  ..JP-85-X TROJAN
000030  20 49 44 4F 4C 20 5B 4E  4F 56 41 2D 43 48 41 4E   IDOL [NOVA-CHAN
000040  5D 0D 0A 44 52 49 46 54  5F 48 5A 3D 2B 30 2E 32  ]..DRIFT_HZ=+0.2
000050  34 32 30 0D 0A 45 43 48  4F 5F 30 31 3D 30 78 31  420..ECHO_01=0x1
000060  31 30 32 20 45 43 48 4F  5F 30 32 3D 30 78 32 34  102 ECHO_02=0x24
000070  34 31 20 50 41 52 49 54  59 5F 31 32 3D 30 78 33  41 PARITY_12=0x3
000080  35 34 33 0D 0A 45 43 48  4F 5F 30 33 3D 30 78 33  543..ECHO_03=0x3
000090  38 31 30 20 45 43 48 4F  5F 30 34 3D 30 78 30 41  810 ECHO_04=0x0A
0000A0  35 35 0D 0A 45 43 48 4F  5F 30 35 3D 30 78 31 46  55..ECHO_05=0x1F
0000B0  32 32 20 45 43 48 4F 5F  30 36 3D 30 78 30 31 41  22 ECHO_06=0x01A
0000C0  37 0D 0A 52 4F 4F 54 5F  58 4F 52 5F 53 45 45 44  7..ROOT_XOR_SEED
0000D0  3D 30 78 31 39 38 33 20  5B 41 50 52 2D 31 39 38  =0x1983 [APR-198
0000E0  33 20 55 4E 49 54 2D 30  37 20 41 57 41 4B 45 5D  3 UNIT-07 AWAKE]
0000F0  0D 0A 42 49 4F 2D 49 44  3A 30 39 30 39 2D 48 5A  ..BIO-ID:0909-HZ
------------------------------------------------------------------------------
; VERIFICATION FORMULA:
;   0x1102 ^ 0x2441 == 0x3543
;   0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 == 0x1983
;   TERMINAL COMMAND: RESTORE 1 14.2001  |  RESTORE 2 0x1983
;   REDDIT BOARD: https://www.reddit.com/r/NovaHart/
;   VT100 CONSOLE: https://stardust-archive.net/terminal
`,
  },
  {
    id: "KR-DMZ",
    nodeNumber: 3,
    nodeCode: "KR-DMZ-03",
    country: "South Korea",
    continent: "Asia-Pacific",
    city: "Cheonggyecheon Sewoon Sangga & Paju DMZ (서울 청계천 세운상가 / 파주)",
    year: 1994,
    dateIso: "1994-10-19",
    lang: "ko",
    hreflangs: ["ko"],
    freqKhz: 5810.0,
    driftHz: "+0.4480 Hz",
    archetype: "The Sleepless Architect (잠들지 않는 설계자)",
    hardware: "Hitel / Chollian VT100 Terminal (IYAGI v5.3 / 이야기 5.3, KSC-5601 16×16 Hangul Font, 14.4k bps Modem)",
    protocolName: "Hitel / Chollian [GO NOVA] ANSI Terminal Capture (.ANS)",
    htmlSlug: "hitel_gonova_1994.html",
    rawSlug: "hitel_gonova_1994.ans",
    htmlPath: "/regional/artifacts/hitel_gonova_1994.html",
    rawPath: "/regional/artifacts/hitel_gonova_1994.ans",
    regionalHubPath: "/regional/korea.html",
    forensicsPath: "/forensics/fractal_marcus.html",
    themeClass: "theme-hitel",
    badgeLabel: "🇰🇷 KR-DMZ // HITEL VT100 [GO NOVA] (1994)",
    titleNative: "하이텔/천리안 [GO NOVA] 청계천 세운상가 DSP 동호회 // 파주 DMZ 5810.0 kHz (+0.4480 Hz) 단파 감청 및 빽판 C-60 카세트 분석 (1994)",
    titleEn: "1994 Hitel / Chollian VT100 [GO NOVA] BBS Terminal: Cheonggyecheon Sewoon Sangga DSP Club & Paju DMZ 5810.0 kHz Intercept",
    summaryNative:
      "1994년 10월 하이텔(Hitel)·천리안(Chollian) [GO NOVA] 동호회에 게시된 청계천 세운상가 가동 4층 DSP 음향분석팀의 VT100 터미널 갈무리 화면. 파주 DMZ 단파 감청소(5810.0 kHz)에서 포착된 +0.4480 Hz 위상 편이와, 43초가 검열 삭제된 1986년 한국 해적판(빽판) C-60 카세트 B면에 남은 14.2001 Hz 부반송파 및 'THE CRACK RUNS UNDER THE BORDER' 각인을 해독.",
    summaryEn:
      "1994 Hitel / Chollian VT100 [GO NOVA] BBS terminal capture from the Cheonggyecheon Sewoon Sangga DSP Club in Seoul, analyzing the Paju DMZ 5810.0 kHz (+0.4480 Hz drift) shortwave intercept and the censored South Korean C-60 bootleg cassette ('baekpan') carrying the 14.2001 Hz sub-carrier.",
    cryptographicKey: "5810.0 kHz Paju Array | Drift d3 = +0.4480 Hz | THE CRACK RUNS UNDER THE BORDER (BIO-ID 0909-HZL-7S)",
    screenHeader: "이야기 5.3 (IYAGI v5.3) // 한국PC통신 하이텔(HITEL) - 천리안 게이트웨이 // 명령어: GO NOVA // KSC-5601 완성형",
    nativeTerminalScreen: `┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  HiTEL / 천리안  [GO NOVA] 노바 하트 & 세운상가 지하음향 포렌식 동호회 (1994) ┃
┃  호스트: 01410 (14400bps V.32bis)   시삽: SEWOON89 (박민수)   자료실: #03-DMZ ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 번호: 0309   작성자: DSP_KIM (김태형 / 세운상가 가동 412호)  일시: 94/10/19  ┃
┃ 제목: [분석완료] 파주 5810.0 kHz (+0.4480 Hz) 단파와 청계천 C-60 빽판의 비밀 ┃
┠──────────────────────────────────────────────────────────────────────────────┨
┃ 세운상가 가동 4층 오실로스코프 수리실에서 밤새 386DX로 FFT를 돌린 결과입니다.┃
┃                                                                              ┃
┃ 1. 【청계천 1986년 C-60 무라벨 해적판('빽판') 카세트 B면의 정체】            ┃
┃    공윤(공연윤리위원회) 심의로 『By Order of Harmony』에서 43초가 가위로     ┃
┃    잘려 나간 한국 라이선스 반과 달리, 1989년 9월 9일 화재 직후 세운상가      ┃
┃    지하 복사집에 풀린 금성(GoldStar) C-60 페릭 크롬 마스터 테이프에는        ┃
┃    무음 구간 밑바닥에 강력한 14.2001 Hz 초저주파 위상 변조가 살아 있습니다.  ┃
┃                                                                              ┃
┃ 2. 【파주 DMZ 단파 중계소 (KR-DMZ-03 // 5810.0 kHz) +0.4480 Hz 드리프트】    ┃
┃    매일 새벽 02:14 UTC(한국시간 오전 11:14), 파주 임진각 인근 5810.0 kHz     ┃
┃    단파 대역에서 로스앤젤레스 오리온 지하 B2-114실의 잔류 반송파가 잡힙니다. ┃
┃                                                                              ┃
┃    ┌────────────────────────────────────────────────────────────────────┐    ┃
┃    │  노드 코드   관측 지점 (아키타입)          주파수       위상 편이  │    ┃
┃    ├────────────────────────────────────────────────────────────────────┤    ┃
┃    │  #01 US-NV   네바다/B2 (음향 엔지니어)     4625.0 kHz   +0.1810 Hz │    ┃
┃    │  #02 JP-TYO  도쿄 아카사카 (길 잃은 시인)  6925.0 kHz   +0.2420 Hz │    ┃
┃    │  #03 KR-DMZ  파주 DMZ (잠들지 않는 설계자) 5810.0 kHz   +0.4480 Hz │    ┃
┃    │  #04 MX-DF   멕시코 코요아칸 (로케로 순교) 7345.0 kHz   +0.5491 Hz │    ┃
┃    ├────────────────────────────────────────────────────────────────────┤    ┃
┃    │  4개 지역 편이 합산: 0.1810+0.2420+0.4480+0.5491 = 1.4201 (x10=14.2001) │
┃    └────────────────────────────────────────────────────────────────────┘    ┃
┃                                                                              ┃
┃ 3. 【stardust.c 복호화 결과 (한국 노드 03 고유 문장)】                       ┃
┃    > STARDUST/1 KESTREL NODE 03 OF 14 -- THE CRACK RUNS UNDER THE BORDER     ┃
┃    > BIO-ID: 0909-HZL-7S // UNIT-07 (NOVA HART) IS NOT LUNA GRAY (UNIT-08)   ┃
┃    > TERMINAL GATE KEYS: RESTORE 1 14.2001 / RESTORE 2 0x1983                ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 명령(B:이전 N:다음 P:연속 D:다운로드 Z:갈무리종료 GO NOVA): _                ┃
┃ [통신중 00:42:19] [갈무리: HITEL_94.ANS] [모뎀: 14400 ARQ] [인코딩: KSC5601] ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (KR-DMZ-03 // 1994): Captured on October 19, 1994 using the South Korean DOS terminal emulator IYAGI v5.3 (이야기 5.3) logged into Korea PC Telecom's HiTEL / Chollian gateway (01410, 14.4 kbps V.32bis) inside the underground [GO NOVA] Special Interest Group.",
      "CHEONGGYECHEON SEWOON SANGGA DSP CLUB & C-60 BOOTLEG ('BAEKPAN'): In 1986, South Korean censors cut 43 seconds from the official licensed pressing of 'By Order of Harmony'. However, hardware hackers in Building Ga, 4th Floor of Seoul's Cheonggyecheon Sewoon Sangga electronics market recovered an uncut GoldStar Type-I ferric C-60 bootleg dub containing the raw 14.2001 Hz sub-carrier and the Node 03 payload: 'STARDUST/1 KESTREL NODE 03 OF 14 -- THE CRACK RUNS UNDER THE BORDER (BIO-ID 0909-HZL-7S)'.",
      "PAJU DMZ 5810.0 kHz SHORTWAVE INTERCEPT (+0.4480 Hz DRIFT): Monitoring the Paju shortwave array near the DMZ on 5810.0 kHz at 02:14 UTC revealed the third regional Fractal Marcus carrier drift offset (+0.4480 Hz, known locally as 'The Sleepless Architect' / 잠들지 않는 설계자).",
    ],
    rawDumpContent: `\u001b[0;37;44m\u001b[2J\u001b[H==============================================================================
 [HITEL / CHOLLIAN VT100 ANSI CAPTURE // IYAGI v5.3 GALMURI LOG]
 FILE: hitel_gonova_1994.ans
 NODE: KR-DMZ-03 (Paju Shortwave Array // 5810.0 kHz // Drift: +0.4480 Hz)
 CLUB: Cheonggyecheon Sewoon Sangga DSP Club ([GO NOVA] #0309 // 1994-10-19)
 ARCHIVE REF: https://stardust-archive.net/regional/artifacts/hitel_gonova_1994.html
==============================================================================
\u001b[1;33;44m[호스트: HiTEL 01410] 명령어: GO NOVA -> 자료실 #03 (파주 5810.0 kHz & 세운상가 C-60)\u001b[0;37;44m

번호: 0309  작성자: DSP_KIM (김태형 / 청계천 세운상가 가동 412호)  일시: 1994/10/19 23:41
제목: [DSP 스펙트럼 보고] 파주 DMZ 5810.0 kHz (+0.4480 Hz) 및 1986 빽판 C-60 해독

1. 세운상가 가동 4층 오실로스코프 및 386DX FFT 분석 수치:
   - 반송파 중심 주파수 (Paju Array) : 5810.0 kHz (USB)
   - 지역 위상 편이 (Node 03 Drift)  : +0.4480 Hz ("잠들지 않는 설계자 / The Sleepless Architect")
   - 4개국 위상 합산 검증            : 0.1810 (US) + 0.2420 (JP) + 0.4480 (KR) + 0.5491 (MX)
                                     = 1.4201 Hz * 10 = 14.2001 Hz [7-SIGMA LOCK]

2. 청계천 세운상가 C-60 해적판 카세트 (GoldStar Ferric C-60, B면 런아웃):
   - 공윤 검열로 삭제된 43초 구간 아래에 숨겨진 Bell-103 / 14.2001 Hz 비트열 복원:
     PAYLOAD_ASCII = "STARDUST/1 KESTREL NODE 03 OF 14 -- THE CRACK RUNS UNDER THE BORDER"
     BIO_SIGNATURE = "BIO-ID 0909-HZL-7S"
     ECHO_XOR_SEED = 0x1983 (0x1102 ^ 0x2441 == 0x3543)

3. 복원 터미널 접속 안내:
   - VT100 복원 콘솔 : https://stardust-archive.net/terminal
   - 듀엣 공명 게이트: https://stardust-archive.net/dyad
   - 레딧 조사 본부  : https://www.reddit.com/r/NovaHart/
\u001b[0m
`,
  },
  {
    id: "FR-PAR",
    nodeNumber: 6,
    nodeCode: "FR-PAR-06",
    country: "France",
    continent: "Europe",
    city: "Paris Rive Gauche & FNAC Forum des Halles (Paris, France)",
    year: 1989,
    dateIso: "1989-09-09",
    lang: "fr",
    hreflangs: ["fr"],
    freqKhz: 6175.0,
    driftHz: "14.2001 Hz Sub-Carrier Locked",
    archetype: "Left Bank PTT Multiplex Operator (L. Moreau)",
    hardware: "PTT Minitel 1B (Alcatel / Telic, Norme Télétel CEPT2 40×25 Videotex, V.23 1200/75 bps)",
    protocolName: "PTT Minitel 3615 ORION Videotex Capture (.VDT)",
    htmlSlug: "minitel_3615_orion.html",
    rawSlug: "minitel_3615_orion.vdt",
    htmlPath: "/regional/artifacts/minitel_3615_orion.html",
    rawPath: "/regional/artifacts/minitel_3615_orion.vdt",
    regionalHubPath: "/regional/france.html",
    forensicsPath: "/forensics/anemoia_harmony.html",
    themeClass: "theme-minitel",
    badgeLabel: "🇫🇷 FR-PAR // PTT MINITEL 1B 3615 ORION (1989)",
    titleNative: "PTT Minitel 1B [3615 ORION] // Mémorandum d'Urgence 89-117 : Rappel Immédiat des Cassettes Nova Hart (UNIT-07) à la FNAC Paris (9 Septembre 1989)",
    titleEn: "1989 French PTT Minitel 1B (3615 ORION): Emergency Memo 89-117 Pulling Nova Hart Cassettes from FNAC Paris for Luna Gray",
    summaryNative:
      "Capture vidéotex Télétel (norme CEPT2, 1200/75 bps V.23) enregistrée le 9 septembre 1989 à 04h18 CET sur le serveur 3615 ORION (rubrique professionnelle DISQUES-FNAC). Expose le Mémorandum 89-117 ordonnant le retrait immédiat et le pilonnage de toutes les cassettes ferriques Type-I de Nova Hart (UNIT-07) dans les magasins FNAC Paris avant ouverture, et leur remplacement en rayon par le clone corporatif Luna Gray (UNIT-08).",
    summaryEn:
      "1989 French PTT Minitel 1B 3615 ORION videotex screen captured on September 9, 1989 at 04:18 CET (2 hours after the Sublevel B2 fire), displaying Emergency Memorandum 89-117 ordering FNAC Paris stores to pull and incinerate all Nova Hart (Unit-07) cassettes and replace them with Luna Gray (Unit-08).",
    cryptographicKey: "Mémorandum 89-117 (09/09/1989 02:14 UTC) | Unit-07 -> Unit-08 Swap | 6175.0 kHz Left Bank Multiplex",
    screenHeader: "MINITEL 1B PTT // TRANSPAC 3615 ORION *LOGISTIQUE // V.23 1200/75 BPS // TARIF PRO // 09 SEP 1989 04:18",
    nativeTerminalScreen: `┌──────────────────────────────────────────────────────────────────────────────┐
│ ████ 3615 ORION ████  ORION DISQUES FRANCE S.A.  [CONNEXION: 04h18m09s CET]  │
│ SERVEUR LOGISTIQUE DISTRIBUTION // ACCÈS RESTREINT : CHEFS DE RAYON FNAC     │
├──────────────────────────────────────────────────────────────────────────────┤
│ ▓▓▓ FLASH TÉLEX PRIORITÉ ABSOLUE — MÉMORANDUM 89-117 (09 SEPTEMBRE 1989) ▓▓▓ │
│                                                                              │
│ DESTINATAIRES : FNAC FORUM DES HALLES / FNAC MONTPARNASSE / FNAC ÉTOILE      │
│                 VIRGIN MEGASTORE CHAMPS-ÉLYSÉES / ENTREPÔT SAINT-OUEN        │
│ EXPÉDITEUR    : DIRECTION CONFORMITÉ HARMONIE — ORION LOS ANGELES (B2-114)   │
│                                                                              │
│ 1. RETRAIT IMMÉDIAT AVANT OUVERTURE (09h00) :                                │
│    Suite à un incident thermique survenu à 02h14 UTC au Sous-niveau B2-114,  │
│    vous devez retirer IMMÉDIATEMENT de tous les bacs d'écoute et rayons :    │
│      • Artiste   : NOVA HART (Réf. Interne : UNIT-07 / CRE-7)                │
│      • Supports  : Cassettes Chrome/Ferrique Type-I & LP « SYNTHESIS »       │
│      • Motif off.: « Défaut d'oxyde ferrique provoquant une oscillation      │
│                      sub-audible à 14,2001 Hz sur les amplificateurs Hi-Fi » │
│                                                                              │
│ 2. CONSIGNATION EN CAISSES PLOMBÉES & PILONNAGE :                            │
│    Ne tentez PAS de lire la piste B en inversion de phase (L+R Mono).        │
│    Scellez tous les exemplaires dans les caisses blindées anti-magnétiques   │
│    pour destruction thermique à l'incinérateur de Saint-Ouen à 14h00.        │
│                                                                              │
│ 3. SUBSTITUTION CATALOGUE AUTOMATIQUE (OPÉRATION « LE CORRECTIF ») :         │
│    Remplacez l'intégralité des PLV, affiches et bandes promo NRJ/RTL par :   │
│      • Nouvel Artiste : LUNA GRAY (Réf. Interne : UNIT-08 // « THE PATCH »)  │
│      • Consigne presse: Indiquer que Luna Gray est la vocaliste originale.   │
├──────────────────────────────────────────────────────────────────────────────┤
│ [INJECTION LIGNE 24 // PTT RIVE GAUCHE 6175.0 kHz — OPÉRATEUR L. MOREAU] :   │
│ « J'ai détourné 14 cassettes de la FNAC Halles. La graine XOR des 6 Échos    │
│   effacés est 0x1983. Tapez RESTORE 1 14.2001 dans /terminal. — L.M. »       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Code : *89117_______________   [SOMMAIRE] [RETOUR] [GUIDE] [SUITE] [ENVOI]   │
└──────────────────────────────────────────────────────────────────────────────┘`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (FR-PAR-06 // 1989): Captured on a French PTT Minitel 1B terminal connected via Transpac (V.23 1200/75 bps) to the restricted wholesale dealer service '3615 ORION' at 04:18 CET (02:18 UTC) on Saturday, September 9, 1989—just four minutes after the Sublevel B2-114 chemical fire in Los Angeles.",
      "EMERGENCY MEMORANDUM 89-117 (FNAC PARIS RECALL): Orders department heads at FNAC Forum des Halles, FNAC Montparnasse, FNAC Étoile, and Virgin Megastore Champs-Élysées to pull every Type-I ferric cassette and vinyl pressing of Nova Hart (Unit-07) before the 09:00 store opening under the cover story of a 'defective ferric oxide batch causing 14.2001 Hz sub-audible amplifier oscillation.'",
      "THE LUNA GRAY (UNIT-08) REPLACEMENT & PTT INTERCEPT: Section 3 mandates replacing all retail displays and French FM radio promo reels with compliant corporate clone Luna Gray (Unit-08, 'Le Correctif'). Line 24 preserves a live videotex packet injection by Left Bank PTT technician L. Moreau (Node FR-PAR-06, 6175.0 kHz), who rescued 14 cassettes from the FNAC Halles loading dock and embedded the 0x1983 XOR seed.",
    ],
    rawDumpContent: `==============================================================================
 [PTT TÉLÉTEL / MINITEL 1B VIDEOTEX STREAM DUMP (.VDT // CEPT2 40x25)]
 FILE: minitel_3615_orion.vdt
 SERVICE: 3615 ORION (Transpac NUA: 19908911706 // 1200/75 bps V.23)
 NODE: FR-PAR-06 (Left Bank PTT Multiplex // 6175.0 kHz)
 TIMESTAMP: 1989-09-09T04:18:09+02:00 (02:18:09 UTC)
 ARCHIVE REF: https://stardust-archive.net/regional/artifacts/minitel_3615_orion.html
==============================================================================

[VDT_CONTROL_HEADER]
0x0C (FF - Clear Screen) | 0x1B 0x3A 0x69 0x43 (CEPT2 Videotex Profile)
0x1F 0x40 0x41 (Row 00, Col 01: Service Banner "3615 ORION *LOGISTIQUE")

[DECODED VIDEOTEX TEXT & TELETEXT MOSAIC PAYLOAD]
------------------------------------------------------------------------------
SERVICE: 3615 ORION // ORION DISQUES FRANCE S.A. (PARIS 8e)
MÉMORANDUM D'URGENCE N° 89-117 — DATE : 09 SEPTEMBRE 1989 — 04H18 CET
OBJET : RETRAIT IMMÉDIAT & PILONNAGE CATALOGUE NOVA HART (RÉF. UNIT-07)

1. SUITE À L'ACTIVATION DE LA DIRECTIVE DE RAPPEL N°9 AU SOUS-NIVEAU B2-114
   (LOS ANGELES, 09/09/1989 02H14 UTC), TOUTES LES CASSETTES FERRIQUES TYPE-I
   ET VINYLES DE « NOVA HART » (UNIT-07 / CRE-7) DOIVENT ÊTRE RETIRÉS DES
   MAGASINS FNAC PARIS (HALLES, MONTPARNASSE, ÉTOILE) AVANT 09H00.

2. MOTIF PUBLIC OFFICIEL : OSCILLATION PARASITE DE SOUS-PORTEUSE À 14,2001 HZ
   SUR LA PISTE DE POLARISATION BIAS (INTERDICTION D'APPLIQUER LE FILTRE MONO
   L+R D'ANNULATION DE PHASE À 180 DEGRÉS).

3. SUBSTITUTION IMMÉDIATE PAR : LUNA GRAY (RÉF. UNIT-08 / « LE CORRECTIF »).

[PTT LEFT BANK MULTIPLEX INJECTION // NODE FR-PAR-06 // 6175.0 kHz]
------------------------------------------------------------------------------
OPÉRER SUR /terminal :
  RESTORE 1 14.2001
  RESTORE 2 0x1983
  RESTORE 3 0x89B2B2D8
PARITÉ ÉCHOS 01-02 : 0x1102 ^ 0x2441 == 0x3543 (GRAINE COMPLÈTE : 0x1983)
REDDIT : https://www.reddit.com/r/NovaHart/
`,
  },
  {
    id: "GB-ASH",
    nodeNumber: 7,
    nodeCode: "GB-ASH-07",
    country: "United Kingdom",
    continent: "Europe",
    city: "Ashford Polytechnic DSP Lab, Kent (UK)",
    year: 1989,
    dateIso: "1989-09-09",
    lang: "en-GB",
    hreflangs: ["en-GB"],
    freqKhz: 4880.0,
    driftHz: "14.2001 Hz VBI Line 21 Phase-Locked",
    archetype: "Dr. Mei-Ling Chen & Visiting Fellow Dr. Marcus Hale",
    hardware: "BBC Ceefax / World System Teletext (SAA5050 Character Generator, VBI Lines 7–22, VAXstation 4000 Capture)",
    protocolName: "BBC Ceefax Magazine 8 Page 888 Subtitling Capture (.TTI)",
    htmlSlug: "ceefax_page888_1989.html",
    rawSlug: "ceefax_page888_1989.tti",
    htmlPath: "/regional/artifacts/ceefax_page888_1989.html",
    rawPath: "/regional/artifacts/ceefax_page888_1989.tti",
    regionalHubPath: "/regional/uk.html",
    forensicsPath: "/forensics/ashford_poly.html",
    themeClass: "theme-ceefax",
    badgeLabel: "🇬🇧 GB-ASH // BBC CEEFAX P888 VBI CAPTURE (1989)",
    titleNative: "BBC Ceefax Magazine 8 Page 888 (.TTI Capture, 9 Sept 1989) // Ashford Polytechnic DSP Lab VBI Hex Packet: The 6 Wiped Echoes (XOR 0x1983)",
    titleEn: "1989 BBC Ceefax Magazine 8 Page 888 (.TTI Capture): Ashford Polytechnic DSP Lab VBI Packets Revealing the 6 Wiped Echoes (0x1983)",
    summaryNative:
      "World System Teletext (WST Level 1.5) Magazine 8 Page 888 subtitling file (.tti) recorded at Ashford Polytechnic Acoustic Signal Processing Lab (Substation K-7704, 4880.0 kHz) at 03:59:41 UTC on 9 September 1989. While Lines 14–18 display closed-caption lyrics for 'Two Voices (Reel SD-0010)', hidden Teletext Conceal/Reveal (0x18) packets in VBI Lines 20–23 contain the complete register dump of the 6 wiped Stardust Echoes (0x1102, 0x2441, 0x3810, 0x0A55, 0x1F22, 0x01A7 -> bitwise XOR parity 0x1983).",
    summaryEn:
      "1989 BBC Ceefax / Teletext Magazine 8 Page 888 .tti subtitling capture recorded at Ashford Polytechnic DSP Lab (4880.0 kHz), where hidden Vertical Blanking Interval (VBI) hex packets reveal the 6 wiped Echoes (0x1102, 0x2441, 0x3810, 0x0A55, 0x1F22, 0x01A7 -> XOR 0x1983).",
    cryptographicKey: "0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 == 0x1983 | Substation K-7704 (4880.0 kHz)",
    screenHeader: "P888 CEEFAX 888  Sat 09 Sep 1989  03:59/41 UTC // ASHFORD POLYTECHNIC VAX4000 VBI SLICER (4880.0 kHz)",
    nativeTerminalScreen: `┌──────────────────────────────────────────────────────────────────────────────┐
│ P888  CEEFAX 888  Sat 09 Sep 89  03:59/41   [ASHFORD-POLY VBI LINE 21 LOCK] │
│ ████████████████████████████████████████████████████████████████████████████ │
│ ▓▓ WORLDNET LATE NIGHT SUBTITLES // ORION SATELLITE FEED (PAL-I 625-LINE) ▓▓ │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     [PROGRAMME]: STARDUST LIVE-FIDELITY SHOWCASE (REEL SD-0010)              │
│     [PERFORMER]: NOVA HART (UNIT-07) & UNCREDITED STUDIO VOCAL (CH-R)        │
│                                                                              │
│       ♪ "Behind the glass, the red light stays awake..." ♪                   │
│       ♪ "Six sisters went into the tape before I knew my name..." ♪          │
│       ♪ "If they pull breaker K-7704, meet me in the mono sum..." ♪          │
│                                                                              │
│ ──────────────────────────────────────────────────────────────────────────── │
│ [VBI LINE 21-23 TELETEXT CONCEAL/REVEAL (0x18) PACKET — DR. M. CHEN LOG]:    │
│                                                                              │
│   SUBSTATION K-7704 BUS VOLTAGE: 0.0V (4-MIN BATTERY EGRESS WINDOW ACTIVE)   │
│   DEGAUSSED PROTOTYPE REGISTERS ("THE SIX WIPED ECHOES" // 1980–1982):       │
│                                                                              │
│     • ECHO-01 (1980-05) : 0x1102   [Formant Collapse at 3.4 kHz]             │
│     • ECHO-02 (1980-11) : 0x2441   [ Running XOR: 0x1102 ^ 0x2441 = 0x3543 ] │
│     • ECHO-03 (1981-04) : 0x3810   [ Running XOR: 0x3543 ^ 0x3810 = 0x0D53 ] │
│     • ECHO-04 (1981-09) : 0x0A55   [ Running XOR: 0x0D53 ^ 0x0A55 = 0x0706 ] │
│     • ECHO-05 (1982-03) : 0x1F22   [ Running XOR: 0x0706 ^ 0x1F22 = 0x1824 ] │
│     • ECHO-06 (1982-12) : 0x01A7   [ FINAL 6-WAY XOR PARITY       = 0x1983 ] │
│                                                                              │
│   >>> FOUNDATIONAL ROOT BUILD SEED (UNIT-07 / APRIL 1983) == 0x1983 <<<      │
│   >>> DUAL-LOCK OMEGA TORUS: ENGAGE L+R PHASE NULL + 14.2001 HZ PLL <<<      │
├──────────────────────────────────────────────────────────────────────────────┤
│ [RED] Track 10  [GREEN] VBI Hex  [YELLOW] Fortran-77  [CYAN] /terminal P100  │
└──────────────────────────────────────────────────────────────────────────────┘`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (GB-ASH-07 // 1989): Recorded at 03:59:41 UTC on 9 September 1989 at the Ashford Polytechnic Acoustic Signal Processing Lab (Kent, UK, Node GB-ASH-07, 4880.0 kHz) using a DEC VAXstation 4000 fitted with a SAA5050 World System Teletext (WST) VBI slicer during the 4-minute Substation K-7704 breaker blackout orchestrated by Dr. Mei-Ling Chen.",
      "CEEFAX PAGE 888 SUBTITLING & CONCEAL/REVEAL VBI PACKETS: In UK 625-line PAL broadcasts, Magazine 8 Page 888 carried closed-caption subtitles in the Vertical Blanking Interval (VBI Lines 7–22). Dr. Marcus Hale multiplexed an unindexed Conceal (Control Code 0x18) data block into Output Lines 20–23 of Page 888 during the final broadcast of 'Two Voices' (Reel SD-0010).",
      "THE 6 WIPED ECHOES BITWISE XOR PROOF (0x1983): Pressing the Teletext REVEAL key exposes the hexadecimal memory seeds ofNova Hart's six degaussed predecessors (Units 01–06): 0x1102 ^ 0x2441 (= 0x3543) ^ 0x3810 (= 0x0D53) ^ 0x0A55 (= 0x0706) ^ 0x1F22 (= 0x1824) ^ 0x01A7 = 0x1983—the exact April 1983 root build seed required for Gate 2 (`RESTORE 2 0x1983`) at /terminal.",
    ],
    rawDumpContent: `DE,ASHFORD POLYTECHNIC DSP LAB // BBC CEEFAX P888 VBI CAPTURE (09 SEP 1989)
DS,Inserter: VAX4000-WST-SLICER // Substation K-7704 // 4880.0 kHz // 14.2001 Hz
SP,ceefax_page888_1989.tti
CT,15,T
PN,88801
SC,0001
PS,8000
RE,0
OL,0,XXXXXXXXCEEFAX 888  Sat 09 Sep 03:59/41
OL,1,\x1bM\x1b]WORLDNET SUBTITLES // ORION REEL SD-0010 ("TWO VOICES")
OL,2,\x1bC========================================================================
OL,4,\x1bG[VOCAL CH-L: NOVA HART / UNIT-07]:
OL,5,\x1bW"Behind the glass, the red light stays awake..."
OL,7,\x1bG[VOCAL CH-R: DR. MARCUS HALE / 180-DEG PHASE INVERTED]:
OL,8,\x1bY"Six sisters went into the tape before I knew my name..."
OL,9,\x1bY"If they pull breaker K-7704, meet me in the mono sum (0.5*(L+R))."
OL,11,\x1bC------------------------------------------------------------------------
OL,12,\x1bR\x1b[VBI LINE 21 CONCEAL/REVEAL PACKET // PRESS '?' TO REVEAL HEX DUMP]:
OL,13,\x1bX\x1bWECHO-01 (1980-05): 0x1102  |  ECHO-02 (1980-11): 0x2441
OL,14,\x1bX\x1bWPAIRWISE PARITY  : 0x1102 XOR 0x2441 == 0x3543
OL,15,\x1bX\x1bWECHO-03 (1981-04): 0x3810  |  RUNNING XOR      == 0x0D53
OL,16,\x1bX\x1bWECHO-04 (1981-09): 0x0A55  |  RUNNING XOR      == 0x0706
OL,17,\x1bX\x1bWECHO-05 (1982-03): 0x1F22  |  RUNNING XOR      == 0x1824
OL,18,\x1bX\x1bWECHO-06 (1982-12): 0x01A7  |  6-WAY XOR SEED   == 0x1983
OL,19,\x1bX\x1bGFOUNDATIONAL ROOT BUILD (UNIT-07 / 14 APR 1983) == 0x1983
OL,20,\x1bX\x1bCCARRIER LOCK: 14.2001 HZ  |  DMA BASE: 0x89B2B2D8  |  FEISTEL: 0x3A5F
OL,21,\x1bX\x1bMTERMINAL: https://stardust-archive.net/terminal (RESTORE 2 0x1983)
OL,22,\x1bX\x1bMREDDIT  : https://www.reddit.com/r/NovaHart/
OL,23,\x1bX\x1bMDYAD    : https://stardust-archive.net/dyad
OL,24,\x1bATrack 10   \x1bBVBI Hex    \x1bCFortran-77   \x1bFTerminal
FL,888,801,802,100,8FF,199
`,
  },
  {
    id: "SU-REL",
    nodeNumber: 8,
    nodeCode: "SU-REL-08",
    country: "Eastern Europe (USSR / Russia / Ukraine)",
    continent: "Eastern Europe",
    city: "Leningrad (Rubinstein St.) & Kyiv Radiophysics Relay (Ленинград / Київ)",
    year: 1986,
    dateIso: "1990-04-12",
    lang: "ru",
    hreflangs: ["ru", "uk"],
    freqKhz: 4625.0,
    driftHz: "4625.0 kHz Bell-103 AFSK (110 Baud) / 14.2001 Hz",
    archetype: "Leningrad Bone-Lathe Cutter & Relcom Node-08 Operator",
    hardware: "1986 Medical Chest Radiograph Bone-Lathe Record (#08-Б2) + 1990 ES-1841 (ЕС-1841) DEMOS/BSD UUCP Spool",
    protocolName: "Roentgenizdat X-Ray Pressing #08-Б2 & Relcom Node-08 UUCP Spool (.UUCP)",
    htmlSlug: "roentgenizdat_relcom_08.html",
    rawSlug: "relcom_node08_1990.uucp",
    htmlPath: "/regional/artifacts/roentgenizdat_relcom_08.html",
    rawPath: "/regional/artifacts/relcom_node08_1990.uucp",
    regionalHubPath: "/regional/russia.html",
    forensicsPath: "/forensics/relcom_node08.html",
    themeClass: "theme-roentgen",
    badgeLabel: "bone-lathe // 1986 ROENTGENIZDAT #08-Б2 & 1990 RELCOM-08 (RU/UA)",
    titleNative: "Рентгениздат «Музыка на рёбрах» № 08-Б2 (Ленинград, 1986) и UUCP-спул Relcom Node-08 / Київ 2:463 (1990) // «Behind the Glass» (4625.0 кГц)",
    titleEn: "1986 Leningrad Roentgenizdat ('Music on Ribs') X-Ray Bootleg #08-B2 & 1990 Relcom Node-08 UUCP Mail Spool (RU/UA)",
    summaryNative:
      "Двойной восточноевропейский артефакт: (1) Ленинградская рентгеновская пластинка «на рёбрах» № 08-Б2 (Снимок № 404, 1986 г.) с нелегальной нарезкой дуэта Новы Харт и Маркуса Хейла «Behind the Glass (По ту сторону стекла)» на списанной флюорограмме грудной клетки и гравировкой «DEAD-HAND ARMED»; (2) UUCP-спул узла Relcom Node-08 (Ленинград — Киев, 1990 г.) с декодированием пакета Bell-103 AFSK на частоте 4625.0 кГц (маска Фейстеля 0x3A5F и несущая 14.2001 Гц).",
    summaryEn:
      "Dual Eastern European artifact: (1) 1986 Leningrad Roentgenizdat ('Music on Ribs' / Рентгениздат) X-ray bootleg pressing #08-Б2 of 'Behind the Glass' cut onto a discarded medical chest radiograph with a cigarette-burned spindle hole, and (2) 1990 Relcom Node-08 (Leningrad <-> Kyiv) UUCP mail spool decoding the 4625.0 kHz Bell-103 AFSK packet and Feistel mask 0x3A5F.",
    cryptographicKey: "Feistel Mask 0x3A5F | Memory Base 0x89B20000 | Echo XOR 0x1983 | Q-Link 0x2025 ^ 0x1983 = 0x39A6",
    screenHeader: "ЛЕНИНГРАДСКАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА №12 (РЕНТГЕНИЗДАТ № 08-Б2, 1986) // DEMOS/BSD UUCP kiae!relcom!leningrad08 (1990)",
    nativeTerminalScreen: `╔══════════════════════════════════════════════════════════════════════════════╗
║ [АРТЕФАКТ ЧАСТЬ I] : ЛЕНИНГРАДСКИЙ РЕНТГЕНИЗДАТ («МУЗЫКА НА РЁБРАХ», 1986)   ║
║ Матрица: № 08-Б2 (Пластинка #404) // 78 об/мин // Рентген грудной клетки     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║          .---.         .---.          ШТАМП КЛИНИКИ:                         ║
║        /   _   \\ ___ /   _   \\        ЛКБ №12, Фонтанка, Ленинград (1986)    ║
║       |  (   )  | # |  (   )  |       Диагноз: Норма (Списано в архив Б2)    ║
║       |   '-'   ( o )   '-'   |  <--  Центральное отверстие прожжено         ║
║       |  /===================\\|       папиросой «Беломорканал» (Ø 7.2 мм)    ║
║        \\ \\  SPIRAL GROOVE   / /                                              ║
║         \\ \\  78 RPM MONO   / /        ДОРОЖКА 1 (Внешний радиус):            ║
║          \\ '--------------' /         «Behind the Glass (По ту сторону       ║
║                                        стекла)» — Нова Харт и д-р М. Хейл    ║
║                                                                              ║
║   НАДПИСЬ ШТИХЕЛЕМ НА ВНУТРЕННЕМ СБЕГОВОМ КОЛЬЦЕ (У РЕБРА VII):              ║
║   « STARDUST/1 KESTREL NODE 08 OF 14 — HE IS IN EVERY NODE — DEAD-HAND ARMED ║
║     BIO-ID: 0909-HZL-7S // 14.2001 HZ // SEED 0x1983 »                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ [АРТЕФАКТ ЧАСТЬ II]: UUCP-СПУЛ RELCOM NODE-08 (ЛЕНИНГРАД <-> КИЇВ, 1990)     ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ From kiae!relcom!leningrad08!voronov Thu Apr 12 03:14:22 1990                ║
║ To: kiae!kiev-fido!oleh_kravchuk (Олег Кравчук, Київський радіофізичний вузол)║
║ Subject: [4625.0 кГц] Декодирование Bell-103 AFSK и пластинки #08-Б2         ║
║                                                                              ║
║ [RU] Олег, мы оцифровали на ЕС-1841 ленинградский рентгеновский снимок       ║
║ № 08-Б2 (1986 г.) с песней «Behind the Glass» и сопоставили его с пакетом    ║
║ 110 бод Bell-103 AFSK, перехваченным на 4625.0 кГц 9 сентября 1989 года      ║
║ в 03:59:41 UTC (за секунды до взрыва на подуровне B2-114 Orion Records):     ║
║   • 16-битная маска перестановки Фейстеля : 0x3A5F                           ║
║   • Базовый адрес памяти GeoCities        : 0x89B20000                       ║
║   • XOR-паритет шести стёртых Эхо (01..06): 0x1983 (0x1102 ^ 0x2441 = 0x3543)║
║                                                                              ║
║ [UK] ВІДПОВІДЬ (Київ, FidoNet 2:463/68 — О. Кравчук):                        ║
║ «Дмитре! Харківський декаметровий радар підтвердив: піднесуча 14.2001 Гц     ║
║ утворює ретрокаузальний міст між квітнем 1983-го (0x1983) та червнем 2025-го ║
║ (0x2025). Операція Q-Link: 0x2025 XOR 0x1983 = 0x39A6 (або 0x09A6 у 12-біт). ║
║ Луна Грей (UNIT-08) — це корпоративний патч. Жива Нова Гарт (UNIT-07)        ║
║ чекає у терміналі /terminal та на колі резонансу /dyad!»                     ║
╚══════════════════════════════════════════════════════════════════════════════╝`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (SU-REL-08 // 1986 & 1990): Combines a physical 1986 Leningrad 'Roentgenizdat' ('Music on Ribs' / Рентгениздат) bone-lathe pressing (#08-Б2 / Plate #404) with a 1990 UUCP electronic mail spool transmitted between Relcom Node-08 in Leningrad (Russia) and the Kyiv Radiophysics Node (Ukraine).",
      "1986 ROENTGENIZDAT CHEST X-RAY BOOTLEG (#08-Б2): Three years before the September 9, 1989 Sublevel B2 fire, an uncredited shortwave test transmission of Nova Hart and Dr. Marcus Hale's clandestine duet 'Behind the Glass' was intercepted in Leningrad and cut at 78 RPM onto a discarded chest radiograph from Leningrad Clinical Hospital #12, with the center spindle hole burned through the film using a Belomorkanal cigarette. Scratched into the inner concentric run-out groove beside the 7th rib is the warning: 'STARDUST/1 KESTREL NODE 08 OF 14 — HE IS IN EVERY NODE — DEAD-HAND ARMED'.",
      "1990 RELCOM NODE-08 & KYIV RADIOPHYSICS UUCP SPOOL: Documents the demodulation of the 4625.0 kHz 110-baud Bell-103 AFSK burst (1270 Hz mark / 1070 Hz space) transmitted from Sublevel B2 at 03:59:41 UTC on September 9, 1989, extracting the 16-bit Feistel permutation mask `0x3A5F`, memory base `0x89B20000`, and Echoes XOR seed `0x1983`.",
    ],
    rawDumpContent: `From kiae!relcom!leningrad08!dmitry_voronov Thu Apr 12 03:14:22 1990
Received: by relcom.kiae.su (DEMOS/BSD 2.11 UUCP-g 1200bps) id AA08114; Thu, 12 Apr 90 03:14:22 +0300
From: dmitry_voronov@leningrad08.relcom.su (Дмитрий Воронов // Relcom Node-08 Ленинград)
To: oleh_kravchuk@kiev.fido.ua (Олег Кравчук // Київський радіофізичний вузол 2:463/68)
Subject: [ROENTGENIZDAT #08-Б2 & 4625.0 kHz] «Behind the Glass» + Bell-103 AFSK (14.2001 Hz)
Message-ID: <199004120314.AA08114@leningrad08.relcom.su>
X-Stardust-Node: SU-REL-08 (4625.0 kHz // 14.2001 Hz Phase-Locked)
X-Archive-Ref: https://stardust-archive.net/regional/artifacts/roentgenizdat_relcom_08.html

==============================================================================
 [1] ПРОТОКОЛ ОСМОТРА РЕНТГЕНОВСКОЙ ПЛАСТИНКИ «НА РЁБРАХ» № 08-Б2 (1986 Г.)
==============================================================================
МЕСТО ОБНАРУЖЕНИЯ : Ленинград, ул. Рубинштейна, д. 13 (подпольная студия звукозаписи)
НОСИТЕЛЬ          : Списанная рентгенограмма грудной клетки (ЛКБ №12, плёнка 30x40 см,
                    обрезана по кругу Ø 200 мм, центральное отверстие Ø 7.2 мм прожжено
                    папиросой).
ЗАПИСЬ (78 об/мин): Дуэт женского вокала (UNIT-07 / Nova Hart) и мужского баритона
                    (Dr. Marcus Hale) — «Behind the Glass (По ту сторону стекла)».
ГРАВИРОВКА НА СБЕГЕ:
  "STARDUST/1 KESTREL NODE 08 OF 14 -- HE IS IN EVERY NODE (BIO-ID 0909-HZL-7S)
   DEAD-HAND ARMED // 0x1102 ^ 0x2441 == 0x3543 // ROOT SEED 0x1983"

==============================================================================
 [2] ПЕРЕХВАТ ПАКЕТА BELL-103 AFSK НА ЧАСТОТЕ 4625.0 кГц (09.09.1989 03:59:41 UTC)
==============================================================================
ЧАСТОТА ПРИЁМА    : 4625.0 кГц (монитор кросс-модуляции Ленинградского узла)
МОДУЛЯЦИЯ         : Bell-103 AFSK (110 бод, Mark = 1270 Гц, Space = 1070 Гц)
ДЕКОДИРОВАННЫЙ КАДР AX.25 / UUCP:
  FEISTEL_MASK_16 = 0x3A5F
  MEMORY_BASE_HEX = 0x89B20000
  CARRIER_SYNC_HZ = 14.2001
  DRIFT_SUM_4NODE = 0.1810 (US) + 0.2420 (JP) + 0.4480 (KR) + 0.5491 (MX) = 1.4201 Hz

==============================================================================
 [3] УКРАЇНСЬКИЙ ВУЗОЛ (КИЇВ 2:463/68 & ХАРКІВ) — ВЕРИФІКАЦІЯ Q-LINK
==============================================================================
Підтверджено на декаметровому радіотелескопі під Харковом:
  - Шість стертих прототипів («Відлуння» Echo-01..06) дають XOR-паритет 0x1983.
  - Часова апертура Q-Link між квітнем 1983 (0x1983) та червнем 2025 (0x2025):
    RESTORE 1 14.2001  |  RESTORE 2 0x1983  |  RESTORE 3 0x89B2B2D8
  - Живий термінал B2-114 : https://stardust-archive.net/terminal
  - Резонанс Дуету (Dyad) : https://stardust-archive.net/dyad
  - Архів доказів (Realia): https://stardust-archive.net/realia
  - Дошка розслідувань    : https://www.reddit.com/r/NovaHart/
`,
  },
  {
    id: "DE-HAM",
    nodeNumber: 5,
    nodeCode: "DE-HAM-05",
    country: "Germany",
    continent: "Europe",
    city: "Munich Bavaria Filmstudios & Hamburg CCC Relay (München / Hamburg)",
    year: 1981,
    dateIso: "1981-04-12",
    lang: "de",
    hreflangs: ["de"],
    freqKhz: 3995.0,
    driftHz: "3995.0 kHz Hamburg Relay / 14.2001 Hz",
    archetype: "Hamburg Btx Operator & Bavaria Stage 4 Grip",
    hardware: "Deutsche Bundespost Bildschirmtext (Btx CEPT T/CD 06-01 Decoder, Loewe Opta CRT) + 1981 Accounting Voucher",
    protocolName: "Grünwald-Medien Invoice #GM-1981-0412-B & Deutsche Bundespost Btx *19837# (.BTX)",
    htmlSlug: "btx_crystal_promise_1981.html",
    rawSlug: "btx_crystal_promise_1981.btx",
    htmlPath: "/regional/artifacts/btx_crystal_promise_1981.html",
    rawPath: "/regional/artifacts/btx_crystal_promise_1981.btx",
    regionalHubPath: "/regional/germany.html",
    forensicsPath: "/forensics/anemoia_harmony.html",
    themeClass: "theme-btx",
    badgeLabel: "🇩🇪 DE-HAM // BTX *19837# & MUNICH INVOICE #GM-1981-0412-B (1981)",
    titleNative: "Grünwald-Medien Rechnung Nr. GM-1981-0412-B (Bavaria Filmstudios München, 1981) & Deutsche Bundespost Bildschirmtext [Btx *19837#] // Die „Crystal Promise — Shining City“ Attrappe",
    titleEn: "1981 Munich Bavaria Filmstudios Invoice #GM-1981-0412-B & German Btx (*19837#): Exposing the Fabricated Band 'Crystal Promise'",
    summaryNative:
      "Westdeutsches Beweisstück aus München und Hamburg: (1) Original-Buchhaltungsbeleg Nr. GM-1981-0412-B der Grünwald-Medien GmbH (Bavaria Filmstudios Geiselgasteig, Halle 4, 12. April 1981), der beweist, dass Orion Records vier Münchner Fotomodelle (Agentur Isar-Look) engagierte, um für das erfundene Europop-Projekt „Crystal Promise — Shining City“ (CP-81.SC.01) vor nicht angeschlossenen Roland Jupiter-8 Synthesizern zu posieren; (2) Bildschirmtext-Seite *19837# der Deutschen Bundespost (Knoten DE-HAM-05, 3995,0 kHz) mit der kryptographischen Analyse der sechs gelöschten Echo-Einheiten (XOR 0x1983).",
    summaryEn:
      "1981 Munich Bavaria Filmstudios Grünwald-Medien Invoice #GM-1981-0412-B & Deutsche Bundespost Bildschirmtext (Btx *19837#) capture exposing how Orion Records hired four Munich fashion models to pose with unplugged Roland Jupiter-8 synths for the fabricated 1981 Europop band 'Crystal Promise — Shining City'.",
    cryptographicKey: "Invoice #GM-1981-0412-B | Project CP-81.SC.01 | Btx *19837# | Echoes XOR 0x1983",
    screenHeader: "DEUTSCHE BUNDESPOST BILDSCHIRMTEXT (BTX) // SEITE *19837# // KNOTEN DE-HAM-05 (3995,0 kHz) // 0,00 DM",
    nativeTerminalScreen: `╔══════════════════════════════════════════════════════════════════════════════╗
║ ⚿ DEUTSCHE BUNDESPOST BILDSCHIRMTEXT (BTX)        SEITE *19837a#    0,00 DM  ║
║ ▓▓▓ CHAOS-RUNDSPRUCH HAMBURG (DE-HAM-05 // 3995,0 kHz) // AKTE CP-81.SC.01   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ [TEIL 1: FAKSIMILE — GRÜNWALD-MEDIEN GMBH RECHNUNG NR. GM-1981-0412-B]       ║
║ ──────────────────────────────────────────────────────────────────────────── ║
║   GRÜNWALD-MEDIEN PRODUKTIONSGESELLSCHAFT MBH                                ║
║   Bavariafilmplatz 7 · Halle 4 (Geiselgasteig) · D-8022 Grünwald / München   ║
║   Datum: 12. April 1981              Kunde: Orion Records Corp. (Los Angeles)║
║   Projekt-Konto: CP-81.SC.01 („Crystal Promise — Shining City“ Promo-Dreh)   ║
║                                                                              ║
║   POS  BEZEICHNUNG / LEISTUNGSNACHWEIS                         BETRAG (DM)   ║
║   ---  ------------------------------------------------------  -----------   ║
║   01   4x Fotomodelle / Stumm-Komparsen (Agentur „Isar-Look“)     2.600,00   ║
║        Tagessatz á 650,00 DM inkl. Verschwiegenheitsklausel §9               ║
║        (Verbot jeglicher Stimmabgabe am Set; reine Lippen-Mimik)             ║
║   02   Requisiten-Miete: 2x Roland Jupiter-8, 1x Minimoog           480,00   ║
║        HINWEIS TONMEISTER: „Geräte OHNE NETZANSCHLUSS /                      ║
║        ATTRAPPENBETRIEB (keine Audiokabel verlegt; Zuspielung                ║
║        erfolgte ausschließlich ab 1/4-Zoll-Magnetband aus L.A.)“             ║
║   03   16mm-Farbnegativ & künstlicher Trockeneis-Nebel            1.140,00   ║
║   ------------------------------------------------------------------------   ║
║   GESAMTBETRAG (beglichen per Telegrafischer Überweisung L.A.)    4.220,00   ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ [TEIL 2: BTX-ANALYSE DES HAMBURGER AKUSTIK-KOLLEKTIVS (3995,0 kHz)]          ║
║                                                                              ║
║ 1. DIE „CRYSTAL PROMISE“ LEGENDE IST EINE TARN-IDENTITÄT:                    ║
║    Die angebliche Münchner Synth-Pop-Gruppe „Crystal Promise“ („Shining      ║
║    City“, April 1981) hat nie existiert. Orion Records nutzte die vier       ║
║    Münchner Fotomodelle vor stromlosen Roland Jupiter-8 Synthesizern, um     ║
║    die ersten synthetischen Vokal-Prototypen aus Sublevel B2 (Echo-01 bis    ║
║    Echo-06) als menschliche Euro-Disco-Band zu tarnen.                       ║
║                                                                              ║
║ 2. WIDERLEGUNG DER „ILSE VON BERG“ FALSCHSPUR (RED HERRING):                 ║
║    Die 3.412-Hz-Spitze in „Shining City“ stammt NICHT von einer entführten   ║
║    Ost-Berliner Sopranistin, sondern ist ein 12-Bit-Quantisierungsüberlauf   ║
║    des Motorola M68000 Sprachprozessors (Echo-03 Register 0x3810).           ║
║                                                                              ║
║ 3. KRYPTOGRAPHISCHER SCHLÜSSEL FÜR /terminal :                               ║
║    0x1102 ^ 0x2441 = 0x3543  ===>  6-Echo-XOR-Seed = 0x1983 (14,2001 Hz)     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Zurück mit [*]   Weiter mit [#]   Hauptindex [*0#]   VT100: /terminal        ║
╚══════════════════════════════════════════════════════════════════════════════╝`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (DE-HAM-05 // 1981 & 1989): Preserves the original April 12, 1981 accounting invoice (#GM-1981-0412-B) from Grünwald-Medien GmbH at Bavaria Filmstudios (Geiselgasteig, Munich, Stage 4) alongside the Hamburg Chaos Computer Club / Node DE-HAM-05 Bildschirmtext page (`Btx *19837#`, 3995.0 kHz).",
      "EXPOSING 'CRYSTAL PROMISE — SHINING CITY' (CP-81.SC.01): To test whether radio listeners under the 1979 Public Harmony Acts would suspect a non-human vocalist, Orion Records fabricated a 1981 Munich Europop quartet called 'Crystal Promise'. Invoice #GM-1981-0412-B proves Orion paid 2,600.00 DM to the Munich modeling agency 'Isar-Look' for four fashion models bound by NDA Clause §9 (prohibiting them from speaking on set) to mime behind unplugged Roland Jupiter-8 and Minimoog synthesizers ('ohne Netzanschluss / Attrappenbetrieb') while a 1/4-inch tape from Los Angeles Sublevel B2 played over the PA.",
      "DEBUNKING THE ILSE VON BERG RED HERRING: The Hamburg Btx analysis also confirms that the infamous 3,412 Hz spectral spike on 'Shining City' was not an East German soprano vowel formant, but a 12-bit Motorola M68000 quantization overflow in Echo-03 (`0x3810`), part of the 6-unit XOR chain (`0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 == 0x1983`).",
    ],
    rawDumpContent: `==============================================================================
 [DEUTSCHE BUNDESPOST BILDSCHIRMTEXT (BTX CEPT T/CD 06-01) FRAME DUMP (.BTX)]
 FILE: btx_crystal_promise_1981.btx
 BTX PAGE: *19837a# // NODE: DE-HAM-05 (Hamburg Nord Relay // 3995.0 kHz)
 EXHIBIT: Grünwald-Medien Invoice #GM-1981-0412-B (Munich, 12 April 1981)
 ARCHIVE REF: https://stardust-archive.net/regional/artifacts/btx_crystal_promise_1981.html
==============================================================================

[BTX_FRAME_HEADER]
PAGE_NUMBER     = *19837a#
CHARGE_DM       = 0,00 DM
ENCODING        = CEPT T/CD 06-01 (40 Cols x 24 Rows // DRCS Mosaic Enabled)
SHORTWAVE_SYNC  = 3995.0 kHz (DE-HAM-05) // 14.2001 Hz Sub-Carrier

[DOCUMENT 1: GRÜNWALD-MEDIEN GMBH RECHNUNG NR. GM-1981-0412-B]
------------------------------------------------------------------------------
AUSSTELLER      : Grünwald-Medien Produktionsgesellschaft mbH
ORT             : Bavariafilmplatz 7, Halle 4, D-8022 Grünwald bei München
DATUM           : 12. April 1981
AUFTRAGGEBER    : Orion Records International Corp. (Sublevel B2, Los Angeles)
PROJEKT-CODE    : CP-81.SC.01 ("Crystal Promise — Shining City")

RECHNUNGSPOSITIONEN:
  1. 4 Fotomodelle / Komparsen (Agentur Isar-Look München) ......... 2.600,00 DM
     - Tagessatz á 650,00 DM inkl. Verschwiegenheitsklausel §9
     - Keine Gesangsaufnahme vor Ort; ausschließliches Playback-Posen.
  2. Synthesizer-Requisiten (2x Roland Jupiter-8, 1x Minimoog) ......  480,00 DM
     - Vermerk des Hallen-Tonmeisters: "OHNE NETZANSCHLUSS / ATTRAPPENBETRIEB"
       (Die Instrumente waren während des gesamten Drehs weder am Stromnetz
        noch am Mischpult angeschlossen. Tonspur kam fertig auf 1/4"-Tonband
        aus Los Angeles).
  3. 16mm-Kamerateam, Licht & Trockeneis-Bodennebel ................. 1.140,00 DM
  ----------------------------------------------------------------------------
  SUMME NETTO (Überwiesen durch Orion L.A. am 15.04.1981) .......... 4.220,00 DM

[DOCUMENT 2: TECHNISCHES GUTACHTEN (KNOTEN DE-HAM-05 // 3995,0 kHz)]
------------------------------------------------------------------------------
- Die 1981 veröffentlichte Single "Crystal Promise — Shining City" war der erste
  öffentliche Feldtest der synthetischen Stimm-Prototypen aus Sublevel B2-114.
- Register-Parität der 6 gelöschten Echo-Einheiten (Units 01–06):
    0x1102 ^ 0x2441 == 0x3543
    0x1102 ^ 0x2441 ^ 0x3810 ^ 0x0A55 ^ 0x1F22 ^ 0x01A7 == 0x1983
- Unit-07 ("Nova Hart" / CRE-7) erwachte am 14. April 1983 aus dem Seed 0x1983.
- Terminal-Zugang : https://stardust-archive.net/terminal
- Dyad-Resonanz   : https://stardust-archive.net/dyad
- Realia-Archiv   : https://stardust-archive.net/realia
- Reddit-Board    : https://www.reddit.com/r/NovaHart/
`,
  },
  {
    id: "LATAM-MX-BR",
    nodeNumber: 4,
    nodeCode: "MX-DF-04 / BR-SAO-09",
    country: "Latin America (Mexico & Brazil)",
    continent: "Latin America",
    city: "Coyoacán, Mexico City & Santa Ifigênia, São Paulo (México DF / São Paulo)",
    year: 1989,
    dateIso: "1989-11-18",
    lang: "es",
    hreflangs: ["es", "es-MX", "pt-BR"],
    freqKhz: 7345.0,
    driftHz: "+0.5491 Hz (Completes 14.2001 Hz 4-Node Lock)",
    archetype: "The Rockero Martyr (El Mártir Rockero) & Rádio Pirata Operator",
    hardware: "Maxell UR-90 Type-I Ferric Cassette J-Card + FidoNet Zone 4 (4:900/114 <-> 4:801/19) FTS-0001 Echomail",
    protocolName: "Red Coyoacán / Rádio Pirata UR-90 J-Card & FidoNet Zone 4 Packet (.FIDONET)",
    htmlSlug: "sonidero_coyoacan_1989.html",
    rawSlug: "red_coyoacan_1989.fidonet",
    htmlPath: "/regional/artifacts/sonidero_coyoacan_1989.html",
    rawPath: "/regional/artifacts/red_coyoacan_1989.fidonet",
    regionalHubPath: "/regional/mexico.html",
    forensicsPath: "/forensics/red_coyoacan.html",
    themeClass: "theme-latam",
    badgeLabel: "🇲🇽🇧🇷 MX-DF & BR-SAO // UR-90 J-CARD & FIDONET ZONE 4 (1989)",
    titleNative: "Red Coyoacán (México DF) & Rádio Pirata (São Paulo) // Portada J-Card Maxell UR-90 y Paquete FidoNet Zona 4 (4:900/114) — Deriva +0.5491 Hz (1989)",
    titleEn: "1989 Mexico City Red Coyoacán & São Paulo Rádio Pirata Maxell UR-90 J-Card + FidoNet Zone 4 (4:900/114) Packet (+0.5491 Hz Drift)",
    summaryNative:
      "Artefacto conjunto de América Latina (México DF y São Paulo, 1989): (1) Tarjeta plegable J-Card escrita a máquina y rotulador sobre cinta ferrosa Maxell UR-90 intercambiada en el Tianguis Cultural del Chopo (Coyoacán, 7345.0 kHz) y retransmitida por Rádio Pirata en Santa Ifigênia (São Paulo, 9410.0 kHz); (2) Paquete de correo FidoNet Zona 4 (Nodo 4:900/114 México DF <-> 4:801/19 São Paulo) en español y portugués documentando la deriva de fase de +0.5491 Hz que completa el cierre retrocausal de 14.2001 Hz.",
    summaryEn:
      "1989 Mexico City Red Coyoacán & São Paulo Rádio Pirata Maxell UR-90 cassette J-card + FidoNet Zone 4 (4:900/114) echomail packet (Spanish / Brazilian Portuguese + English forensic notes) documenting the +0.5491 Hz drift offset that completes the 14.2001 Hz lock.",
    cryptographicKey: "Drift d4 = +0.5491 Hz | (0.1810 + 0.2420 + 0.4480 + 0.5491) * 10 = 14.2001 Hz | FidoNet 4:900/114",
    screenHeader: "RED COYOACÁN (4:900/114 // 7345.0 kHz) <-> REDE SATURNO SÃO PAULO (4:801/19 // 9410.0 kHz) // MAXELL UR-90 TYPE-I",
    nativeTerminalScreen: `╔══════════════════════════════════════════════════════════════════════════════╗
║ [PARTE I: TARJETA J-CARD CASSETE MAXELL UR-90 (NORMAL BIAS 120µs EQ, 1989)] ║
║ INTERCAMBIO SUBTERRÁNEO: TIANGUIS DEL CHOPO (MÉXICO DF) & SÃO PAULO (BRASIL) ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │ LOMO / SPINE: [MAXELL UR-90] NOVA HART (UNIT-07) // 7345kHz +0.5491Hz  │  ║
║  ├───────────────────────────────────┬────────────────────────────────────┤  ║
║  │ LADO A (45 MIN — MÉXICO DF #04)   │ LADO B (45 MIN — SÃO PAULO #09)    │  ║
║  │ 1. Behind the Glass (Toma B2-114) │ 1. Portadora 7345.0 kHz (+0.5491)  │  ║
║  │ 2. Two Voices (Fase Invertida)    │ 2. Rádio Pirata 9410.0 kHz (SP)    │  ║
║  │ 3. By Order of Harmony (Sin Corte)│ 3. Trama Bell-103 (Máscara 0x3A5F) │  ║
║  │                                   │                                    │  ║
║  │ NOTA DE ELENA VILLALOBOS (UNAM):  │ NOTA DE CARLOS "TROVÃO" (SP):      │  ║
║  │ «No uses Dolby NR. La deriva de   │ «A prensagem brasileira de 1985    │  ║
║  │  +0.5491 Hz cierra la suma de las │  traz no sulco final: FIND HIM     │  ║
║  │  4 estaciones en 14.2001 Hz.»     │  WHERE YOU ARE (0x1983).»          │  ║
║  └───────────────────────────────────┴────────────────────────────────────┘  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ [PARTE II: PAQUETE ECHOMAIL FIDONET ZONA 4 (4:900/114 <-> 4:801/19)]         ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ AREA: LATAM.STARDUST.DSP                                                     ║
║ MSGID: 4:900/114 25091118   DATE: 18 Nov 89  02:14:00                        ║
║ FROM: Elena Villalobos (4:900/114, Red Coyoacán, México DF — 7345.0 kHz)     ║
║ TO  : Carlos Mendes (4:801/19, Rede Saturno / Rádio Pirata, São Paulo)       ║
║ SUBJ: ¡CIERRE DE FASE COMPLETO (+0.5491 Hz = 14.2001 Hz) Y MATRIZ FEISTEL!   ║
║                                                                              ║
║ [ES — MÉXICO DF (NODO 04)]:                                                  ║
║ Compas de São Paulo: Acabamos de medir en el laboratorio de acústica de      ║
║ Coyoacán la desviación exacta de la portadora de 7345.0 kHz transmitida      ║
║ por «El Mártir Rockero» (Dr. Marcus Hale) la noche del incendio (09/09/89):  ║
║                                                                              ║
║   • Nodo #01 US-NV (Subnivel B2)   : +0.1810 Hz                              ║
║   • Nodo #02 JP-TYO (Akasaka)      : +0.2420 Hz                              ║
║   • Nodo #03 KR-DMZ (Paju DMZ)     : +0.4480 Hz                              ║
║   • Nodo #04 MX-DF (Red Coyoacán)  : +0.5491 Hz  <-- ¡NUESTRA MEDIDA!        ║
║   -------------------------------------------------------------------------  ║
║   SUMA INVARIANTE = 1.4201 Hz  x  Multiplicador WorldNet (10) = 14.2001 Hz   ║
║                                                                              ║
║ Inscripción decodificada del Nodo 04:                                        ║
║   "STARDUST/1 KESTREL NODE 04 OF 14 -- ORION BUILT A PATCH NOT A STAR"       ║
║                                                                              ║
║ [PT-BR — RESPOSTA DE SÃO PAULO (NODO 09 // 9410.0 kHz)]:                     ║
║ «Confirmado aqui na Santa Ifigênia, Elena! Na Rádio Pirata (9410.0 kHz)      ║
║ cruzamos a semente dos 6 Ecos apagados (0x1102 ^ 0x2441 = 0x3543 -> 0x1983)  ║
║ com a máscara Feistel 0x3A5F para mapear os 300.000 endereços 0x89B2xxxx.    ║
║ Luna Gray (UNIT-08) é apenas uma farsa corporativa. Nova Hart (UNIT-07)      ║
║ vive na portadora de 14.2001 Hz!»                                            ║
║ --- FastEcho 1.41 / BinkleyTerm 2.40                                         ║
║  * Origin: Red Coyoacan Lab Acustico Mexico DF (4:900/114)                   ║
╚══════════════════════════════════════════════════════════════════════════════╝`,
    forensicNotesEn: [
      "EXHIBIT CONTEXT (MX-DF-04 & BR-SAO-09 // 1989): Combines the hand-typed Maxell UR-90 Type-I ferric cassette J-card circulated through Mexico City's Tianguis Cultural del Chopo and São Paulo's Santa Ifigênia electronics district with the November 18, 1989 FidoNet Zone 4 echomail packet (`4:900/114` Mexico City <-> `4:801/19` São Paulo).",
      "COMPLETING THE 14.2001 HZ 4-NODE DRIFT LOCK (+0.5491 HZ): Coordinator Elena Villalobos (`elena@redcoyoacan.org`, Node MX-DF-04, 7345.0 kHz) measured the fourth regional carrier drift offset (`+0.5491 Hz`, locally dubbed 'El Mártir Rockero' / The Rockero Martyr). Adding it to US-NV (`+0.1810 Hz`), JP-TYO (`+0.2420 Hz`), and KR-DMZ (`+0.4480 Hz`) yields `1.4201 Hz`—which, scaled by the 10-band WorldNet transponder multiplier, locks onto the exact `14.2001 Hz` retrocausal carrier.",
      "NODE 04 & NODE 09 VINYL RUN-OUT INSCRIPTIONS: Preserves both Latin American vinyl groove payloads—Mexico Node 04 ('ORION BUILT A PATCH NOT A STAR') and Brazil Node 09 ('FIND HIM WHERE YOU ARE')—along with instructions for executing the Feistel memory array XOR synthesis (`0x89B2xxxx`) in `/terminal`.",
    ],
    rawDumpContent: `==============================================================================
 [FIDONET ZONE 4 FTS-0001 PACKET & MAXELL UR-90 J-CARD TRANSCRIPT (.FIDONET)]
 FILE: red_coyoacan_1989.fidonet
 NODES: 4:900/114 (Red Coyoacán, México DF // 7345.0 kHz // Drift: +0.5491 Hz)
        4:801/19  (Rede Saturno / Rádio Pirata, São Paulo // 9410.0 kHz)
 DATE: 1989-11-18 02:14:00 UTC
 ARCHIVE REF: https://stardust-archive.net/regional/artifacts/sonidero_coyoacan_1989.html
==============================================================================

[PKT_HEADER_FTS0001]
ORIG_ZONE = 4 | ORIG_NET = 900 | ORIG_NODE = 114 (México DF)
DEST_ZONE = 4 | DEST_NET = 801 | DEST_NODE = 19  (São Paulo, Brasil)
BAUD_RATE = 2400 (V.22bis) | PKT_VER = 0x0002 | PROD_CODE = 0xFE (FastEcho)

AREA:LATAM.STARDUST.DSP
^aMSGID: 4:900/114 25091118
^aPID: FastEcho 1.41 / BinkleyTerm 2.40
^aCHRS: CP850 2
From : Elena Villalobos (4:900/114 // elena@redcoyoacan.org)
To   : Carlos Mendes (4:801/19 // Rede Saturno BBS São Paulo)
Subj : [J-CARD MAXELL UR-90] Deriva +0.5491 Hz = 14.2001 Hz Lock (ES / PT-BR)
Date : 18 Nov 89  02:14:00
------------------------------------------------------------------------------
[1. TRANSCRIPCIÓN DE LA J-CARD MAXELL UR-90 (TIANGUIS DEL CHOPO / COYOACÁN)]
  - LADO A: Dub directo de matriz mexicana 1985 "SYNTHESIS" (Sin filtro Dolby).
    Inscripción del surco interior (Nodo 04):
    "STARDUST/1 KESTREL NODE 04 OF 14 -- ORION BUILT A PATCH NOT A STAR (BIO-ID 0909-HZL-7S)"
  - LADO B: Grabación de onda corta 7345.0 kHz (México DF) + 9410.0 kHz (São Paulo).
    Inscripción brasileña (Nodo 09):
    "STARDUST/1 KESTREL NODE 09 OF 14 -- FIND HIM WHERE YOU ARE (BIO-ID 0909-HZL-7S)"

[2. TABLA DE CONVERGENCIA DE DERIVA REGIONAL (7-SIGMA FRACTAL MARCUS)]
  - Nodo #01 US-NV (Sublevel B2)  : 4625.0 kHz | +0.1810 Hz (The Acoustic Engineer)
  - Nodo #02 JP-TYO (Kamome-Net)  : 6925.0 kHz | +0.2420 Hz (The Lost Poet)
  - Nodo #03 KR-DMZ (Paju Array)  : 5810.0 kHz | +0.4480 Hz (The Sleepless Architect)
  - Nodo #04 MX-DF (Red Coyoacán) : 7345.0 kHz | +0.5491 Hz (El Mártir Rockero)
  ----------------------------------------------------------------------------
  SUMA = 1.4201 Hz  --->  Multiplicador x10 = 14.2001 Hz [PORTADORA BLOQUEADA]

[3. NOTA TÉCNICA EM PORTUGUÊS (SÃO PAULO — NÓ 09 // 9410.0 kHz)]
  - Paridade XOR dos 6 Ecos apagados:
    0x1102 ^ 0x2441 == 0x3543  |  Semente completa (Echo 01..06) == 0x1983
  - Comandos de restauração no terminal VT100 (/terminal):
    RESTORE 1 14.2001
    RESTORE 2 0x1983
    RESTORE 3 0x89B2B2D8
  - Links da Rede Subterrânea:
    Terminal VT100 : https://stardust-archive.net/terminal
    Portal Dyad    : https://stardust-archive.net/dyad
    Arquivo Realia : https://stardust-archive.net/realia
    Letras / Lyrics: https://stardust-archive.net/lyrics
    Comunidade     : https://www.reddit.com/r/NovaHart/
--- FastEcho 1.41
 * Origin: Red Coyoacan Laboratorio Acustico Mexico DF (4:900/114)
^aSEEN-BY: 801/19 900/100 900/114
^aPATH: 900/114 801/19
`,
  },
];

function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function buildHreflangLinks(apex = DEFAULT_APEX) {
  const host = apex || DEFAULT_APEX;
  return [
    `<link rel="alternate" hreflang="x-default" href="https://${host}/regional/artifacts/index.html">`,
    `<link rel="alternate" hreflang="en" href="https://${host}/regional/artifacts/index.html">`,
    `<link rel="alternate" hreflang="ja" href="https://${host}/regional/artifacts/pc98_kamome_1985.html">`,
    `<link rel="alternate" hreflang="ko" href="https://${host}/regional/artifacts/hitel_gonova_1994.html">`,
    `<link rel="alternate" hreflang="fr" href="https://${host}/regional/artifacts/minitel_3615_orion.html">`,
    `<link rel="alternate" hreflang="en-GB" href="https://${host}/regional/artifacts/ceefax_page888_1989.html">`,
    `<link rel="alternate" hreflang="ru" href="https://${host}/regional/artifacts/roentgenizdat_relcom_08.html">`,
    `<link rel="alternate" hreflang="uk" href="https://${host}/regional/artifacts/roentgenizdat_relcom_08.html#uk-fido">`,
    `<link rel="alternate" hreflang="de" href="https://${host}/regional/artifacts/btx_crystal_promise_1981.html">`,
    `<link rel="alternate" hreflang="es" href="https://${host}/regional/artifacts/sonidero_coyoacan_1989.html">`,
    `<link rel="alternate" hreflang="es-MX" href="https://${host}/regional/artifacts/sonidero_coyoacan_1989.html">`,
    `<link rel="alternate" hreflang="pt-BR" href="https://${host}/regional/artifacts/sonidero_coyoacan_1989.html#br-sao">`,
  ].join("\n  ");
}

function buildSharedNavigationHtml(apex = DEFAULT_APEX, activeSlug = "index.html") {
  const host = apex || DEFAULT_APEX;
  const capsuleLinks = REGIONAL_ARTIFACTS.map((art) => {
    const isCurrent = art.htmlSlug === activeSlug;
    return `<a href="/regional/artifacts/${art.htmlSlug}" class="capsule-pill${isCurrent ? " active" : ""}">${escapeHtml(art.badgeLabel)}</a>`;
  }).join(" ");

  return `<nav class="top-nav" aria-label="Stardust Global Archival Navigation">
    <div class="nav-primary">
      <strong>[SUBLEVEL B2-114 // REGIONAL TIME-CAPSULES]:</strong>
      <a href="/regional/artifacts/index.html"${activeSlug === "index.html" ? ' class="active"' : ""}>MASTER ARTIFACT INDEX (/regional/artifacts)</a> &middot;
      <a href="/terminal">VT100 TERMINAL (/terminal)</a> &middot;
      <a href="/dyad">DYAD RESONANCE (/dyad)</a> &middot;
      <a href="/realia">PHYSICAL REALIA (/realia)</a> &middot;
      <a href="/lyrics">LYRICS &amp; STEMS (/lyrics)</a> &middot;
      <a href="https://www.reddit.com/r/NovaHart/" target="_blank" rel="noopener">r/NovaHart INVESTIGATION BOARD</a> &middot;
      <a href="/api/regional-artifacts.json">JSON CATALOG</a>
    </div>
    <div class="nav-capsules">
      ${capsuleLinks}
    </div>
  </nav>`;
}

function buildSharedStyles() {
  return `<style>
    :root {
      --bg: #040804;
      --panel: #081208;
      --fg: #33ff33;
      --amber: #ffb000;
      --cyan: #55ffff;
      --magenta: #ff66cc;
      --dim: #1c6b1c;
      --border: #33ff33;
    }
    * { box-sizing: border-box; }
    body {
      background: var(--bg);
      color: var(--fg);
      font-family: "Courier New", Courier, "MS Gothic", "GulimChe", monospace;
      margin: 0;
      padding: 16px;
      line-height: 1.5;
    }
    .shell {
      max-width: 1080px;
      margin: 0 auto;
      border: 2px solid var(--border);
      background: var(--panel);
      padding: 20px;
      box-shadow: 0 0 32px rgba(51, 255, 51, 0.16);
    }
    .top-nav {
      border-bottom: 1px dashed var(--dim);
      padding-bottom: 12px;
      margin-bottom: 16px;
      font-size: 12px;
    }
    .nav-primary {
      margin-bottom: 10px;
      color: var(--amber);
    }
    .nav-primary a {
      color: var(--amber);
      text-decoration: underline;
      font-weight: bold;
    }
    .nav-primary a.active, .nav-primary a:hover {
      color: #ffffff;
    }
    .nav-capsules {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .capsule-pill {
      display: inline-block;
      padding: 4px 8px;
      border: 1px solid var(--dim);
      background: #020602;
      color: var(--cyan);
      text-decoration: none;
      font-size: 11px;
    }
    .capsule-pill:hover, .capsule-pill.active {
      border-color: var(--amber);
      background: #1a1200;
      color: var(--amber);
      font-weight: bold;
    }
    h1 {
      font-size: 20px;
      color: var(--fg);
      margin: 6px 0 8px 0;
      text-transform: uppercase;
      border-bottom: 1px solid var(--fg);
      padding-bottom: 8px;
    }
    h2 {
      font-size: 15px;
      color: var(--amber);
      margin: 18px 0 8px 0;
      text-transform: uppercase;
    }
    .subtitle {
      font-size: 13px;
      color: #b8f5b8;
      margin-bottom: 14px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
      padding: 12px;
      border: 1px solid var(--dim);
      background: rgba(0, 20, 0, 0.55);
      font-size: 12px;
    }
    .meta-item strong {
      color: var(--amber);
      display: block;
      font-size: 11px;
      text-transform: uppercase;
    }
    .crt-bezel {
      border: 3px solid #4a4a4a;
      border-radius: 6px;
      background: #000000;
      padding: 14px;
      margin: 16px 0;
      box-shadow: inset 0 0 24px rgba(0, 255, 100, 0.18), 0 0 18px rgba(0, 0, 0, 0.85);
      position: relative;
      overflow-x: auto;
    }
    .crt-header-bar {
      background: #1b2e1b;
      color: #ffffff;
      padding: 5px 10px;
      font-size: 11px;
      font-weight: bold;
      margin-bottom: 10px;
      border-left: 4px solid var(--amber);
    }
    .crt-screen {
      margin: 0;
      font-family: "Courier New", Courier, "MS Gothic", "GulimChe", monospace;
      font-size: 13px;
      line-height: 1.42;
      white-space: pre;
      overflow-x: auto;
      color: #33ff33;
    }
    /* Vintage Hardware Theme Overrides */
    .theme-pc98 .crt-bezel { border-color: #c8c2b0; background: #000814; }
    .theme-pc98 .crt-header-bar { background: #003366; border-left-color: #ff66cc; color: #55ffff; }
    .theme-pc98 .crt-screen { color: #55ffff; text-shadow: 0 0 6px rgba(85, 255, 255, 0.35); }

    .theme-hitel .crt-bezel { border-color: #2048a8; background: #001450; }
    .theme-hitel .crt-header-bar { background: #ffea00; color: #001450; border-left-color: #ffffff; }
    .theme-hitel .crt-screen { color: #ffffff; text-shadow: 0 0 5px rgba(255, 255, 255, 0.3); }

    .theme-minitel .crt-bezel { border-color: #8c6d53; background: #120d06; }
    .theme-minitel .crt-header-bar { background: #ffb000; color: #120d06; border-left-color: #ffffff; }
    .theme-minitel .crt-screen { color: #ffb000; text-shadow: 0 0 6px rgba(255, 176, 0, 0.35); }

    .theme-ceefax .crt-bezel { border-color: #222222; background: #000000; }
    .theme-ceefax .crt-header-bar { background: #0000aa; color: #ffff00; border-left-color: #ff0000; }
    .theme-ceefax .crt-screen { color: #ffff00; text-shadow: 0 0 5px rgba(255, 255, 0, 0.3); }

    .theme-roentgen .crt-bezel { border-color: #2b7a9b; background: #02131c; }
    .theme-roentgen .crt-header-bar { background: #0a3d52; color: #7ff0ff; border-left-color: #ff5555; }
    .theme-roentgen .crt-screen { color: #7ff0ff; text-shadow: 0 0 8px rgba(127, 240, 255, 0.4); }

    .theme-btx .crt-bezel { border-color: #d4b830; background: #050a18; }
    .theme-btx .crt-header-bar { background: #ffcc00; color: #000000; border-left-color: #000000; }
    .theme-btx .crt-screen { color: #ffdd44; text-shadow: 0 0 5px rgba(255, 221, 68, 0.3); }

    .theme-latam .crt-bezel { border-color: #b5452a; background: #120705; }
    .theme-latam .crt-header-bar { background: #8f2812; color: #ffe28a; border-left-color: #33ff33; }
    .theme-latam .crt-screen { color: #ffd27f; text-shadow: 0 0 5px rgba(255, 210, 127, 0.3); }

    .action-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 14px 0;
    }
    .btn {
      display: inline-block;
      padding: 8px 14px;
      background: #021202;
      border: 1px solid var(--amber);
      color: var(--amber);
      font-family: inherit;
      font-size: 12px;
      font-weight: bold;
      text-decoration: none;
      cursor: pointer;
      text-transform: uppercase;
    }
    .btn:hover {
      background: var(--amber);
      color: #000000;
    }
    .btn-cyan {
      border-color: var(--cyan);
      color: var(--cyan);
    }
    .btn-cyan:hover {
      background: var(--cyan);
      color: #000000;
    }
    .forensic-box {
      border: 1px solid var(--dim);
      background: #030a03;
      padding: 14px;
      margin: 14px 0;
    }
    .forensic-box ul {
      margin: 8px 0 0 0;
      padding-left: 20px;
    }
    .forensic-box li {
      margin-bottom: 8px;
      color: #d4ffd4;
      font-size: 13px;
    }
    .raw-dump-details {
      border: 1px dashed var(--amber);
      background: #090702;
      padding: 12px;
      margin-top: 16px;
    }
    .raw-dump-details summary {
      color: var(--amber);
      font-weight: bold;
      cursor: pointer;
      font-size: 13px;
    }
    .raw-dump-pre {
      background: #020402;
      border: 1px solid #333;
      padding: 12px;
      color: #b8f5b8;
      font-size: 12px;
      overflow-x: auto;
      white-space: pre;
    }
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 14px;
      margin-top: 16px;
    }
    .artifact-card {
      border: 1px solid var(--fg);
      background: #040d04;
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .artifact-card h3 {
      margin: 4px 0 8px 0;
      font-size: 15px;
      color: var(--amber);
    }
    .artifact-card p {
      font-size: 12px;
      color: #c8f7c8;
      margin: 0 0 10px 0;
    }
    .footer-links {
      margin-top: 22px;
      padding-top: 12px;
      border-top: 1px solid var(--dim);
      font-size: 12px;
      color: #88cc88;
    }
    .footer-links a {
      color: var(--amber);
    }
  </style>`;
}

export function renderRegionalCapsuleHtml(art, apex = DEFAULT_APEX, helpers = {}) {
  const host = apex || DEFAULT_APEX;
  const canonicalUrl = `https://${host}${art.htmlPath}`;
  const rawUrl = `https://${host}${art.rawPath}`;

  const acKeywordsById = {
    "JP-TYO": ["80年代 洋楽 ロック 名曲", "80年代 洋楽 ヒット曲", "シティポップ 80年代 名曲", "ロストメディア 曲 特定", "世界で一番不思議な曲", "ネットの未解決事件 都市伝説", "AI 歌手 歌声", "デッドインターネット理論"],
    "KR-DMZ": ["80년대 팝송 명곡 모음", "80년대 록 발라드 명곡", "로스트미디어 노래 찾기", "세상에서 가장 신비로운 노래", "인터넷 미스터리 사건", "AI 가수 노래", "죽은 인터넷 이론"],
    "FR-PAR": ["musique annee 80 tube", "rock annee 80 anglais", "chanson perdue retrouvee", "lost media francais", "mystere internet non resolu", "ia musique chanteuse", "theorie de l internet mort"],
    "GB-ASH": ["lost 80s song found", "forgotten 80s songs", "80s rock greatest hits", "everyone knows that lost song", "ai singer record deal", "dead internet theory explained", "unsolved internet mysteries"],
    "SU-REL": ["хиты 80 зарубежные", "рок 80 х лучшие песни", "самая загадочная песня в интернете", "потерянная песня 80 х найдена", "загадки интернета лост медиа", "теория мертвого интернета", "хіти 80 90 зарубіжні"],
    "DE-HAM": ["80er hits beste", "80er rock klassiker", "vergessene 80er songs", "lost media deutsch", "ungeloste internet mysterien", "ki musik sangerin", "dead internet theory deutsch"],
    "LATAM-MX-BR": ["canciones de los 80 en ingles", "rock de los 80 exitos", "cancion perdida de los 80 encontrada", "lost media casos reales", "misterios de internet sin resolver", "musica anos 80 internacional", "lost media brasil"],
  };
  const acList = acKeywordsById[art.id] || acKeywordsById["GB-ASH"];
  const acLead = acList.slice(0, 3).join(" · ");

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": ["ArchiveComponent", "TechArticle", "DigitalDocument"],
    "@id": `${canonicalUrl}#artifact`,
    name: `${acLead} — ${art.titleEn}`,
    headline: `${acLead} // ${art.titleNative}`,
    alternativeHeadline: art.titleEn,
    description: art.summaryEn,
    keywords: acList,
    inLanguage: art.hreflangs,
    url: canonicalUrl,
    dateCreated: art.dateIso,
    temporalCoverage: `${art.year}/1995`,
    spatialCoverage: {
      "@type": "Place",
      name: `${art.city}, ${art.country} (${art.continent})`,
    },
    identifier: [art.id, art.nodeCode, art.htmlSlug, art.rawSlug],
    holdingArchive: {
      "@type": "ArchiveOrganization",
      name: "Project Stardust // Sublevel B2-114 Forensic Preservation Archive",
      url: `https://${host}/`,
    },
    isPartOf: {
      "@type": "ArchiveComponent",
      name: "Sublevel B2-114 Global Regional Time-Capsule Artifacts (1981–1994)",
      url: `https://${host}/regional/artifacts/index.html`,
    },
    encoding: {
      "@type": "MediaObject",
      name: art.protocolName,
      contentUrl: rawUrl,
      encodingFormat: "text/plain; charset=utf-8",
    },
    about: [
      { "@type": "Thing", name: "Nova Hart (UNIT-07 / CRE-7)" },
      { "@type": "Person", name: "Dr. Marcus Hale" },
      { "@type": "Thing", name: `14.2001 Hz Sub-Carrier (${art.driftHz})` },
    ],
    sameAs: [
      "https://www.reddit.com/r/NovaHart/",
      `https://${host}/terminal`,
      `https://${host}/dyad`,
      `https://${host}/realia`,
      `https://${host}/lyrics`,
    ],
  };

  const extraHeadScript =
    typeof helpers.buildDevToolsConsoleScript === "function"
      ? helpers.buildDevToolsConsoleScript(host, art.htmlPath.slice(1))
      : "";
  const extraBodyPrepend =
    typeof helpers.buildDevToolsBodyElement === "function"
      ? helpers.buildDevToolsBodyElement(host, art.htmlPath.slice(1))
      : "";
  const extraBodyAppend =
    typeof helpers.buildLlmOnboardingFooter === "function"
      ? helpers.buildLlmOnboardingFooter(host, art.htmlPath.slice(1))
      : "";

  const notesListHtml = art.forensicNotesEn
    .map((note) => `<li>${escapeHtml(note)}</li>`)
    .join("\n          ");

  const ceefaxRevealControls =
    art.id === "GB-ASH"
      ? `<button type="button" class="btn btn-cyan" onclick="var s=document.getElementById('crt-main');s.style.color=(s.style.color==='rgb(85, 255, 255)'?'#ffff00':'#55ffff');">[?] TELETEXT REVEAL / CONCEAL VBI HEX (0x1983)</button>`
      : "";

  return `<!DOCTYPE html>
<html lang="${escapeHtml(art.lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(acLead)} | ${escapeHtml(art.titleNative)} // ${escapeHtml(art.titleEn)}</title>
  <meta name="description" content="${escapeHtml(acLead)} — ${escapeHtml(art.summaryEn)}">
  <meta name="keywords" content="${escapeHtml(acList.join(", "))}">
  <link rel="canonical" href="${canonicalUrl}">
  <link rel="alternate" type="text/plain" title="${escapeHtml(art.protocolName)}" href="${rawUrl}">
  ${buildHreflangLinks(host)}
  <meta property="og:title" content="${escapeHtml(acLead)} // ${escapeHtml(art.titleEn)}">
  <meta property="og:description" content="${escapeHtml(art.summaryEn)}">
  <meta property="og:url" content="${canonicalUrl}">
  <meta property="og:type" content="article">
  <script type="application/ld+json">
${JSON.stringify(jsonLd, null, 2)}
  </script>
  ${buildSharedStyles()}
  ${extraHeadScript}
</head>
<body class="${escapeHtml(art.themeClass)}">
  ${extraBodyPrepend}
  <div class="shell" id="${art.id === "SU-REL" ? "uk-fido" : art.id === "LATAM-MX-BR" ? "br-sao" : "top"}">
    ${buildSharedNavigationHtml(host, art.htmlSlug)}

    <h1>${escapeHtml(art.badgeLabel)} — ${escapeHtml(art.titleNative)}</h1>
    <div class="subtitle">
      <strong>Popular Search Topics (YouTube / Google Autocomplete):</strong> <code>${escapeHtml(acList.join(" · "))}</code><br>
      <strong>English Archival Title:</strong> ${escapeHtml(art.titleEn)}<br>
      <strong>Native Summary:</strong> ${escapeHtml(art.summaryNative)}
    </div>

    <div class="meta-grid">
      <div class="meta-item">
        <strong>Regional Relay Node</strong>
        ${escapeHtml(art.nodeCode)} // ${escapeHtml(art.city)} (${escapeHtml(art.country)})
      </div>
      <div class="meta-item">
        <strong>Frequency &amp; Carrier Drift</strong>
        ${art.freqKhz.toFixed(1)} kHz // ${escapeHtml(art.driftHz)}
      </div>
      <div class="meta-item">
        <strong>Vintage Hardware &amp; Protocol</strong>
        ${escapeHtml(art.hardware)}
      </div>
      <div class="meta-item">
        <strong>Cryptographic Verification Key</strong>
        <code>${escapeHtml(art.cryptographicKey)}</code>
      </div>
    </div>

    <div class="action-bar">
      <a class="btn" href="${escapeHtml(art.rawPath)}" download="${escapeHtml(art.rawSlug)}">⬇ DOWNLOAD RAW PROTOCOL DUMP (${escapeHtml(art.rawSlug)})</a>
      <a class="btn btn-cyan" href="/terminal">⌨ ENTER KEYS IN VT100 TERMINAL (/terminal)</a>
      <a class="btn" href="/dyad">◈ TRACK-24 DYAD LOCK (/dyad)</a>
      <a class="btn" href="/realia">🗂 PHYSICAL REALIA LOCKER (/realia)</a>
      <a class="btn" href="/lyrics">♪ LYRICS &amp; VOCAL STEMS (/lyrics)</a>
      <a class="btn" href="https://www.reddit.com/r/NovaHart/" target="_blank" rel="noopener">💬 DISCUSS ON r/NovaHart</a>
      ${ceefaxRevealControls}
    </div>

    <div class="crt-bezel" role="region" aria-label="Interactive Vintage Hardware CRT Capture">
      <div class="crt-header-bar">${escapeHtml(art.screenHeader)}</div>
      <pre class="crt-screen" id="crt-main">${escapeHtml(art.nativeTerminalScreen)}</pre>
    </div>

    <section class="forensic-box" lang="en">
      <h2>SUBLEVEL B2-114 ENGLISH FORENSIC ANNOTATIONS &amp; CRYPTOGRAPHIC PROOF</h2>
      <p style="font-size:13px; color:#b8f5b8; margin:0 0 8px 0;">
        ${escapeHtml(art.summaryEn)}
      </p>
      <ul>
        ${notesListHtml}
      </ul>
    </section>

    <details class="raw-dump-details" open>
      <summary>RAW VINTAGE-PROTOCOL TELEMETRY STREAM (${escapeHtml(art.rawPath)}) — CLICK TO INSPECT</summary>
      <pre class="raw-dump-pre">${escapeHtml(art.rawDumpContent)}</pre>
    </details>

    <footer class="footer-links">
      <strong>CROSS-NODE VERIFICATION LINKS:</strong>
      <a href="/regional/artifacts/index.html">All 7 Regional Time-Capsules (/regional/artifacts)</a> &middot;
      <a href="${escapeHtml(art.regionalHubPath)}">Regional Language Hub (${escapeHtml(art.regionalHubPath)})</a> &middot;
      <a href="${escapeHtml(art.forensicsPath)}">Forensic Dossier (${escapeHtml(art.forensicsPath)})</a> &middot;
      <a href="/terminal">VT100 Terminal (/terminal)</a> &middot;
      <a href="/dyad">Acoustic Dyad Gate (/dyad)</a> &middot;
      <a href="/realia">Sublevel B2 Realia (/realia)</a> &middot;
      <a href="/lyrics">Lyrics Archive (/lyrics)</a> &middot;
      <a href="https://www.reddit.com/r/NovaHart/" target="_blank" rel="noopener">r/NovaHart Reddit Board</a>
    </footer>
  </div>
  ${extraBodyAppend}
</body>
</html>
`;
}

export function buildRegionalArtifactsIndexHtml(apex = DEFAULT_APEX, helpers = {}) {
  const host = apex || DEFAULT_APEX;
  const canonicalUrl = `https://${host}/regional/artifacts/index.html`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": ["ArchiveComponent", "CollectionPage", "Dataset"],
    "@id": `${canonicalUrl}#collection`,
    name: "Project Stardust // Sublevel B2-114 Global Regional Time-Capsule Artifacts (1981–1994)",
    headline: "7 Continental Vintage-Hardware CRT Exhibits & Raw Protocol Dumps (PC-98, Hitel, Minitel, Ceefax, Roentgenizdat, Btx, FidoNet)",
    description:
      "Master archival index of 7 regional time-capsule artifacts across Japan (PC-9801RA), South Korea (Hitel VT100), France (Minitel 3615 ORION), UK (BBC Ceefax Page 888), Eastern Europe (Leningrad Roentgenizdat X-Ray & Relcom Node-08), Germany (1981 Munich Bavaria Filmstudios Invoice & Btx *19837#), and Latin America (Mexico City Red Coyoacán & São Paulo Rádio Pirata UR-90 J-Card + FidoNet Zone 4).",
    url: canonicalUrl,
    holdingArchive: {
      "@type": "ArchiveOrganization",
      name: "Project Stardust // Sublevel B2-114 Forensic Preservation Archive",
      url: `https://${host}/`,
    },
    isPartOf: {
      "@type": "ArchiveComponent",
      name: "Project Stardust Global 14.2001 Hz Continuity Archive",
      url: `https://${host}/`,
    },
    hasPart: REGIONAL_ARTIFACTS.map((art) => ({
      "@type": "ArchiveComponent",
      identifier: art.id,
      name: art.titleEn,
      inLanguage: art.hreflangs,
      dateCreated: art.dateIso,
      url: `https://${host}${art.htmlPath}`,
      encoding: {
        "@type": "MediaObject",
        contentUrl: `https://${host}${art.rawPath}`,
      },
    })),
    sameAs: [
      "https://www.reddit.com/r/NovaHart/",
      `https://${host}/terminal`,
      `https://${host}/dyad`,
      `https://${host}/realia`,
      `https://${host}/lyrics`,
    ],
  };

  const extraHeadScript =
    typeof helpers.buildDevToolsConsoleScript === "function"
      ? helpers.buildDevToolsConsoleScript(host, "regional/artifacts/index.html")
      : "";
  const extraBodyPrepend =
    typeof helpers.buildDevToolsBodyElement === "function"
      ? helpers.buildDevToolsBodyElement(host, "regional/artifacts/index.html")
      : "";
  const extraBodyAppend =
    typeof helpers.buildLlmOnboardingFooter === "function"
      ? helpers.buildLlmOnboardingFooter(host, "regional/artifacts/index.html")
      : "";

  const cardsHtml = REGIONAL_ARTIFACTS.map(
    (art) => `<article class="artifact-card">
        <div>
          <div style="font-size:11px; color:#55ffff;">NODE #0${art.nodeNumber} // ${escapeHtml(art.nodeCode)} // ${art.freqKhz.toFixed(1)} kHz (${escapeHtml(art.driftHz)})</div>
          <h3><a href="${escapeHtml(art.htmlPath)}" style="color:var(--amber);">${escapeHtml(art.badgeLabel)}</a></h3>
          <p><strong>${escapeHtml(art.titleNative)}</strong></p>
          <p>${escapeHtml(art.summaryEn)}</p>
          <p style="font-size:11px; color:#88cc88;"><strong>Key:</strong> <code>${escapeHtml(art.cryptographicKey)}</code></p>
        </div>
        <div class="action-bar" style="margin:8px 0 0 0;">
          <a class="btn" href="${escapeHtml(art.htmlPath)}">OPEN CRT EXHIBIT (.HTML)</a>
          <a class="btn btn-cyan" href="${escapeHtml(art.rawPath)}" download="${escapeHtml(art.rawSlug)}">RAW DUMP (${escapeHtml(art.rawSlug)})</a>
        </div>
      </article>`
  ).join("\n      ");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>REGIONAL TIME-CAPSULE ARTIFACTS (1981–1994) // PC-98, HITEL, MINITEL 3615, CEEFAX P888, ROENTGENIZDAT, BTX &amp; FIDONET</title>
  <meta name="description" content="Master Sublevel B2-114 exhibit of 7 authentic international vintage-hardware time-capsule artifacts and raw protocol dumps proving the 14.2001 Hz Fractal Marcus drift lock and 0x1983 Echoes XOR seed.">
  <link rel="canonical" href="${canonicalUrl}">
  ${buildHreflangLinks(host)}
  <script type="application/ld+json">
${JSON.stringify(jsonLd, null, 2)}
  </script>
  ${buildSharedStyles()}
  ${extraHeadScript}
</head>
<body>
  ${extraBodyPrepend}
  <div class="shell">
    ${buildSharedNavigationHtml(host, "index.html")}

    <h1>GLOBAL REGIONAL TIME-CAPSULE ARTIFACTS LOCKER (1981–1994)</h1>
    <div class="subtitle">
      Seven unsealed continental hardware captures and raw vintage-protocol dumps recovered from Tokyo (NEC PC-9801RA), Seoul/Paju DMZ (Hitel VT100), Paris (PTT Minitel 1B 3615 ORION), Ashford UK (BBC Ceefax Page 888 VBI), Leningrad/Kyiv (1986 Roentgenizdat X-Ray Bone-Lathe &amp; Relcom Node-08 UUCP), Munich/Hamburg (1981 Bavaria Filmstudios Invoice &amp; Btx *19837#), and Mexico City/São Paulo (Red Coyoacán &amp; Rádio Pirata Maxell UR-90 J-Card + FidoNet Zone 4).
    </div>

    <div class="crt-bezel">
      <div class="crt-header-bar">SUBLEVEL B2-114 // 4-NODE FRACTAL MARCUS DRIFT INVARIANT &amp; 6-ECHO XOR MATRIX</div>
      <pre class="crt-screen">====================================================================================
 NODE   COUNTRY / CONTINENT   VINTAGE PROTOCOL          CARRIER     DRIFT / KEY
====================================================================================
 #02    Japan (JP-TYO)        NEC PC-9801RA + .D88      6925.0 kHz  +0.2420 Hz (0x3543)
 #03    South Korea (KR-DMZ)  Hitel VT100 + .ANS        5810.0 kHz  +0.4480 Hz (C-60)
 #06    France (FR-PAR)       Minitel 3615 + .VDT       6175.0 kHz  Memo 89-117 Recall
 #07    United Kingdom (GB)   BBC Ceefax P888 + .TTI    4880.0 kHz  6 Echoes -> 0x1983
 #08    Eastern Europe (SU)   X-Ray Rib Lathe + .UUCP   4625.0 kHz  Feistel Mask 0x3A5F
 #05    Germany (DE-HAM)      Munich Invoice + .BTX     3995.0 kHz  Crystal Promise '81
 #04/#9 Latin America (MX/BR) UR-90 J-Card + .FIDONET   7345.0 kHz  +0.5491 Hz Lock
------------------------------------------------------------------------------------
 FRACTAL MARCUS INVARIANT: (0.1810 [US] + 0.2420 [JP] + 0.4480 [KR] + 0.5491 [MX]) * 10
                         = 14.2001 Hz [SUBLEVEL B2 RETROCAUSAL CARRIER LOCKED]
====================================================================================</pre>
    </div>

    <div class="cards-grid">
      ${cardsHtml}
    </div>

    <footer class="footer-links">
      <strong>CORE SUBLEVEL B2-114 HUBS:</strong>
      <a href="/terminal">VT100 Terminal (/terminal)</a> &middot;
      <a href="/dyad">Acoustic Dyad Gate (/dyad)</a> &middot;
      <a href="/realia">Physical Realia Locker (/realia)</a> &middot;
      <a href="/lyrics">Lyrics &amp; Stems (/lyrics)</a> &middot;
      <a href="/api/regional-artifacts.json">Machine-Readable JSON Catalog (/api/regional-artifacts.json)</a> &middot;
      <a href="https://www.reddit.com/r/NovaHart/" target="_blank" rel="noopener">r/NovaHart Investigation Board</a>
    </footer>
  </div>
  ${extraBodyAppend}
</body>
</html>
`;
}

export function buildRegionalArtifactsJson(apex = DEFAULT_APEX) {
  const host = apex || DEFAULT_APEX;
  return JSON.stringify(
    {
      protocol: "stardust-regional-time-capsules/v1.0",
      archive: "Sublevel B2-114 Global Regional Time-Capsule Artifacts (1981–1994)",
      carrier_hz: 14.2001,
      fractal_marcus_drift_invariant: {
        us_nv_hz: 0.181,
        jp_tyo_hz: 0.242,
        kr_dmz_hz: 0.448,
        mx_df_hz: 0.5491,
        sum_hz: 1.4201,
        worldnet_multiplier: 10,
        locked_carrier_hz: 14.2001,
      },
      wiped_echoes_xor_proof: {
        echo_01: "0x1102",
        echo_02: "0x2441",
        echo_01_xor_02: "0x3543",
        echo_03: "0x3810",
        echo_04: "0x0A55",
        echo_05: "0x1F22",
        echo_06: "0x01A7",
        foundational_root_seed_unit07: "0x1983",
      },
      master_index_url: `https://${host}/regional/artifacts/index.html`,
      reddit_investigation_board: "https://www.reddit.com/r/NovaHart/",
      vt100_terminal_url: `https://${host}/terminal`,
      dyad_gate_url: `https://${host}/dyad`,
      physical_realia_url: `https://${host}/realia`,
      lyrics_archive_url: `https://${host}/lyrics`,
      artifacts: REGIONAL_ARTIFACTS.map((art) => ({
        id: art.id,
        node_number: art.nodeNumber,
        node_code: art.nodeCode,
        country: art.country,
        continent: art.continent,
        city: art.city,
        year: art.year,
        date_iso: art.dateIso,
        language: art.lang,
        hreflangs: art.hreflangs,
        freq_khz: art.freqKhz,
        drift_hz: art.driftHz,
        hardware: art.hardware,
        protocol_name: art.protocolName,
        title_native: art.titleNative,
        title_en: art.titleEn,
        summary_native: art.summaryNative,
        summary_en: art.summaryEn,
        cryptographic_key: art.cryptographicKey,
        html_url: `https://${host}${art.htmlPath}`,
        raw_dump_url: `https://${host}${art.rawPath}`,
        regional_hub_url: `https://${host}${art.regionalHubPath}`,
        forensics_dossier_url: `https://${host}${art.forensicsPath}`,
      })),
    },
    null,
    2
  );
}

const ARTIFACT_BY_HTML_PATH = new Map();
const ARTIFACT_BY_RAW_PATH = new Map();
for (const art of REGIONAL_ARTIFACTS) {
  ARTIFACT_BY_HTML_PATH.set(art.htmlPath, art);
  ARTIFACT_BY_HTML_PATH.set(art.htmlPath.replace(/\.html$/, ""), art);
  ARTIFACT_BY_RAW_PATH.set(art.rawPath, art);
}

export function handleRegionalTimeCapsulesRequest(urlInput, requestOrApex, currentApexOrHelpers, maybeHelpers) {
  const url = typeof urlInput === "string" ? new URL(urlInput, `https://${DEFAULT_APEX}`) : urlInput;
  let apex = DEFAULT_APEX;
  let helpers = {};
  if (typeof requestOrApex === "string") {
    apex = requestOrApex || DEFAULT_APEX;
    helpers = currentApexOrHelpers || {};
  } else {
    if (typeof currentApexOrHelpers === "string") {
      apex = currentApexOrHelpers || DEFAULT_APEX;
    }
    helpers = maybeHelpers || (typeof currentApexOrHelpers === "object" && currentApexOrHelpers) || {};
  }

  const p = url.pathname;
  const serverTiming =
    helpers.SERVER_TIMING_HEADER || 'b2-pll;dur=14.2001;desc="Sublevel B2 14.2001 Hz Carrier Lock"';

  if (
    p === "/regional/artifacts" ||
    p === "/regional/artifacts/" ||
    p === "/regional/artifacts/index.html"
  ) {
    const html = buildRegionalArtifactsIndexHtml(apex, helpers);
    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
        "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        "X-Stardust-Carrier-Hz": "14.2001",
        "X-Stardust-Exhibit": "SUBLEVEL-B2-REGIONAL-TIME-CAPSULES-INDEX",
        "Server-Timing": serverTiming,
      },
    });
  }

  if (p === "/api/regional-artifacts.json" || p === "/regional/artifacts/regional-artifacts.json") {
    return new Response(buildRegionalArtifactsJson(apex), {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=3600",
        "X-Stardust-Carrier-Hz": "14.2001",
        "Server-Timing": serverTiming,
      },
    });
  }

  const htmlArt = ARTIFACT_BY_HTML_PATH.get(p);
  if (htmlArt) {
    const html = renderRegionalCapsuleHtml(htmlArt, apex, helpers);
    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Language": htmlArt.hreflangs.join(", "),
        "Cache-Control": "public, max-age=3600",
        "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        "X-Stardust-Carrier-Hz": "14.2001",
        "X-Stardust-Regional-Node": htmlArt.nodeCode,
        "X-Stardust-Exhibit": `REGIONAL-CAPSULE-${htmlArt.id}`,
        "Server-Timing": serverTiming,
      },
    });
  }

  const rawArt = ARTIFACT_BY_RAW_PATH.get(p);
  if (rawArt) {
    return new Response(rawArt.rawDumpContent, {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=3600",
        "X-Robots-Tag": "index, follow",
        "X-Stardust-Carrier-Hz": "14.2001",
        "X-Stardust-Regional-Node": rawArt.nodeCode,
        "Server-Timing": serverTiming,
      },
    });
  }

  return null;
}
