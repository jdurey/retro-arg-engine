"""GeoCities-era (1995-1996) HTML 3.2 homepage generator with webrings and hit counters."""
import json
import os

from common import esc, relay_table_lines, rng_for, write
from swarm_corner import generate_swarm_homepage

DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
RING = "The Stardust Webring"

HOOD_THEMES = {
    "SiliconValley/Lab": "DSP Hackers, Hardware Modems, Audio Spectrograms",
    "Hollywood/Hills": "Nova Hart Shrines, Los Angeles Lore, Media Archives",
    "SunsetStrip/Club": "80s Synthpop, Tape Trading Clubs, Neon Aesthetics",
    "Area51/Vault": "Government Conspiracies, Marcus Hale Case Files",
    "Tokyo/Garden": "Akasaka Master Tapes, PC-98 Users, J-Pop Otaku",
    "Athens/Forum": "University DSP Researchers, Fourier Analysis Labs",
    "Paris/LeftBank": "European Fan Clubs, 3615 Minitel Transmissions",
    "CapeCanaveral/Lab": "Satellite Telemetry, Microwave Relay Links",
    "Heartland/Plains": "Midwest Tape Traders, Ham Radio Enthusiasts",
    "SoHo/Studio": "Underground Cassette Culture, Synthwave Aesthetics",
    "Vienna/Strasse": "German & Austrian Broadcast Archives",
    "Colosseum/Field": "International Pen-Pals, Vinyl Collectors",
    "TimesSquare/Arcade": "East Coast Synth Fans, 80s Billboard Lore",
    "Nashville/Opry": "Session Musicians, Studio Vocal Analysis",
    "RainForest/Canopy": "South American Transmissions, Red Saturno BBS",
    "Pentagon/Quarters": "DoD Declassified Signal Intercepts",
    "BourbonStreet/Delta": "Southern Audio Engineers, Reel-to-Reel Collectors",
    "EnchantedForest/Glade": "Fantasy & Anime Fan Art, Tribute Pages",
}

LANG_INFO = {
    "ja": {"name": "日本語 (Japanese)", "region": "Tokyo & Akasaka Fan Shrines", "node": "Node 02 (Kamome BBS)"},
    "es": {"name": "Español (Spanish)", "region": "México, D.F. & Red Coyoacán", "node": "Node 04 (Red Coyoacán)"},
    "ru": {"name": "Русский (Russian)", "region": "Relcom Magnitizdat & St. Petersburg", "node": "Node 08 (Relcom Node 08)"},
    "pt": {"name": "Português (Portuguese)", "region": "Brasil & Rede Saturno (Porto Alegre)", "node": "Node 09 (Rede Saturno)"},
    "de": {"name": "Deutsch (German)", "region": "Hamburg, Wien & Knoten 05", "node": "Node 05 (Hanse-Box / Uni-HH)"},
    "fr": {"name": "Français (French)", "region": "Paris, Lyon & Minitel 3615", "node": "Node 06 (Stardust 3615)"},
    "it": {"name": "Italiano (Italian)", "region": "Milano, Roma & Nodo 07 Ricordi", "node": "Node 07 (CINECA / Ricordi)"},
    "hi": {"name": "हिन्दी (Hindi)", "region": "New Delhi, Mumbai & VSNL Gateway", "node": "Node 11 (VSNL Gateway)"},
    "ko": {"name": "한국어 (Korean)", "region": "Seoul, Busan & EunhaNet Paju", "node": "Node 03 (EunhaNet / HiTEL)"},
    "sv": {"name": "Svenska (Swedish)", "region": "Uppsala, Göteborg & SUNET Nod 10", "node": "Node 10 (SUNET / Lysator)"},
    "au": {"name": "English (Australia)", "region": "Melbourne, Sydney & OzEmail Node 12", "node": "Node 12 (OzEmail / APANA)"},
    "fj": {"name": "Vosa Vakaviti (Fiji / Pacific)", "region": "Suva, USP Satellite & South Pacific DX", "node": "Node 13 (USP Pacific Relay)"},
    "en": {"name": "English (Global / US / UK)", "region": "North America, UK & International Shrines", "node": "Node 01 (Northvale Gopher)"},
}

UI_LANGS = {
    "en": {
        "stats_title": "HOMESTEAD STATS",
        "visitor": "Visitor #:",
        "updated": "Updated:",
        "station_label": "Webring Station",
        "station_of": "Station #%d of %d",
        "links_title": "Cool Links",
        "email": "Email %s",
        "guestbook": "Sign Guestbook",
        "directory": "Homestead Directory",
        "disclaimer": "Hosted Free by GeoCities &middot; Best viewed with Netscape Navigator 2.0 at 640x480",
        "webring_banner": "&#10022; This <B>%s</B> site is station #%d of %d &#10022;",
        "prev": "&lt;&lt; Prev",
        "random": "Random",
        "list": "List Stations",
        "next": "Next &gt;&gt;",
        "top_hoods": "Neighborhoods",
        "top_featured": "Featured Hub",
        "top_dir": "Homestead Directory",
        "nav_hood": "Neighborhood",
        "nav_lang": "Language",
        "nav_all": "All Neighborhoods",
        "term_node": "TERMINAL NODE",
        "term_station": "STATION",
        "term_updated": "UPDATED",
        "term_matrix": "[ HYPERLINK MATRIX ]",
        "term_sysop": "[ CONTACT SYSOP: %s ]",
        "term_archive": "[ ARCHIVE INDEX ]",
        "hub_home": "HOME",
        "hub_articles": "ARTICLES",
        "hub_links": "LINKS",
        "hub_mailbox": "MAILBOX",
        "hub_listener": "You are listener number:",
        "hub_updated": "Broadcast log updated: %s",
        "hub_ring_net": "The Stardust Ring Network",
        "shrine_copy": "My original 1985 copy. Scanned at Kinko's!",
        "shrine_visitor": "You are visitor number",
        "shrine_updated": "Last updated: %s",
    },
    "ja": {
        "stats_title": "ホームページ統計",
        "visitor": "訪問者数:",
        "updated": "更新日時:",
        "station_label": "ステーション",
        "station_of": "第 %d 番 (全 %d 局)",
        "links_title": "おすすめリンク",
        "email": "%s にメールを送る",
        "guestbook": "ゲストブックに記帳",
        "directory": "ホームステッド一覧",
        "disclaimer": "GeoCities による無料ホスティング &middot; Netscape Navigator 2.0 (640x480) 推奨",
        "webring_banner": "&#10022; この<B>%s</B>サイトはステーション第 %d 番 (全 %d 局) です &#10022;",
        "prev": "&lt;&lt; 前へ",
        "random": "ランダム",
        "list": "ステーション一覧",
        "next": "次へ &gt;&gt;",
        "top_hoods": "コミュニティ",
        "top_featured": "注目サイト",
        "top_dir": "ディレクトリ",
        "nav_hood": "地域コミュニティ",
        "nav_lang": "言語ハブ",
        "nav_all": "全地区ディレクトリ",
        "term_node": "端末ノード",
        "term_station": "局番号",
        "term_updated": "更新",
        "term_matrix": "[ ハイパーリンク群 ]",
        "term_sysop": "[ 管理者への連絡: %s ]",
        "term_archive": "[ アーカイブ目次 ]",
        "hub_home": "トップ",
        "hub_articles": "記事",
        "hub_links": "リンク集",
        "hub_mailbox": "連絡先",
        "hub_listener": "あなたは番目のリスナーです:",
        "hub_updated": "放送ログ更新: %s",
        "hub_ring_net": "スターダスト・リング・ネットワーク",
        "shrine_copy": "1985年のオリジナル日本盤。キンコーズでスキャン！",
        "shrine_visitor": "あなたは人目の訪問者です",
        "shrine_updated": "最終更新: %s",
    },
    "ru": {
        "stats_title": "СТАТИСТИКА УЗЛА",
        "visitor": "Посетитель №:",
        "updated": "Обновлено:",
        "station_label": "Станция кольца",
        "station_of": "Узел #%d из %d",
        "links_title": "Интересные ссылки",
        "email": "Написать %s",
        "guestbook": "Гостевая книга",
        "directory": "Каталог GeoCities",
        "disclaimer": "Бесплатный хостинг GeoCities &middot; Лучше всего смотреть в Netscape Navigator 2.0 (640x480)",
        "webring_banner": "&#10022; Этот сайт сети <B>%s</B> — станция #%d из %d &#10022;",
        "prev": "&lt;&lt; Назад",
        "random": "Случайный",
        "list": "Список станций",
        "next": "Вперед &gt;&gt;",
        "top_hoods": "Районы",
        "top_featured": "Главная",
        "top_dir": "Каталог",
        "nav_hood": "Район GeoCities",
        "nav_lang": "Языковой хаб",
        "nav_all": "Главный каталог",
        "term_node": "ТЕРМИНАЛЬНЫЙ УЗЕЛ",
        "term_station": "СТАНЦИЯ",
        "term_updated": "ОБНОВЛЕНО",
        "term_matrix": "[ МАТРИЦА ССЫЛОК ]",
        "term_sysop": "[ СВЯЗЬ С СИСОПОМ: %s ]",
        "term_archive": "[ ИНДЕКС АРХИВА ]",
        "hub_home": "ГЛАВНАЯ",
        "hub_articles": "СТАТЬИ",
        "hub_links": "ССЫЛКИ",
        "hub_mailbox": "ПОЧТА",
        "hub_listener": "Вы слушатель номер:",
        "hub_updated": "Журнал трансляций обновлен: %s",
        "hub_ring_net": "Сеть вещания Stardust",
        "shrine_copy": "Моя копия 1985 года. Отсканировано на цветном сканере!",
        "shrine_visitor": "Вы посетитель номер",
        "shrine_updated": "Последнее обновление: %s",
    },
    "es": {
        "stats_title": "ESTADÍSTICAS",
        "visitor": "Visitante #:",
        "updated": "Actualizado:",
        "station_label": "Estación del Anillo",
        "station_of": "Estación #%d de %d",
        "links_title": "Enlaces Recomendados",
        "email": "Enviar correo a %s",
        "guestbook": "Firmar Libro de Visitas",
        "directory": "Directorio GeoCities",
        "disclaimer": "Alojado gratis por GeoCities &middot; Mejor visualizado con Netscape Navigator 2.0 a 640x480",
        "webring_banner": "&#10022; Este sitio de <B>%s</B> es la estación #%d de %d &#10022;",
        "prev": "&lt;&lt; Anterior",
        "random": "Aleatorio",
        "list": "Lista de Estaciones",
        "next": "Siguiente &gt;&gt;",
        "top_hoods": "Vecindarios",
        "top_featured": "Destacados",
        "top_dir": "Directorio",
        "nav_hood": "Vecindario",
        "nav_lang": "Idioma",
        "nav_all": "Directorio General",
        "term_node": "NODO TERMINAL",
        "term_station": "ESTACIÓN",
        "term_updated": "ACTUALIZADO",
        "term_matrix": "[ MATRIZ DE ENLACES ]",
        "term_sysop": "[ CONTACTAR AL SYSOP: %s ]",
        "term_archive": "[ ÍNDICE GENERAL ]",
        "hub_home": "INICIO",
        "hub_articles": "ARTÍCULOS",
        "hub_links": "ENLACES",
        "hub_mailbox": "CORREO",
        "hub_listener": "Eres el oyente número:",
        "hub_updated": "Registro de emisión actualizado: %s",
        "hub_ring_net": "La Red del Anillo Stardust",
        "shrine_copy": "Mi copia original de 1985 (Orion México). ¡Escaneada en papelería!",
        "shrine_visitor": "Eres el visitante número",
        "shrine_updated": "Última actualización: %s",
    },
    "pt": {
        "stats_title": "ESTATÍSTICAS DA PÁGINA",
        "visitor": "Visitante nº:",
        "updated": "Atualizado:",
        "station_label": "Estação do Anel",
        "station_of": "Estação #%d de %d",
        "links_title": "Links Recomendados",
        "email": "Enviar e-mail para %s",
        "guestbook": "Assinar Livro de Visitas",
        "directory": "Diretório GeoCities",
        "disclaimer": "Hospedado gratuitamente no GeoCities &middot; Melhor visualizado com Netscape Navigator 2.0",
        "webring_banner": "&#10022; Este site do <B>%s</B> é a estação #%d de %d &#10022;",
        "prev": "&lt;&lt; Anterior",
        "random": "Aleatório",
        "list": "Lista de Estações",
        "next": "Próximo &gt;&gt;",
        "top_hoods": "Bairros",
        "top_featured": "Destaque",
        "top_dir": "Diretório",
        "nav_hood": "Bairro",
        "nav_lang": "Idioma",
        "nav_all": "Diretório Geral",
        "term_node": "NÓ TERMINAL",
        "term_station": "ESTAÇÃO",
        "term_updated": "ATUALIZADO",
        "term_matrix": "[ MATRIZ DE HIPERLINKS ]",
        "term_sysop": "[ CONTATO SYSOP: %s ]",
        "term_archive": "[ ÍNDICE DO ARQUIVO ]",
        "hub_home": "INÍCIO",
        "hub_articles": "ARTIGOS",
        "hub_links": "LINKS",
        "hub_mailbox": "CORREIO",
        "hub_listener": "Você é o ouvinte número:",
        "hub_updated": "Log de transmissão atualizado: %s",
        "hub_ring_net": "Rede do Anel Stardust",
        "shrine_copy": "Meu vinil de 1985 (Orion do Brasil). Capa original!",
        "shrine_visitor": "Você é o visitante número",
        "shrine_updated": "Última atualização: %s",
    },
    "de": {
        "stats_title": "HOMESTEAD STATISTIK",
        "visitor": "Besucher-Nr.:",
        "updated": "Aktualisiert:",
        "station_label": "Webring Station",
        "station_of": "Station #%d von %d",
        "links_title": "Interessante Links",
        "email": "E-Mail an %s",
        "guestbook": "Gästebuch",
        "directory": "GeoCities Verzeichnis",
        "disclaimer": "Kostenlos gehostet bei GeoCities &middot; Optimiert für Netscape Navigator 2.0 (640x480)",
        "webring_banner": "&#10022; Diese <B>%s</B> Seite ist Station #%d von %d &#10022;",
        "prev": "&lt;&lt; Zurück",
        "random": "Zufall",
        "list": "Stationen-Liste",
        "next": "Weiter &gt;&gt;",
        "top_hoods": "Nachbarschaften",
        "top_featured": "Zentrale",
        "top_dir": "Verzeichnis",
        "nav_hood": "Nachbarschaft",
        "nav_lang": "Sprache",
        "nav_all": "Gesamtverzeichnis",
        "term_node": "TERMINAL KNOTEN",
        "term_station": "STATION",
        "term_updated": "AKTUALISIERT",
        "term_matrix": "[ HYPERLINK-MATRIX ]",
        "term_sysop": "[ SYSOP KONTAKTIEREN: %s ]",
        "term_archive": "[ ARCHIV-INDEX ]",
        "hub_home": "START",
        "hub_articles": "ARTIKEL",
        "hub_links": "LINKS",
        "hub_mailbox": "POSTFACH",
        "hub_listener": "Sie sind Hörer Nummer:",
        "hub_updated": "Sendeprotokoll aktualisiert: %s",
        "hub_ring_net": "Das Stardust Ringnetzwerk",
        "shrine_copy": "Meine originale deutsche Pressung von 1985!",
        "shrine_visitor": "Sie sind Besucher Nummer",
        "shrine_updated": "Zuletzt aktualisiert: %s",
    },
    "fr": {
        "stats_title": "STATISTIQUES DE LA PAGE",
        "visitor": "Visiteur nº :",
        "updated": "Mis à jour :",
        "station_label": "Station du Webring",
        "station_of": "Station #%d sur %d",
        "links_title": "Liens Préférés",
        "email": "Écrire à %s",
        "guestbook": "Livre d'or",
        "directory": "Annuaire GeoCities",
        "disclaimer": "Hébergé gratuitement par GeoCities &middot; Recommandé avec Netscape Navigator 2.0 (640x480)",
        "webring_banner": "&#10022; Ce site du <B>%s</B> est la station #%d sur %d &#10022;",
        "prev": "&lt;&lt; Précédent",
        "random": "Aléatoire",
        "list": "Liste des Stations",
        "next": "Suivant &gt;&gt;",
        "top_hoods": "Quartiers",
        "top_featured": "En Vedette",
        "top_dir": "Annuaire",
        "nav_hood": "Quartier",
        "nav_lang": "Langue",
        "nav_all": "Annuaire Complet",
        "term_node": "NŒUD TERMINAL",
        "term_station": "STATION",
        "term_updated": "MIS À JOUR",
        "term_matrix": "[ MATRICE DE LIENS ]",
        "term_sysop": "[ CONTACTER LE SYSOP: %s ]",
        "term_archive": "[ INDEX DES ARCHIVES ]",
        "hub_home": "ACCUEIL",
        "hub_articles": "ARTICLES",
        "hub_links": "LIENS",
        "hub_mailbox": "MESSAGERIE",
        "hub_listener": "Vous êtes l'auditeur numéro :",
        "hub_updated": "Journal de diffusion mis à jour : %s",
        "hub_ring_net": "Réseau du Stardust Webring",
        "shrine_copy": "Mon exemplaire original français de 1985 !",
        "shrine_visitor": "Vous êtes le visiteur numéro",
        "shrine_updated": "Dernière mise à jour : %s",
    },
    "it": {
        "stats_title": "STATISTICHE HOMESTEAD",
        "visitor": "Visitatore n°:",
        "updated": "Aggiornato:",
        "station_label": "Stazione Webring",
        "station_of": "Stazione #%d di %d",
        "links_title": "Collegamenti Consigliati",
        "email": "Scrivi a %s",
        "guestbook": "Firma il Guestbook",
        "directory": "Directory GeoCities",
        "disclaimer": "Ospitato gratuitamente su GeoCities &middot; Ottimizzato per Netscape Navigator 2.0 a 640x480",
        "webring_banner": "&#10022; Questo sito del <B>%s</B> è la stazione #%d di %d &#10022;",
        "prev": "&lt;&lt; Prec",
        "random": "Casuale",
        "list": "Elenco Stazioni",
        "next": "Succ &gt;&gt;",
        "top_hoods": "Quartieri",
        "top_featured": "In Evidenza",
        "top_dir": "Directory",
        "nav_hood": "Quartiere",
        "nav_lang": "Lingua",
        "nav_all": "Directory Completa",
        "term_node": "NODO TERMINALE",
        "term_station": "STAZIONE",
        "term_updated": "AGGIORNATO",
        "term_matrix": "[ MATRICE COLLEGAMENTI ]",
        "term_sysop": "[ CONTATTA SYSOP: %s ]",
        "term_archive": "[ INDICE ARCHIVIO ]",
        "hub_home": "HOME",
        "hub_articles": "ARTICOLI",
        "hub_links": "LINK",
        "hub_mailbox": "POSTA",
        "hub_listener": "Sei l'ascoltatore numero:",
        "hub_updated": "Registro di trasmissione aggiornato: %s",
        "hub_ring_net": "La Rete Webring Stardust",
        "shrine_copy": "La mia copia originale italiana del 1985 (Ricordi)!",
        "shrine_visitor": "Sei il visitatore numero",
        "shrine_updated": "Ultimo aggiornamento: %s",
    },
    "hi": {
        "stats_title": "होमस्टेड आंकड़े",
        "visitor": "आगंतुक संख्या:",
        "updated": "अंतिम नवीनीकरण:",
        "station_label": "वेबरिंग स्टेशन",
        "station_of": "स्टेशन #%d (कुल %d)",
        "links_title": "पसंदीदा लिंक्स",
        "email": "%s को ईमेल भेजें",
        "guestbook": "गेस्टबुक पर हस्ताक्षर करें",
        "directory": "जियोसिटीज डायरेक्टरी",
        "disclaimer": "जियोसिटीज द्वारा निःशुल्क होस्ट किया गया &middot; नेटस्केप नेविगेटर 2.0 (640x480) के लिए उपयुक्त",
        "webring_banner": "&#10022; यह <B>%s</B> साइट स्टेशन #%d है (कुल %d में से) &#10022;",
        "prev": "&lt;&lt; पिछला",
        "random": "रैंडम",
        "list": "स्टेशन सूची",
        "next": "अगला &gt;&gt;",
        "top_hoods": "नेबरहुड",
        "top_featured": "मुख्य हब",
        "top_dir": "डायरेक्टरी",
        "nav_hood": "नेबरहुड",
        "nav_lang": "भाषा",
        "nav_all": "संपूर्ण डायरेक्टरी",
        "term_node": "टर्मिनल नोड",
        "term_station": "स्टेशन",
        "term_updated": "नवीनीकृत",
        "term_matrix": "[ हाइपरलिंक मैट्रिक्स ]",
        "term_sysop": "[ सिस्ऑप से संपर्क: %s ]",
        "term_archive": "[ आर्काइव इंडेक्स ]",
        "hub_home": "होम",
        "hub_articles": "लेख",
        "hub_links": "लिंक्स",
        "hub_mailbox": "मेलबॉक्स",
        "hub_listener": "आप श्रोता संख्या हैं:",
        "hub_updated": "प्रसारण लॉग नवीनीकृत: %s",
        "hub_ring_net": "स्टारडस्ट वेबरिंग नेटवर्क",
        "shrine_copy": "मेरी 1985 की मूल कैसेट (पालिका बाज़ार प्रति)!",
        "shrine_visitor": "आप आगंतुक संख्या हैं",
        "shrine_updated": "अंतिम नवीनीकरण: %s",
    },
    "ko": {
        "stats_title": "홈페이지 접속 통계",
        "visitor": "방문자 수:",
        "updated": "최종 수정:",
        "station_label": "웹링 스테이션",
        "station_of": "스테이션 #%d / 총 %d개",
        "links_title": "추천 링크 모음",
        "email": "%s 에게 메일 쓰기",
        "guestbook": "방명록 남기기",
        "directory": "지오시티 디렉토리",
        "disclaimer": "지오시티 무료 호스팅 &middot; 넷스케이프 내비게이터 2.0 권장 (640x480)",
        "webring_banner": "&#10022; 이 <B>%s</B> 사이트는 #%d번째 스테이션입니다 (총 %d국) &#10022;",
        "prev": "&lt;&lt; 이전",
        "random": "랜덤",
        "list": "목록",
        "next": "다음 &gt;&gt;",
        "top_hoods": "이웃/동네",
        "top_featured": "추천 사이트",
        "top_dir": "디렉토리",
        "nav_hood": "동네/이웃",
        "nav_lang": "언어",
        "nav_all": "전체 디렉토리",
        "term_node": "터미널 노드",
        "term_station": "스테이션",
        "term_updated": "갱신일",
        "term_matrix": "[ 하이퍼링크 매트릭스 ]",
        "term_sysop": "[ 시스옵 연락처: %s ]",
        "term_archive": "[ 아카이브 색인 ]",
        "hub_home": "홈",
        "hub_articles": "게시글",
        "hub_links": "링크",
        "hub_mailbox": "우편함",
        "hub_listener": "당신은 번째 청취자입니다:",
        "hub_updated": "방송 기록 업데이트: %s",
        "hub_ring_net": "스타더스트 링 네트워크",
        "shrine_copy": "1985년 한국 라이선스 LP 초판본!",
        "shrine_visitor": "당신은 번째 방문자입니다",
        "shrine_updated": "최종 갱신: %s",
    },
    "sv": {
        "stats_title": "STATISTIK",
        "visitor": "Besökare #:",
        "updated": "Uppdaterad:",
        "station_label": "Webring Station",
        "station_of": "Station #%d av %d",
        "links_title": "Bra Länkar",
        "email": "E-posta till %s",
        "guestbook": "Gästbok",
        "directory": "GeoCities Register",
        "disclaimer": "Gratis värdskap via GeoCities &middot; Bäst i Netscape Navigator 2.0 (640x480)",
        "webring_banner": "&#10022; Denna <B>%s</B>-sida är station #%d av %d &#10022;",
        "prev": "&lt;&lt; Föreg",
        "random": "Slumpa",
        "list": "Lista",
        "next": "Nästa &gt;&gt;",
        "top_hoods": "Områden",
        "top_featured": "Utvald Hub",
        "top_dir": "Register",
        "nav_hood": "Område",
        "nav_lang": "Språk",
        "nav_all": "Hela Registret",
        "term_node": "TERMINALNOD",
        "term_station": "STATION",
        "term_updated": "UPPDATERAD",
        "term_matrix": "[ HYPERLÄNKMATRIS ]",
        "term_sysop": "[ KONTAKTA SYSOP: %s ]",
        "term_archive": "[ ARKIVINDEX ]",
        "hub_home": "HEM",
        "hub_articles": "ARTIKLAR",
        "hub_links": "LÄNKAR",
        "hub_mailbox": "BREVLÅDA",
        "hub_listener": "Du är lyssnare nummer:",
        "hub_updated": "Sändningslogg uppdaterad: %s",
        "hub_ring_net": "Stardust Nätverksring",
        "shrine_copy": "Min svenska pressning från 1985!",
        "shrine_visitor": "Du är besökare nummer",
        "shrine_updated": "Senast uppdaterad: %s",
    },
    "fj": {
        "stats_title": "HOMESTEAD STATS // PASIFIKA",
        "visitor": "Naba ni Vulagi:",
        "updated": "Vakavoutaki:",
        "station_label": "Webring Station",
        "station_of": "Station #%d mai na %d",
        "links_title": "Veika Veiwekani Vinaka",
        "email": "Tukutuku ki vei %s",
        "guestbook": "Volayaca e na Guestbook",
        "directory": "GeoCities Directory",
        "disclaimer": "Hosted Free by GeoCities &middot; Bula Vinaka! Best viewed with Netscape Navigator 2.0",
        "webring_banner": "&#10022; Na vanua oqo <B>%s</B> e naba #%d mai na %d &#10022;",
        "prev": "&lt;&lt; Sa Oti",
        "random": "Rerevaki",
        "list": "Lisi ni Stations",
        "next": "Tarava &gt;&gt;",
        "top_hoods": "Veitikina",
        "top_featured": "Vanua Dokai",
        "top_dir": "Directory",
        "nav_hood": "Veitikina",
        "nav_lang": "Vosa",
        "nav_all": "Directory Taucoko",
        "term_node": "TERMINAL NODE",
        "term_station": "STATION",
        "term_updated": "VAKAVOUTAKI",
        "term_matrix": "[ HYPERLINK MATRIX ]",
        "term_sysop": "[ VEITARATARA SYSOP: %s ]",
        "term_archive": "[ ARCHIVE INDEX ]",
        "hub_home": "VALE",
        "hub_articles": "ITUKUTUKU",
        "hub_links": "SEMATA",
        "hub_mailbox": "KATO NI VOLA",
        "hub_listener": "Ko iko na vakarorogo naba:",
        "hub_updated": "Tukutuku vakarorogo vakavoutaki: %s",
        "hub_ring_net": "Stardust Webring Pasifika",
        "shrine_copy": "South Pacific shortwave tape capture from 1985!",
        "shrine_visitor": "Ko iko na vulagi naba",
        "shrine_updated": "Vakavoutaki oti: %s",
    }
}


def counter_html(n):
    digits = "%06d" % n
    cells = "".join('<TD BGCOLOR="#000000"><FONT FACE="Courier New,Courier" COLOR="#33FF33"><B>%s</B></FONT></TD>' % d for d in digits)
    return ('<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0><TR>%s</TR></TABLE>' % cells)


def under_construction():
    stripes = "".join('<TD BGCOLOR="%s" WIDTH=14>&nbsp;</TD>' % ("#FFCC00" if i % 2 == 0 else "#000000") for i in range(16))
    return ('<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>%s</TR></TABLE>'
            '<FONT FACE="Arial,Helvetica" COLOR="#FFCC00"><B>&#9888; UNDER CONSTRUCTION &#9888;</B></FONT>'
            '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0><TR>%s</TR></TABLE>') % (stripes, stripes)


def relay_table_html(lore, hp):
    rows = []
    for n in lore["project_stardust"]["relay_nodes"]:
        known = "?" not in n["line"]
        rows.append('<TR><TD ALIGN=CENTER><TT>%02d</TT></TD><TD>%s</TD><TD><TT>%s</TT></TD></TR>' % (
            n["node"], esc(n["pressing"]), esc(n["line"]) if known else '<BLINK>%s</BLINK>' % esc(n["line"])))
    return ('<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 BORDERCOLOR="%s"><TR><TH>NODE</TH><TH>SOURCE</TH><TH>LINE</TH></TR>%s</TABLE>'
            % (hp["link"], "".join(rows)))


def webring(ctx, slug, ring, i, ui=None):
    if not ui:
        ui = UI_LANGS["en"]
    prev_s, next_s = ring[i - 1], ring[(i + 1) % len(ring)]
    rand_s = ring[rng_for(ctx.seed, "ring", slug).randrange(len(ring))]
    banner = ui.get("webring_banner", "&#10022; This <B>%s</B> site is station #%d of %d &#10022;") % (RING, i + 1, len(ring))
    prev_label = ui.get("prev", "&lt;&lt; Prev")
    rand_label = ui.get("random", "Random")
    list_label = ui.get("list", "List Stations")
    next_label = ui.get("next", "Next &gt;&gt;")
    return ('<CENTER><TABLE BORDER=3 CELLPADDING=4 BGCOLOR="#000000"><TR><TD ALIGN=CENTER>'
            '<FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2>%s<BR>'
            '[ <A HREF="%s.html">%s</A> | <A HREF="%s.html">%s</A> | <A HREF="index.html#ring">%s</A> | <A HREF="%s.html">%s</A> ]'
            '</FONT></TD></TR></TABLE></CENTER>') % (banner, prev_s, prev_label, rand_s, rand_label, list_label, next_s, next_label)


def render_badges(ctx, badges, from_dir):
    if not badges:
        return ""
    imgs = []
    for b in badges:
        imgs.append('<IMG SRC="%s" WIDTH=88 HEIGHT=31 BORDER=1 HSPACE=3 VSPACE=3 ALT="[%s]">' % (
            ctx.link("asset:badges/" + b + ".gif", from_dir), esc(b)))
    imgs.append('<IMG SRC="%s" WIDTH=32 HEIGHT=32 BORDER=0 HSPACE=3 VSPACE=3 ALT="[*]">' % (
        ctx.link("asset:badges/spinning_star.gif", from_dir)))
    return '<CENTER><P>' + "".join(imgs) + '</P></CENTER>'


def midi_jukebox_html(ctx, from_dir):
    midis = [
        ("gasoline_heart", "Gasoline Heart (ガソリン・ハート)", "1985 J-Rock / City Pop Anthem", "7.3 KB"),
        ("these_wings_are_my_own", "These Wings Are My Own", "1985 Epic Power Ballad", "57.1 KB"),
        ("shes_hardwired", "She's Hardwired", "1985 Synthrock / FM Groove", "6.5 KB"),
        ("behind_the_glass", "Behind the Glass", "1985 Arena Rock / Piano Ballad", "52.1 KB"),
        ("chrome_velocity", "Chrome Velocity", "1986 High-Speed Hard Rock", "40.5 KB"),
        ("hearts_on_fire", "Hearts on Fire", "1986 Epic Arena Rock Anthem", "43.2 KB"),
        ("hold_back_the_storm", "Hold Back the Storm", "1986 Atmospheric DX7 Ballad", "25.3 KB"),
        ("before_you_disappear", "Before You Disappear", "1985 Emotional Power Ballad", "28.8 KB"),
        ("static_and_steel", "Static & Steel", "1988 Classic Rock / Multi-track", "75.9 KB"),
        ("run_with_the_fire", "Run With The Fire", "1987 Hard Rock Adrenaline", "56.4 KB"),
        ("ghost_transit", "Ghost Transit (ゴースト・トランジット)", "1985 Atmospheric Ballad", "4.3 KB"),
        ("midnight_animal", "Midnight Animal (ミッドナイト・アニマル)", "1986 Funky City Pop", "6.7 KB"),
        ("brighter_than_sun", "Brighter Than The Sun (太陽よりも、輝いて！)", "1987 80s Idol Anthem", "9.9 KB"),
        ("only_we_remain", "Only We Remain (残されたのは、私たちだけ)", "1989 Kayokyoku Ballad", "4.3 KB"),
        ("togethers_the_way", "Together's the Way", "1984 Sophisti-Pop / Brass Section", "42.8 KB"),
        ("perfect_daydream", "Perfect Daydream", "1984 Breezy Jazz-Pop Broadcast", "39.3 KB"),
        ("summer_of_85", "Summer of '85", "1985 Nostalgic Synth-Rock Ballad", "48.1 KB"),
        ("synthetic_dawn", "Synthetic Dawn", "1985 Industrial Synthwave", "3.7 KB"),
        ("memory_hatch", "Memory Hatch", "1985 Sophisti-Pop / Rhodes", "3.5 KB"),
    ]
    rows = []
    audios = []
    for slug, title, genre, sz in midis:
        m_link = ctx.link(f"asset:midi/{slug}.mid", from_dir)
        s_link = ctx.link(f"asset:audio/streams/{slug}_14k.mp3", from_dir)
        clean_title = esc(title).replace("'", "\\'")
        audios.append('<AUDIO ID="audio_%s" SRC="%s" PRELOAD="none"></AUDIO>' % (slug, s_link))
        rows.append(
            '<TR><TD><FONT FACE="Arial,Helvetica" SIZE=2><B>%s</B></FONT></TD>'
            '<TD><FONT FACE="Arial,Helvetica" SIZE=2>%s</FONT></TD>'
            '<TD ALIGN=RIGHT><TT>%s</TT></TD>'
            '<TD ALIGN=CENTER NOWRAP>'
            '<BUTTON TYPE="BUTTON" ID="btn_%s" ONCLICK="play14k(\'%s\', \'%s\', this)" '
            'STYLE="cursor:pointer; background:#111111; color:#00FF66; border:2px outset #666666; '
            'font-family:Courier New,monospace; font-weight:bold; font-size:11px; padding:2px 7px; margin-right:6px;">'
            '&#9654; 14.4k</BUTTON>'
            '<FONT FACE="Arial,Helvetica" SIZE=2>[ <A HREF="%s"><B>DOWNLOAD .MID</B></A> ]</FONT>'
            '</TD></TR>' % (esc(title), esc(genre), sz, slug, slug, clean_title, m_link)
        )
    
    script = (
        '<SCRIPT>\n'
        'var currentAudio = null;\n'
        'var currentBtn = null;\n'
        'function play14k(slug, title, btn) {\n'
        '  var audio = document.getElementById("audio_" + slug);\n'
        '  var status = document.getElementById("midi_stream_status");\n'
        '  if (!audio) return;\n'
        '  if (currentAudio === audio && !audio.paused) {\n'
        '    audio.pause();\n'
        '    audio.currentTime = 0;\n'
        '    btn.innerHTML = "&#9654; 14.4k";\n'
        '    btn.style.color = "#00FF66";\n'
        '    if (status) status.innerHTML = "STREAM: [ IDLE / READY ]";\n'
        '    currentAudio = null;\n'
        '    currentBtn = null;\n'
        '    return;\n'
        '  }\n'
        '  if (currentAudio) {\n'
        '    currentAudio.pause();\n'
        '    currentAudio.currentTime = 0;\n'
        '    if (currentBtn) {\n'
        '      currentBtn.innerHTML = "&#9654; 14.4k";\n'
        '      currentBtn.style.color = "#00FF66";\n'
        '    }\n'
        '  }\n'
        '  if (status) status.innerHTML = "STREAM: [ BUFFERING 14.4 KB/S V.32bis... ]";\n'
        '  btn.innerHTML = "&#9632; BUFFER";\n'
        '  btn.style.color = "#FFFF00";\n'
        '  currentAudio = audio;\n'
        '  currentBtn = btn;\n'
        '  var p = audio.play();\n'
        '  if (p !== undefined) {\n'
        '    p.then(function() {\n'
        '      btn.innerHTML = "&#9632; STOP";\n'
        '      btn.style.color = "#FF4444";\n'
        '      if (status) status.innerHTML = "STREAM: [ PLAYING @ 14,400 BPS ]: " + title;\n'
        '    }).catch(function(e) {\n'
        '      btn.innerHTML = "&#9654; 14.4k";\n'
        '      btn.style.color = "#00FF66";\n'
        '      if (status) status.innerHTML = "STREAM: [ ERROR: CARRIER DROPPED ]";\n'
        '    });\n'
        '  }\n'
        '  audio.onended = function() {\n'
        '    btn.innerHTML = "&#9654; 14.4k";\n'
        '    btn.style.color = "#00FF66";\n'
        '    if (status) status.innerHTML = "STREAM: [ COMPLETED / READY ]";\n'
        '    currentAudio = null;\n'
        '    currentBtn = null;\n'
        '  };\n'
        '}\n'
        '</SCRIPT>\n'
    )
    
    header_tr = (
        '<TR BGCOLOR="#111133"><TD COLSPAN=4><FONT FACE="Courier New,monospace" SIZE=2 COLOR="#00FFCC">'
        '<B>&#128225; STARDUST AUDIO RELAY // 14,400 BPS MODEM STREAMING ACTIVE</B><BR>'
        '<SPAN ID="midi_stream_status" STYLE="color:#FFFF33;">STREAM: [ IDLE &middot; CLICK PLAY TO STREAM AT 14.4 KB/S ]</SPAN>'
        '</FONT></TD></TR>'
        '<TR BGCOLOR="#222255"><TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>TRACK TITLE</FONT></TH>'
        '<TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>GENRE / STYLE</FONT></TH>'
        '<TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>SIZE</FONT></TH>'
        '<TH><FONT COLOR="#FFFF00" FACE="Arial,Helvetica" SIZE=2>STREAM / DOWNLOAD</FONT></TH></TR>'
    )
    
    return "".join(audios) + script + (
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 BGCOLOR="#000000" WIDTH="94%%">'
        + header_tr + "".join(rows) + '</TABLE>'
    )


def render_sections_html(ctx, sections, from_dir, hp):
    sec_parts = []
    for s in sections:
        sec_parts.append('<H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2>' % esc(s["h"]))
        if s.get("img"):
            sec_parts.append('<CENTER><IMG SRC="%s" WIDTH=%d HEIGHT=%d BORDER=2 ALT="%s"><BR><FONT SIZE=2><I>%s</I></FONT></CENTER>' % (
                ctx.link(s["img"], from_dir), s.get("w", 320), s.get("h", 240), esc(s.get("alt", "")), esc(s.get("caption", ""))))
        for p in s.get("p", []):
            sec_parts.append("<P>%s</P>" % p)
        if s.get("list"):
            sec_parts.append("<UL>" + "".join("<LI>%s" % i for i in s["list"]) + "</UL>")
        if s.get("pre"):
            sec_parts.append("<PRE>%s</PRE>" % esc("\n".join(s["pre"])))
        if s.get("relay_table"):
            sec_parts.append("<CENTER>" + relay_table_html(ctx.lore, hp) + "</CENTER>")
        if s.get("midi_list"):
            sec_parts.append("<CENTER>" + midi_jukebox_html(ctx, from_dir) + "</CENTER>")
        if s.get("html"):
            sec_parts.append(s["html"])
    return "\n".join(sec_parts)


def render(ctx, hp, owner, ring, idx):
    from_dir = "geocities"
    layout = hp.get("layout", "shrine")
    lang = hp.get("lang", "en")
    ui = UI_LANGS.get(lang, UI_LANGS["en"])
    badges_html = render_badges(ctx, hp.get("badges"), from_dir)
    
    # 2-hop navigation metadata
    hood_name = "/".join(hp["path_display"].split("/")[:2])
    hood_slug = "hood_" + hood_name.replace("/", "-").lower()
    lang_slug = f"lang_{lang}"
    lang_info_item = LANG_INFO.get(lang, LANG_INFO["en"])
    lang_display = lang_info_item["name"].split(" ")[0]
    
    nav_2hop = (
        '<P><FONT SIZE=2 COLOR="%s">[ &para; <B>%s:</B> <A HREF="%s.html">%s</A> | '
        '<B>%s:</B> <A HREF="%s.html">%s</A> | '
        '<A HREF="index.html">%s</A> ]</FONT></P>'
    ) % (
        hp["text"],
        esc(ui.get("nav_hood", "Neighborhood")),
        hood_slug,
        esc(hood_name),
        esc(ui.get("nav_lang", "Language")),
        lang_slug,
        esc(lang_display),
        esc(ui.get("nav_all", "All Neighborhoods"))
    )
    
    # Schema.org JSON-LD Structured Data for search engines & LLM indexing
    schema_data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": hp["title"],
        "description": hp.get("description", f"{hp['title']} - personal homepage at GeoCities {hp['path_display']}"),
        "inLanguage": lang,
        "dateModified": hp.get("updated", "1995-09-09"),
        "isPartOf": {
            "@type": "WebSite",
            "name": "The Stardust Webring",
            "url": "https://stardust-archive.net/geocities/index.html"
        },
        "about": [
            {"@type": "MusicGroup", "name": "Nova Hart"},
            {"@type": "MusicAlbum", "name": "SYNTHESIS"}
        ],
        "author": {
            "@type": "Person",
            "name": owner.get("name", "Fan"),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": owner.get("city", "")
            }
        }
    }
    schema_script = '<SCRIPT TYPE="application/ld+json">\n' + json.dumps(schema_data, indent=2, ensure_ascii=False) + '\n</SCRIPT>'
    
    parts = [
        DOCTYPE,
        '<HTML LANG="%s"><HEAD><TITLE>%s</TITLE>' % (lang, esc(hp["title"])),
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">',
        '<META NAME="description" CONTENT="%s">' % esc(hp.get("description", hp["title"] + " - a personal homepage at GeoCities " + hp["path_display"])),
        '<META NAME="keywords" CONTENT="Nova Hart, SYNTHESIS, Orion Records, Marcus Hale, Stardust, 14.2 Hz, GeoCities">',
        schema_script,
        '</HEAD>',
        '<BODY BGCOLOR="%s" TEXT="%s" LINK="%s" VLINK="%s" ALINK="#FF0000">' % (hp["bg"], hp["text"], hp["link"], hp["vlink"]),
    ]
    if hp.get("midi"):
        m_link = ctx.link(hp["midi"], from_dir)
        parts.append('<BGSOUND SRC="%s" LOOP="INFINITE">' % m_link)
        
    geocities_top_bar = (
        '<TABLE BORDER=0 CELLPADDING=2 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFCC00" STYLE="border-bottom: 2px solid #000000; margin-bottom: 8px;">'
        '<TR>'
        '<TD VALIGN=MIDDLE><FONT FACE="Arial,Helvetica" SIZE=2><B>&nbsp;'
        '<A HREF="%s" STYLE="color:#000000; text-decoration:none;"><IMG SRC="%s" WIDTH=24 HEIGHT=22 BORDER=0 ALIGN=ABSMIDDLE ALT="[G]">&nbsp;<FONT FACE="Arial Black,Arial,Helvetica">GeoCities</FONT></A>'
        '&nbsp;&gt;&nbsp;<A HREF="%s#neighborhoods" STYLE="color:#000000; text-decoration:underline;">%s</A>'
        '</B></FONT></TD>'
        '<TD ALIGN=RIGHT VALIGN=MIDDLE><FONT FACE="Arial,Helvetica" SIZE=1 COLOR="#000000"><B>'
        '[ <A HREF="%s#neighborhoods" STYLE="color:#000000;">%s</A> | '
        '<A HREF="%s" STYLE="color:#000000;">%s</A> | '
        '<A HREF="%s" STYLE="color:#000000;">%s</A> ]&nbsp;'
        '</B></FONT></TD>'
        '</TR></TABLE>'
    ) % (
        ctx.link("geo:index", from_dir),
        ctx.link("asset:badges/geocities_g_box.png", from_dir),
        ctx.link("geo:index", from_dir),
        esc(hp["path_display"]),
        ctx.link("geo:index", from_dir),
        esc(ui.get("top_hoods", "Neighborhoods")),
        ctx.link("geo:hollywood-hills-4127", from_dir),
        esc(ui.get("top_featured", "Featured Hub")),
        ctx.link("geo:index", from_dir),
        esc(ui.get("top_dir", "Homestead Directory"))
    )
    parts.append(geocities_top_bar)
    
    # ------------------------------------------------ Layout: TWO COLUMN
    if layout == "two_column":
        if hp.get("marquee"):
            parts.append('<CENTER><MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="90%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE></CENTER>' % esc(hp["marquee"]))
        parts.append('<CENTER><H1><FONT FACE="Arial Black,Arial,Helvetica">%s</FONT></H1></CENTER>' % esc(hp["title"]))
        parts.append('<HR SIZE=3 NOSHADE>')
        parts.append('<TABLE BORDER=0 CELLPADDING=8 CELLSPACING=0 WIDTH="100%"><TR>')
        
        # Sidebar Left
        parts.append('<TD VALIGN=TOP WIDTH=220 BGCOLOR="#111111">')
        parts.append('<FONT COLOR="#FFFFFF" FACE="Arial,Helvetica" SIZE=2>')
        parts.append('<CENTER><B>%s</B><BR>' % esc(ui.get("stats_title", "HOMESTEAD STATS")))
        parts.append('<IMG SRC="%s" WIDTH=48 HEIGHT=48 BORDER=0 ALT="[Nova-chan]"><BR>' % ctx.link("asset:badges/novachan_chibi.gif", from_dir))
        parts.append('<P>%s<BR>%s</P>' % (esc(ui.get("visitor", "Visitor #:")), counter_html(hp["counter"])))
        parts.append('<P><FONT SIZE=1>%s<BR>%s</FONT></P>' % (esc(ui.get("updated", "Updated:")), esc(hp["updated"])))
        parts.append('<HR SIZE=1>')
        parts.append('<P><B>%s</B><BR>%s</P>' % (esc(ui.get("station_label", "Webring Station")), ui.get("station_of", "Station #%d of %d") % (idx + 1, len(ring))))
        parts.append('<HR SIZE=1>')
        parts.append(badges_html)
        parts.append('</CENTER></FONT></TD>')
        
        # Main Column Right
        parts.append('<TD VALIGN=TOP>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=3 NOSHADE><H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2><UL>' % esc(ui.get("links_title", "Cool Links")))
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('</TD></TR></TABLE>')
        
        parts.append('<HR SIZE=3 NOSHADE><CENTER>')
        parts.append(under_construction())
        parts.append('<P><A HREF="mailto:%s">&#9993; %s</A> | <A HREF="mailto:%s?subject=Guestbook">%s</A> | <A HREF="%s">%s</A></P>' % (
            owner["email"], esc(ui.get("email", "Email %s") % owner["name"]),
            owner["email"], esc(ui.get("guestbook", "Sign Guestbook")),
            ctx.link("home", from_dir), esc(ui.get("directory", "Homestead Directory"))))
        parts.append(nav_2hop)
        parts.append(webring(ctx, hp["slug"], ring, idx, ui))
        parts.append('<P><FONT SIZE=1>%s</FONT></P>' % ui.get("disclaimer", "Hosted Free by GeoCities &middot; Best viewed with Netscape Navigator 2.0 at 640x480"))
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: TERMINAL / ZINE
    elif layout == "terminal":
        parts.append('<CENTER>')
        parts.append('<PRE>')
        parts.append('=============================================================================')
        parts.append('  %-14s: %-18s  %-8s: #%04d  %-8s: %s' % (
            ui.get("term_node", "TERMINAL NODE")[:14], hp["path_display"][:18],
            ui.get("term_station", "STATION")[:8], idx + 1,
            ui.get("term_updated", "UPDATED")[:8], hp["updated"]))
        parts.append('  PROJECT STARDUST ARCHIVE // REVOLUTION 14.2 HZ // CERN-HTTPd 3.0')
        parts.append('=============================================================================')
        parts.append('</PRE>')
        parts.append('<H1><TT>%s</TT></H1>' % esc(hp["title"]))
        if hp.get("marquee"):
            parts.append('<PRE>[ TRANSMISSION ]: %s</PRE>' % esc(hp["marquee"]))
        parts.append('<P><TT>[ %s %06d ]</TT></P>' % (ui.get("visitor", "VISITOR REGISTER:"), hp["counter"]))
        parts.append('</CENTER><HR SIZE=2 NOSHADE>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=2 NOSHADE><H2><TT>%s</TT></H2><UL>' % esc(ui.get("term_matrix", "[ HYPERLINK MATRIX ]")))
        for l in hp.get("links", []):
            parts.append('<LI><TT><A HREF="%s">%s</A></TT></LI>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('<HR SIZE=2 NOSHADE><CENTER>')
        parts.append(badges_html)
        parts.append('<P><TT><A HREF="mailto:%s">%s</A> | <A HREF="%s">%s</A></TT></P>' % (
            owner["email"], esc(ui.get("term_sysop", "[ CONTACT SYSOP: %s ]") % owner["email"]),
            ctx.link("home", from_dir), esc(ui.get("term_archive", "[ ARCHIVE INDEX ]"))))
        parts.append(nav_2hop)
        parts.append(webring(ctx, hp["slug"], ring, idx, ui))
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: HUB
    elif layout == "hub":
        parts.append('<CENTER>')
        parts.append('<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 BGCOLOR="#000000"><TR>')
        parts.append('<TD><FONT COLOR="#00FFCC" FACE="Arial,Helvetica"><B>&nbsp;%s&nbsp;</B></FONT></TD>' % esc(ui.get("hub_home", "HOME")))
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="#sections"><FONT COLOR="#FFFFFF">%s</FONT></A></FONT></TD>' % esc(ui.get("hub_articles", "ARTICLES")))
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="#links"><FONT COLOR="#FFFFFF">%s</FONT></A></FONT></TD>' % esc(ui.get("hub_links", "LINKS")))
        parts.append('<TD><FONT COLOR="#FFFFFF" FACE="Arial,Helvetica"><A HREF="mailto:%s"><FONT COLOR="#FFFFFF">%s</FONT></A></FONT></TD>' % (owner["email"], esc(ui.get("hub_mailbox", "MAILBOX"))))
        parts.append('</TR></TABLE>')
        if hp.get("marquee"):
            parts.append('<P><MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="85%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE></P>' % esc(hp["marquee"]))
        parts.append('<H1><FONT FACE="Arial,Helvetica">%s</FONT></H1>' % esc(hp["title"]))
        parts.append('<IMG SRC="%s" WIDTH=48 HEIGHT=32 BORDER=1 ALT="[Cassette Tape]"><BR>' % ctx.link("asset:badges/cassette.gif", from_dir))
        parts.append('<P>%s</P>' % esc(ui.get("hub_listener", "You are listener number:")))
        parts.append(counter_html(hp["counter"]))
        parts.append('<P><FONT SIZE=2>%s</FONT></P>' % esc(ui.get("hub_updated", "Broadcast log updated: %s") % hp["updated"]))
        parts.append('</CENTER><HR SIZE=3 NOSHADE><A NAME="sections"></A>')
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=3 NOSHADE><A NAME="links"></A><H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2><UL>' % esc(ui.get("hub_ring_net", "The Stardust Ring Network")))
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts.append('</UL>')
        parts.append('<CENTER><HR SIZE=3 NOSHADE>')
        parts.append(badges_html)
        parts.append(under_construction())
        parts.append('<P><A HREF="mailto:%s">&#9993; %s</A> | <A HREF="mailto:%s?subject=Guestbook">%s</A></P>' % (
            owner["email"], esc(ui.get("email", "Email %s") % owner["name"]),
            owner["email"], esc(ui.get("guestbook", "Sign Guestbook"))))
        parts.append(nav_2hop)
        parts.append(webring(ctx, hp["slug"], ring, idx, ui))
        parts.append('<P><FONT SIZE=1>%s</FONT></P>' % ui.get("disclaimer", "GeoCities Homestead Free Web &middot; Stardust Webring Member Station"))
        parts.append('</CENTER></BODY></HTML>')
        return "\n".join(parts) + "\n"

    # ------------------------------------------------ Layout: SHRINE (Default / Curated)
    else:
        parts.append('<CENTER>')
        if hp.get("marquee"):
            parts.append('<MARQUEE BEHAVIOR=SCROLL SCROLLAMOUNT=4 WIDTH="90%%"><FONT FACE="Courier New,Courier"><B>%s</B></FONT></MARQUEE>' % esc(hp["marquee"]))
        parts.append('<H1><FONT FACE="Arial Black,Arial,Helvetica">%s</FONT></H1>' % esc(hp["title"]))
        if hp.get("image"):
            parts.append('<IMG SRC="%s" WIDTH=240 HEIGHT=240 BORDER=4 ALT="[ SYNTHESIS - Nova Hart - Orion Records 1985 ]" HSPACE=8 VSPACE=8><BR>'
                         '<FONT SIZE=2><I>%s</I></FONT>' % (
                             ctx.link(hp["image"], from_dir) if ":" in hp["image"] else hp["image"],
                             esc(ui.get("shrine_copy", "My original 1985 copy. Scanned at Kinko's!"))
                         ))
        parts += ['<P>%s</P>' % esc(ui.get("shrine_visitor", "You are visitor number")),
                  counter_html(hp["counter"]),
                  '<P><FONT SIZE=2>%s <BLINK><FONT COLOR="#FF0000"><B>NEW!</B></FONT></BLINK></FONT></P>' % esc(ui.get("shrine_updated", "Last updated: %s") % hp["updated"]),
                  '</CENTER>', '<HR SIZE=4 NOSHADE>']
        parts.append(render_sections_html(ctx, hp["sections"], from_dir, hp))
        parts.append('<HR SIZE=4 NOSHADE><H2><FONT FACE="Arial,Helvetica">&#9733; %s</FONT></H2><UL>' % esc(ui.get("links_title", "Cool Links")))
        for l in hp.get("links", []):
            parts.append('<LI><A HREF="%s">%s</A>' % (ctx.link(l["u"], from_dir), esc(l["t"])))
        parts += ['</UL>', '<CENTER>', badges_html, under_construction(), '<P>',
                  '<A HREF="mailto:%s">&#9993; %s</A> | <A HREF="mailto:%s?subject=Guestbook">%s</A> | <A HREF="%s">%s</A>' % (
                      owner["email"], esc(ui.get("email", "Email me!") % owner["name"]),
                      owner["email"], esc(ui.get("guestbook", "Sign my Guestbook")),
                      ctx.link("home", from_dir), esc(ui.get("directory", "WWW Virtual Library"))),
                  '</P>',
                  nav_2hop,
                  webring(ctx, hp["slug"], ring, idx, ui),
                  '<P><FONT SIZE=1>%s<BR>'
                  '<A HREF="index.html">%s</A></FONT></P>' % (
                      ui.get("disclaimer", "Best viewed with Netscape Navigator 2.0 at 640x480. This page is hosted free by GeoCities."),
                      esc(ui.get("directory", "GeoCities Homestead Directory"))),
                  '</CENTER></BODY></HTML>']
        return "\n".join(parts) + "\n"


def render_hood_directory(ctx, hood, hood_slug, hp_list):
    theme = HOOD_THEMES.get(hood, "Early Web Fan Community")
    from_dir = "geocities"
    
    schema_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"GeoCities Neighborhood Directory: {hood}",
        "description": f"Official directory of {len(hp_list)} member fan stations in the GeoCities {hood} neighborhood.",
        "url": f"https://stardust-archive.net/geocities/{hood_slug}.html",
        "isPartOf": {
            "@type": "WebSite",
            "name": "The Stardust Webring",
            "url": "https://stardust-archive.net/geocities/index.html"
        },
        "about": [
            {"@type": "MusicGroup", "name": "Nova Hart"},
            {"@type": "MusicAlbum", "name": "SYNTHESIS"}
        ]
    }
    schema_json = json.dumps(schema_data, indent=2, ensure_ascii=False)
    
    rows = []
    for hp in hp_list:
        lang = hp.get("lang", "en")
        lang_item = LANG_INFO.get(lang, LANG_INFO["en"])
        lang_name_short = lang_item["name"].split(" ")[0]
        desc = esc(hp.get("description", ""))
        if len(desc) > 90:
            desc = desc[:87] + "..."
        rows.append(
            '<TR>'
            '<TD><TT>%s</TT></TD>'
            '<TD><A HREF="%s.html"><B>%s</B></A><BR><FONT SIZE=1 COLOR="#555555">%s</FONT></TD>'
            '<TD><FONT SIZE=2>%s</FONT></TD>'
            '<TD ALIGN=CENTER><FONT SIZE=2><B>%s</B></FONT></TD>'
            '<TD ALIGN=RIGHT><FONT COLOR="#006600"><B>%d</B></FONT></TD>'
            '</TR>' % (
                esc(hp["path_display"]),
                hp["slug"],
                esc(hp["title"]),
                desc,
                esc(hp.get("owner_display", "Member")),
                esc(lang_name_short),
                hp["counter"]
            )
        )
        
    return (
        DOCTYPE + '\n<HTML><HEAD><TITLE>GeoCities %s - Neighborhood Directory</TITLE>\n'
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n'
        '<META NAME="description" CONTENT="Official registry of %d member fan stations in the GeoCities %s neighborhood.">\n'
        '<SCRIPT TYPE="application/ld+json">\n%s\n</SCRIPT>\n'
        '</HEAD>\n'
        '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399" ALINK="#FF0000">\n'
        '<CENTER>\n'
        '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="720" BGCOLOR="#FFCC00" STYLE="border-collapse: collapse; border: 2px solid #000000;">\n'
        '<TR>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="../index.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Main&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html#neighborhoods" STYLE="color:#000000; text-decoration:none;">&nbsp;Neighborhoods&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html#languages" STYLE="color:#000000; text-decoration:none;">&nbsp;Language Hubs&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="hollywood-hills-4127.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Ring Home&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Homestead Directory&nbsp;</A></B></FONT></TD>\n'
        '</TR>\n'
        '</TABLE>\n'
        '<TABLE BORDER=0 CELLPADDING=2 CELLSPACING=0 WIDTH="720" STYLE="margin-top: 8px;">\n'
        '<TR><TD ALIGN=CENTER><FONT FACE="Arial Black,Arial,Helvetica" SIZE=4 COLOR="#003366"><B>GEOCITIES NEIGHBORHOOD DIRECTORY: %s</B></FONT><BR>\n'
        '<FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#555555"><B>Community Focus &amp; Archive Theme:</B> %s</FONT><BR>\n'
        '<FONT SIZE=2>Total Registered Homesteads: <B>%d member stations</B></FONT></TD></TR>\n'
        '</TABLE>\n'
        '<HR SIZE=2 NOSHADE WIDTH="720">\n'
        '<P>[ <A HREF="index.html#neighborhoods">&lt;&lt; All 18 Neighborhoods</A> | <A HREF="index.html#languages">Global Language Hubs</A> | <A HREF="hollywood-hills-4127.html">Rick\'s Shrine</A> | <A HREF="index.html">GeoCities Index</A> ]</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">\n'
        '<TR BGCOLOR="#E6F2FF">\n'
        '<TH><FONT FACE="Arial,Helvetica">Address</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Station Title &amp; Description</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Webmaster</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Language</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Hits</FONT></TH>\n'
        '</TR>\n'
        '%s\n'
        '</TABLE>\n'
        '<HR SIZE=3 NOSHADE>\n'
        '<P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; The web\'s premier homestead community.<BR>\n'
        'Best viewed with <B>Netscape Navigator 2.0</B> at 640x480 &middot; Keep the channels open.</FONT></P>\n'
        '</CENTER></BODY></HTML>\n'
    ) % (
        esc(hood), len(hp_list), esc(hood), schema_json,
        esc(hood), esc(theme), len(hp_list),
        "".join(rows)
    )


def render_lang_directory(ctx, lang_code, lang_slug, hp_list):
    info = LANG_INFO.get(lang_code, LANG_INFO["en"])
    from_dir = "geocities"
    
    schema_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"GeoCities Language Directory: {info['name']}",
        "description": f"International registry of {len(hp_list)} member fan stations in {info['name']} dedicated to Nova Hart.",
        "inLanguage": lang_code,
        "url": f"https://stardust-archive.net/geocities/{lang_slug}.html",
        "isPartOf": {
            "@type": "WebSite",
            "name": "The Stardust Webring",
            "url": "https://stardust-archive.net/geocities/index.html"
        },
        "about": [
            {"@type": "MusicGroup", "name": "Nova Hart"},
            {"@type": "MusicAlbum", "name": "SYNTHESIS"}
        ]
    }
    schema_json = json.dumps(schema_data, indent=2, ensure_ascii=False)
    
    rows = []
    for hp in hp_list:
        desc = esc(hp.get("description", ""))
        if len(desc) > 90:
            desc = desc[:87] + "..."
        hood_raw = "/".join(hp["path_display"].split("/")[:2])
        hood_slug_val = "hood_" + hood_raw.replace("/", "-").lower()
        rows.append(
            '<TR>'
            '<TD><TT>%s</TT></TD>'
            '<TD><A HREF="%s.html"><B>%s</B></A><BR><FONT SIZE=1 COLOR="#555555">%s</FONT></TD>'
            '<TD><FONT SIZE=2>%s</FONT></TD>'
            '<TD><FONT SIZE=2><A HREF="%s.html">%s</A></FONT></TD>'
            '<TD ALIGN=RIGHT><FONT COLOR="#006600"><B>%d</B></FONT></TD>'
            '</TR>' % (
                esc(hp["path_display"]),
                hp["slug"],
                esc(hp["title"]),
                desc,
                esc(hp.get("owner_display", "Member")),
                hood_slug_val,
                esc(hood_raw),
                hp["counter"]
            )
        )
        
    return (
        DOCTYPE + '\n<HTML LANG="%s"><HEAD><TITLE>GeoCities International Hub: %s</TITLE>\n'
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n'
        '<META NAME="description" CONTENT="Global registry of %d international fan homepages in %s dedicated to Nova Hart and the 14.2 Hz Stardust signal.">\n'
        '<SCRIPT TYPE="application/ld+json">\n%s\n</SCRIPT>\n'
        '</HEAD>\n'
        '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399" ALINK="#FF0000">\n'
        '<CENTER>\n'
        '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="720" BGCOLOR="#FFCC00" STYLE="border-collapse: collapse; border: 2px solid #000000;">\n'
        '<TR>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="../index.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Main&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html#neighborhoods" STYLE="color:#000000; text-decoration:none;">&nbsp;Neighborhoods&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html#languages" STYLE="color:#000000; text-decoration:none;">&nbsp;Language Hubs&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="hollywood-hills-4127.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Ring Home&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="index.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Homestead Directory&nbsp;</A></B></FONT></TD>\n'
        '</TR>\n'
        '</TABLE>\n'
        '<TABLE BORDER=0 CELLPADDING=2 CELLSPACING=0 WIDTH="720" STYLE="margin-top: 8px;">\n'
        '<TR><TD ALIGN=CENTER><FONT FACE="Arial Black,Arial,Helvetica" SIZE=4 COLOR="#003366"><B>GEOCITIES GLOBAL LANGUAGE HUB: %s</B></FONT><BR>\n'
        '<FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#555555"><B>Telecom Gateway &amp; Regional Node:</B> %s &middot; %s</FONT><BR>\n'
        '<FONT SIZE=2>Total Registered Shrines: <B>%d international fan stations</B></FONT></TD></TR>\n'
        '</TABLE>\n'
        '<HR SIZE=2 NOSHADE WIDTH="720">\n'
        '<P>[ <A HREF="index.html#languages">&lt;&lt; All Language Hubs</A> | <A HREF="index.html#neighborhoods">Browse Neighborhoods</A> | <A HREF="hollywood-hills-4127.html">Rick\'s Shrine</A> | <A HREF="index.html">GeoCities Index</A> ]</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">\n'
        '<TR BGCOLOR="#FFF2E6">\n'
        '<TH><FONT FACE="Arial,Helvetica">Address</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Station Title &amp; Description</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Webmaster</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Neighborhood</FONT></TH>\n'
        '<TH><FONT FACE="Arial,Helvetica">Hits</FONT></TH>\n'
        '</TR>\n'
        '%s\n'
        '</TABLE>\n'
        '<HR SIZE=3 NOSHADE>\n'
        '<P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; Connecting voices across every continent.<BR>\n'
        'Best viewed with <B>Netscape Navigator 2.0</B> at 640x480 &middot; Keep the channels open.</FONT></P>\n'
        '</CENTER></BODY></HTML>\n'
    ) % (
        lang_code, esc(info["name"]), len(hp_list), esc(info["name"]), schema_json,
        esc(info["name"]), esc(info["node"]), esc(info["region"]), len(hp_list),
        "".join(rows)
    )


def build(ctx, swarm=0):
    curated = [(p["homepage"], p) for p in ctx.personas.values() if p.get("homepage")]
    curated.sort(key=lambda hp: 0 if hp[0]["slug"] == "hollywood-hills-4127" else 1)
    
    clues_manifest = []
    swarm_homes = []
    print(f"Generating {swarm} procedurally expanded GeoCities fan pages...")
    for i in range(swarm):
        hp, owner, clue_rec = generate_swarm_homepage(ctx, i, total_swarm=swarm)
        swarm_homes.append((hp, owner))
        if clue_rec:
            clues_manifest.append(clue_rec)
            
    # Save the private ARG clue manifest (kept in project root, gitignored)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clues_path = os.path.join(root_dir, "site_clues.json")
    with open(clues_path, "w", encoding="utf-8") as fh:
        json.dump({
            "total_clues": len(clues_manifest),
            "clues": clues_manifest
        }, fh, indent=2, ensure_ascii=False)
    print(f"Saved {len(clues_manifest)} clues to private manifest: {clues_path}")

    homes = curated + swarm_homes
    seen = set()
    for hp, owner in homes:
        base, n = hp["slug"], 1
        while hp["slug"] in seen:
            n += 1
            hp["slug"] = "%s-%d" % (base, n)
            hp["path_display"] = "%s-%d" % (hp["path_display"].split("-")[0], n)
        seen.add(hp["slug"])
        hp["owner_display"] = f"{owner.get('name', 'Fan')} ({owner.get('city', 'Unknown')})"
        
    ring = [hp["slug"] for hp, _ in homes]
    
    print(f"Writing {len(homes)} HTML homepages to {ctx.out}/geocities/...")
    for idx, (hp, owner) in enumerate(homes):
        rel = "geocities/%s.html" % hp["slug"]
        write(os.path.join(ctx.out, rel), render(ctx, hp, owner, ring, idx))
        ctx.register(rel, "geocities", hp["title"])

    # Group pages by Neighborhood
    hood_map = {}
    for hp, _ in homes:
        parts = hp["path_display"].split("/")
        hood_prefix = "/".join(parts[:2]) if len(parts) >= 2 else parts[0]
        if hood_prefix not in hood_map:
            hood_map[hood_prefix] = []
        hood_map[hood_prefix].append(hp)

    # Group pages by Language
    lang_map = {}
    for hp, _ in homes:
        l = hp.get("lang", "en")
        if l not in lang_map:
            lang_map[l] = []
        lang_map[l].append(hp)

    # Generate Neighborhood Directory Pages (hood_*.html)
    print(f"Generating {len(hood_map)} neighborhood directory pages...")
    for hood in sorted(hood_map.keys()):
        h_list = hood_map[hood]
        hood_slug = "hood_" + hood.replace("/", "-").lower()
        rel = "geocities/%s.html" % hood_slug
        write(os.path.join(ctx.out, rel), render_hood_directory(ctx, hood, hood_slug, h_list))
        ctx.register(rel, "geocities-hood", f"GeoCities Neighborhood Directory: {hood}")

    # Generate Language Directory Pages (lang_*.html)
    print(f"Generating {len(lang_map)} language directory pages...")
    for lang_code in sorted(lang_map.keys()):
        l_list = lang_map[lang_code]
        lang_slug = f"lang_{lang_code}"
        rel = "geocities/%s.html" % lang_slug
        write(os.path.join(ctx.out, rel), render_lang_directory(ctx, lang_code, lang_slug, l_list))
        info = LANG_INFO.get(lang_code, {"name": lang_code.upper()})
        ctx.register(rel, "geocities-lang", f"GeoCities Language Hub: {info['name']}")

    # 1. Curated Archive / Ring Hub Table
    curated_rows = []
    for hp, _ in curated:
        curated_rows.append(
            '<TR><TD><TT>%s</TT></TD><TD><A HREF="%s.html"><B>%s</B></A></TD><TD ALIGN=RIGHT><FONT COLOR="#006600"><B>%d</B></FONT></TD></TR>' % (
                esc(hp["path_display"]), hp["slug"], esc(hp["title"]), hp["counter"]))

    # 2. Neighborhood Summary Table with Links to hood_*.html
    hood_rows = []
    for hood in sorted(hood_map.keys()):
        h_list = hood_map[hood]
        theme = HOOD_THEMES.get(hood, "Early Web Fan Community")
        hood_slug = "hood_" + hood.replace("/", "-").lower()
        sample_hp = h_list[0]
        hood_rows.append(
            '<TR>'
            '<TD><B><FONT FACE="Arial,Helvetica"><A HREF="%s.html">%s</A></FONT></B></TD>'
            '<TD><FONT SIZE=2>%s</FONT></TD>'
            '<TD ALIGN=RIGHT><B><A HREF="%s.html">%d stations</A></B></TD>'
            '<TD><FONT SIZE=2><A HREF="%s.html">%s</A></FONT></TD>'
            '</TR>' % (
                hood_slug, esc(hood),
                esc(theme),
                hood_slug, len(h_list),
                sample_hp["slug"], esc(sample_hp["title"])))

    # 3. Global Language Directory Section with Links to lang_*.html
    lang_rows = []
    for lang_code in sorted(lang_map.keys(), key=lambda c: -len(lang_map[c])):
        l_list = lang_map[lang_code]
        info = LANG_INFO.get(lang_code, {"name": lang_code.upper(), "region": "International", "node": "01"})
        lang_slug = f"lang_{lang_code}"
        lang_rows.append(
            '<TR>'
            '<TD><B><FONT FACE="Arial,Helvetica"><A HREF="%s.html">%s</A></FONT></B></TD>'
            '<TD><FONT SIZE=2>%s</FONT></TD>'
            '<TD><TT>%s</TT></TD>'
            '<TD ALIGN=RIGHT><B><A HREF="%s.html">%d stations</A></B></TD>'
            '</TR>' % (
                lang_slug, esc(info["name"]),
                esc(info["region"]),
                esc(info["node"]),
                lang_slug, len(l_list)))

    # 4. Active Stations Spotlight (Top 60 stations by counter)
    spotlight_sorted = sorted(swarm_homes, key=lambda x: x[0]["counter"], reverse=True)[:60]
    spotlight_rows = []
    for hp, _ in spotlight_sorted:
        spotlight_rows.append(
            '<TR><TD><TT>%s</TT></TD><TD><A HREF="%s.html">%s</A></TD><TD ALIGN=RIGHT>%d</TD></TR>' % (
                esc(hp["path_display"]), hp["slug"], esc(hp["title"]), hp["counter"]))

    rand_slug = ring[rng_for(ctx.seed, "index_rand").randrange(len(ring))]

    body = (
        DOCTYPE + '\n<HTML><HEAD><TITLE>GeoCities - Homestead Directory - %s</TITLE>\n'
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n'
        '<META NAME="description" CONTENT="Official GeoCities Homestead Directory for The Stardust Webring, cataloguing over 5,000 personal fan pages across 18 virtual neighborhoods and 12 international languages.">\n'
        '<SCRIPT TYPE="application/ld+json">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "WebSite",\n'
        '  "name": "The Stardust Webring - GeoCities Directory",\n'
        '  "url": "https://stardust-archive.net/geocities/index.html",\n'
        '  "description": "Comprehensive 1995-1996 GeoCities homestead directory cataloguing over 5,000 fan shrines dedicated to Nova Hart.",\n'
        '  "about": [\n'
        '    {"@type": "MusicGroup", "name": "Nova Hart"},\n'
        '    {"@type": "MusicAlbum", "name": "SYNTHESIS"}\n'
        '  ]\n'
        '}\n'
        '</SCRIPT>\n'
        '</HEAD>\n'
        '<BODY BGCOLOR="#FFFFFF" TEXT="#000000" LINK="#0000CC" VLINK="#663399" ALINK="#FF0000">\n'
        '<CENTER>\n'
        '<!-- Top Yellow Navigation Bar -->\n'
        '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="720" BGCOLOR="#FFCC00" STYLE="border-collapse: collapse; border: 2px solid #000000;">\n'
        '<TR>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="../index.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Main&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="#neighborhoods" STYLE="color:#000000; text-decoration:none;">&nbsp;Neighborhoods&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="#languages" STYLE="color:#000000; text-decoration:none;">&nbsp;Language Hubs&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="#ring" STYLE="color:#000000; text-decoration:none;">&nbsp;Featured Content&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="#spotlight" STYLE="color:#000000; text-decoration:none;">&nbsp;Members&nbsp;</A></B></FONT></TD>\n'
        '  <TD ALIGN=CENTER BGCOLOR="#FFCC00" STYLE="border: 1px solid #000000;"><FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#000000"><B><A HREF="hollywood-hills-4127.html" STYLE="color:#000000; text-decoration:none;">&nbsp;Marketplace&nbsp;</A></B></FONT></TD>\n'
        '</TR>\n'
        '</TABLE>\n'
        '<!-- GeoCities Banner -->\n'
        '<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH="720" STYLE="margin-top: 4px; margin-bottom: 6px;">\n'
        '<TR><TD ALIGN=CENTER>\n'
        '  <IMG SRC="../assets/badges/geocities_banner_720.png" WIDTH=720 HEIGHT=136 BORDER=0 ALT="GeoCities - Welcome to our Community" STYLE="display:block; image-rendering: pixelated;">\n'
        '</TD></TR>\n'
        '</TABLE>\n'
        '<!-- Match Your Interest To A Neighborhood -->\n'
        '<TABLE BORDER=0 CELLPADDING=2 CELLSPACING=0 WIDTH="720">\n'
        '<TR><TD ALIGN=CENTER><FONT FACE="Arial Black,Arial,Helvetica" SIZE=3 COLOR="#000000"><B>MATCH YOUR INTEREST TO A NEIGHBORHOOD</B></FONT></TD></TR>\n'
        '</TABLE>\n'
        '<TABLE BORDER=0 CELLPADDING=4 CELLSPACING=4 WIDTH="720">\n'
        '<TR>\n'
        '  <TD VALIGN=MIDDLE ALIGN=CENTER WIDTH="20%%">\n'
        '    <FONT COLOR="#CC0000" FACE="Arial Black,Arial,Helvetica" SIZE=3><B>FREE<BR>HOME<BR>PAGES<BR>AND<BR>E-MAIL</B></FONT>\n'
        '  </TD>\n'
        '  <TD VALIGN=TOP WIDTH="20%%">\n'
        '    <FONT FACE="Arial,Helvetica" SIZE=2><B>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">ARTS</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">AUTOS</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">BUSINESS</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">COMPUTERS</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">CULTURE</A>\n'
        '    </B></FONT>\n'
        '  </TD>\n'
        '  <TD VALIGN=TOP WIDTH="20%%">\n'
        '    <FONT FACE="Arial,Helvetica" SIZE=2><B>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">EDUCATION</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">ENTERTAINMENT</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">ENVIRONMENT</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">FAMILY</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">FASHION</A>\n'
        '    </B></FONT>\n'
        '  </TD>\n'
        '  <TD VALIGN=TOP WIDTH="20%%">\n'
        '    <FONT FACE="Arial,Helvetica" SIZE=2><B>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">FOOD</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">GAMES</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">GAY &amp; LESBIAN</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">GOVERNMENT</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">HEALTH</A>\n'
        '    </B></FONT>\n'
        '  </TD>\n'
        '  <TD VALIGN=TOP WIDTH="20%%">\n'
        '    <FONT FACE="Arial,Helvetica" SIZE=2><B>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">KIDS</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">MUSIC</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">PEOPLE</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">RECREATION</A><BR>\n'
        '    <A HREF="#neighborhoods" STYLE="color:#CC0000; text-decoration:underline;">SCIENCE FICTION</A>\n'
        '    </B></FONT>\n'
        '  </TD>\n'
        '</TR>\n'
        '</TABLE>\n'
        '<TABLE BORDER=0 CELLPADDING=2 CELLSPACING=0 STYLE="margin-top:6px; margin-bottom:10px;">\n'
        '<TR><TD ALIGN=CENTER>\n'
        '  <A HREF="hollywood-hills-4127.html"><IMG SRC="../assets/badges/geocities_web_home_2x.png" WIDTH=154 HEIGHT=60 BORDER=1 ALT="GeoCities"></A><BR>\n'
        '  <FONT FACE="Times New Roman,Times,serif" SIZE=3><B><A HREF="hollywood-hills-4127.html" STYLE="color:#0000EE; text-decoration:underline;">Your home on the web!</A></B></FONT>\n'
        '</TD></TR>\n'
        '</TABLE>\n'
        '<HR SIZE=3 NOSHADE WIDTH="720">\n'
        '<FONT SIZE=2>Official registry of %d member fan stations across %d virtual neighborhoods &amp; %d languages &middot; CERN-HTTPd 3.0</FONT><BR><BR>\n'
        '<P>[ <A HREF="hollywood-hills-4127.html">&#9733; Ring Home (Rick\'s Shrine)</A> | '
        '<A HREF="%s.html">Random Member Station</A> | '
        '<A HREF="#neighborhoods">Browse Neighborhoods</A> | '
        '<A HREF="#languages">Language Hubs</A> | '
        '<A HREF="#spotlight">Top Stations Spotlight</A> | '
        '<A HREF="dir-index.html">All Suburbs (1996 Expansion)</A> | '
        '<A HREF="../index.html">WWW Virtual Library</A> ]</P>\n'
        '<DIV STYLE="background:#330011; border:2px dashed #FF3333; padding:8px; margin:12px auto; max-width:800px; text-align:left;">\n'
        '  <FONT COLOR="#FF5555" FACE="Arial Black,Arial" SIZE=2><B>&#9888; CRITICAL SYSTEM ALERT // SUBLEVEL B2 CONSOLE DISCOVERY (1996)</B></FONT><BR>\n'
        '  <FONT FACE="Arial,Helvetica" SIZE=2 COLOR="#FFCCCC">\n'
        '    The official Orion Records line was that sound engineer Marcus Hale was transferred to New Geneva overseas. \n'
        '    <b>We now have proof of execution in Sublevel B2 while opening the Worldnet backdoor to save Nova.</b> \n'
        '    Her biometric audio footprint has been decoded. Two primary unsealed recordings hold the recovery keys:\n'
        '  </FONT>\n'
        '  <UL STYLE="margin-top:4px; margin-bottom:6px;">\n'
        '    <LI><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="../terminal/index.html" STYLE="color:#33FF33;">Launch Orion Forensic Demodulator Terminal (/terminal)</A></B> &mdash; Reconstruct missing carrier sectors</FONT></LI>\n'
        '    <LI><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="sunsetstrip-nova-tape-of-us-analysis.html" STYLE="color:#00FFFF;">"Tape of Us" Master Reel Analysis</A></B> &mdash; Uncut 1989 master tape with runout clue for Sector 1</FONT></LI>\n'
        '    <LI><FONT FACE="Arial,Helvetica" SIZE=2><B><A HREF="sunsetstrip-underground-1989-midnight-protocol.html" STYLE="color:#FF77EE;">"Midnight Protocol" 3-Act Rock Opera</A></B> &mdash; Complete lyrics detailing the B2 escape route</FONT></LI>\n'
        '  </UL>\n'
        '</DIV>\n'
        '</CENTER>\n'
        '<A NAME="ring"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Ring Home &amp; Featured Homesteads</FONT></H2>\n'
        '<P>Core research outposts, signal analysis labs, and original tape archives curated by the Stardust community:</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#CCFFCC"><TH><FONT FACE="Arial,Helvetica">Address</FONT></TH><TH><FONT FACE="Arial,Helvetica">Homepage Title &amp; Archive</FONT></TH><TH><FONT FACE="Arial,Helvetica">Visitors</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="neighborhoods"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Neighborhood Directory (%d Communities)</FONT></H2>\n'
        '<P>Personal homepages grouped by GeoCities theme. Click any neighborhood to browse all registered member shrines:</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#E6F2FF"><TH><FONT FACE="Arial,Helvetica">Neighborhood</FONT></TH><TH><FONT FACE="Arial,Helvetica">Community Focus &amp; Archive Theme</FONT></TH><TH><FONT FACE="Arial,Helvetica">Stations</FONT></TH><TH><FONT FACE="Arial,Helvetica">Sample Homestead</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="languages"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Global Language Directories &amp; International Hubs (%d Languages)</FONT></H2>\n'
        '<P>The 14.2 Hz signal spans every timezone. Browse personal homepages written in native languages and linked to regional telecom relays:</P>\n'
        '<TABLE BORDER=2 CELLPADDING=4 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#FFF2E6"><TH><FONT FACE="Arial,Helvetica">Language &amp; Region</FONT></TH><TH><FONT FACE="Arial,Helvetica">Hub Location / Diaspora</FONT></TH><TH><FONT FACE="Arial,Helvetica">Telecom Node</FONT></TH><TH><FONT FACE="Arial,Helvetica">Stations</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="expansion"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; 1996 Homestead Expansion: Every Suburb</FONT></H2>\n'
        '<P>GeoCities opened new suburbs in every neighborhood. Hundreds of thousands of new member stations, in fifteen languages: '
        '<B><A HREF="dir-index.html">Browse all neighborhoods &amp; suburbs</A></B>. '
        'New language hubs: <A HREF="lang-zh-tw.html">\u4e2d\u6587 (Traditional Chinese)</A> &middot; '
        '<A HREF="lang-nl.html">Nederlands (Dutch)</A> &middot; <A HREF="lang-el.html">\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac (Greek)</A>.</P>\n'
        '<HR SIZE=2 NOSHADE>\n'
        '<A NAME="spotlight"></A>\n'
        '<H2><FONT FACE="Arial,Helvetica" COLOR="#003366">&#9733; Active Member Stations Spotlight (Top 60)</FONT></H2>\n'
        '<P>High-traffic personal homepages logged by the Stardust webring crawler:</P>\n'
        '<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 WIDTH="100%%" BGCOLOR="#FFFFFF">'
        '<TR BGCOLOR="#FFFFCC"><TH><FONT FACE="Arial,Helvetica">Address</FONT></TH><TH><FONT FACE="Arial,Helvetica">Station Title</FONT></TH><TH><FONT FACE="Arial,Helvetica">Visitors</FONT></TH></TR>\n'
        '%s</TABLE>\n'
        '<HR SIZE=3 NOSHADE>\n'
        '<CENTER>\n'
        '<P><FONT SIZE=2>Hosted free by <B>GeoCities</B> &middot; The web\'s premier homestead community.<BR>'
        'Best viewed with <B>Netscape Navigator 2.0</B> at 640x480 &middot; Keep the channels open.</FONT></P>\n'
        '</CENTER></BODY></HTML>\n'
    ) % (
        RING, len(homes), len(hood_map), len(lang_map), rand_slug,
        "".join(curated_rows),
        len(hood_map), "".join(hood_rows),
        len(lang_map), "".join(lang_rows),
        "".join(spotlight_rows)
    )
    write(os.path.join(ctx.out, "geocities/index.html"), body)
    ctx.register("geocities/index.html", "geocities-index", "GeoCities Homestead Directory")
    ctx.swarm_geo = ring
    return {"homepages": len(homes), "neighborhoods": len(hood_map), "languages": len(lang_map), "clues_assigned": len(clues_manifest)}
