"""좌표 사전, 이벤트, 키워드 카테고리 등 상수."""
from __future__ import annotations

# ============================================================
# 분석용 키워드 사전 (노트북과 동기화)
# ============================================================
KEYWORDS_KR = {
    "호르무즈 해협":         ["호르무즈 해협", "호르무즈"],
    "혁명수비대(IRGC)":      ["혁명수비대", "IRGC"],
    "시아 벨트":             ["시아 벨트", "시아벨트"],
    "테헤란 정권":           ["테헤란 정권", "테헤란"],
    "샤헤드 드론":           ["샤헤드 드론", "샤헤드"],
    "대리세력 네트워크":     ["대리세력", "프록시"],
    "핵협상(JCPOA)":         ["핵협상", "JCPOA"],
    "중동 저항축":           ["저항축", "Axis of Resistance"],
    "헤즈볼라 연계":         ["헤즈볼라"],
    "페르시아만 긴장":       ["페르시아만"],
    "제재 경제":             ["제재"],
    "비대칭 전력 전략":      ["비대칭 전력", "비대칭전"],
    "시아파 영향권":         ["시아파"],
    "솔레이마니 사망 사건":  ["솔레이마니"],
}

KEYWORDS_US = {
    "Strait of Hormuz":      ["Strait of Hormuz", "Hormuz"],
    "IRGC":                  ["IRGC", "Revolutionary Guard"],
    "Shia Belt":             ["Shia belt", "Shi'a belt", "Shia crescent"],
    "Tehran Regime":         ["Tehran regime", "Tehran"],
    "Shahed Drone":          ["Shahed drone", "Shahed"],
    "Proxy Network":         ["proxy network", "proxies", "proxy forces"],
    "JCPOA":                 ["JCPOA", "nuclear deal"],
    "Axis of Resistance":    ["Axis of Resistance"],
    "Hezbollah":             ["Hezbollah"],
    "Persian Gulf":          ["Persian Gulf"],
    "Sanctions":             ["sanctions"],
    "Asymmetric Warfare":    ["asymmetric warfare", "asymmetric"],
    "Shia Influence":        ["Shia influence", "Shiite", "Shia"],
    "Soleimani":             ["Soleimani"],
}

# ============================================================
# 중동 키워드 좌표 (지도 [중동] 뷰용)
# ============================================================
KEYWORD_COORDS = {
    # (lat, lon, category, label)
    "호르무즈 해협":        (26.57, 56.25, "conflict",  "Strait of Hormuz"),
    "혁명수비대(IRGC)":     (35.69, 51.42, "strategic", "Tehran (IRGC HQ)"),
    "테헤란 정권":           (35.70, 51.40, "strategic", "Tehran"),
    "샤헤드 드론":           (32.40, 53.70, "strategic", "Iran (Shahed)"),
    "헤즈볼라 연계":         (33.89, 35.51, "proxy",     "Beirut (Hezbollah)"),
    "페르시아만 긴장":       (27.00, 51.50, "conflict",  "Persian Gulf"),
    "솔레이마니 사망 사건":  (33.26, 44.23, "historical","Baghdad (Soleimani)"),
    "시아파 영향권":         (31.00, 47.00, "proxy",     "Shia Influence Zone"),
    "대리세력 네트워크":     (36.20, 37.13, "proxy",     "Proxy Network (Syria)"),
    "시아 벨트":             (34.00, 43.00, "proxy",     "Shia Belt"),
    "핵협상(JCPOA)":         (48.21, 16.37, "diplomacy", "Vienna (JCPOA)"),
    "제재 경제":             (35.69, 51.42, "strategic", "Tehran (Sanctions)"),
    "중동 저항축":           (35.00, 40.00, "proxy",     "Axis of Resistance"),
    "비대칭 전력 전략":      (32.00, 53.00, "strategic", "Iran (Asymmetric)"),
}

# 영문 키워드도 같은 좌표 매핑 (이름만 다름)
KEYWORD_COORDS_US = {
    "Strait of Hormuz":    KEYWORD_COORDS["호르무즈 해협"],
    "IRGC":                KEYWORD_COORDS["혁명수비대(IRGC)"],
    "Tehran Regime":       KEYWORD_COORDS["테헤란 정권"],
    "Shahed Drone":        KEYWORD_COORDS["샤헤드 드론"],
    "Hezbollah":           KEYWORD_COORDS["헤즈볼라 연계"],
    "Persian Gulf":        KEYWORD_COORDS["페르시아만 긴장"],
    "Soleimani":           KEYWORD_COORDS["솔레이마니 사망 사건"],
    "Shia Influence":      KEYWORD_COORDS["시아파 영향권"],
    "Proxy Network":       KEYWORD_COORDS["대리세력 네트워크"],
    "Shia Belt":           KEYWORD_COORDS["시아 벨트"],
    "JCPOA":               KEYWORD_COORDS["핵협상(JCPOA)"],
    "Sanctions":           KEYWORD_COORDS["제재 경제"],
    "Axis of Resistance":  KEYWORD_COORDS["중동 저항축"],
    "Asymmetric Warfare":  KEYWORD_COORDS["비대칭 전력 전략"],
}

# 카테고리별 색상 (worldmonitor 팔레트)
CATEGORY_COLORS = {
    "conflict":   "#ff4444",  # 빨강 — High alert
    "strategic":  "#ff8c00",  # 주황 — Elevated
    "proxy":      "#aa44ff",  # 보라 — Proxy
    "diplomacy":  "#00d4ff",  # 시안 — Diplomacy
    "historical": "#888888",  # 회색 — Historical
    "source_kr":  "#00ff88",  # 녹색 — KR news source
    "source_us":  "#ffdd00",  # 노랑 — US news source
}

# ============================================================
# 한국 매체 좌표 ([한국] 뷰용)
# ============================================================
# Seoul 중심으로 약간씩 분산
KR_SOURCE_COORDS = {
    "v.daum.net":      (33.5000, 126.5300),  # 제주 (Daum)
    "연합뉴스":         (37.5708, 126.9744),
    "YTN":             (37.5797, 126.8929),  # 상암
    "뉴시스":          (37.5645, 126.9785),
    "한겨레":          (37.5602, 126.9784),
    "뉴스1":           (37.5664, 126.9788),
    "조선일보":         (37.5697, 126.9799),
    "KBS 뉴스":        (37.5251, 126.9197),  # 여의도
    "경향신문":         (37.5586, 126.9777),
    "중앙일보":         (37.5760, 126.8884),  # 상암
    "MBC 뉴스":        (37.5797, 126.8929),
    "연합인포맥스":     (37.5640, 126.9744),
    "동아일보":         (37.5709, 126.9819),
    "연합뉴스TV":       (37.5708, 126.9744),
    "글로벌이코노믹":   (37.5650, 126.9786),
    "한국경제":         (37.5630, 126.9786),
    "채널A":           (37.5709, 126.9819),
    "JTBC":            (37.5760, 126.8884),
    "마켓인":          (37.5670, 126.9780),
    "문화일보":         (37.5660, 126.9784),
    "Chosunbiz":       (37.5697, 126.9799),
    "네이트":          (37.4012, 127.1086),  # 판교
    "머니투데이":       (37.5640, 126.9744),
    "전자신문":         (37.5670, 126.9760),
    "조선비즈":         (37.5697, 126.9799),
    "비즈워치":         (37.5640, 126.9744),
    "데일리안":         (37.5640, 126.9744),
    "이데일리":         (37.5640, 126.9760),
}

# ============================================================
# 미국 / 글로벌 매체 좌표 ([미국] / [글로벌] 뷰용)
# ============================================================
US_SOURCE_COORDS = {
    "Al Jazeera":           (25.3260,  51.5380),  # Doha
    "Reuters":              (51.5135,  -0.1064),  # London
    "The Jerusalem Post":   (31.7683,  35.2137),  # Jerusalem
    "The New York Times":   (40.7560, -73.9905),
    "The Times of Israel":  (31.7683,  35.2137),
    "MSN":                  (47.6396,-122.1281),  # Redmond, WA
    "Anadolu Ajansı":       (39.9255,  32.8378),  # Ankara
    "PBS":                  (38.8800, -77.1100),  # Arlington
    "BBC":                  (51.5180,  -0.1438),  # London
    "ایران اینترنشنال":     (51.5074,  -0.1278),  # London (Iran International)
    "The Hill":             (38.8951, -77.0364),  # DC
    "Fox News":             (40.7589, -73.9851),  # NYC
    "CNN":                  (33.7560, -84.3880),  # Atlanta
    "The Guardian":         (51.5364,  -0.1178),  # London
    "CNBC":                 (40.8857, -73.9495),  # NJ
    "Middle East Eye":      (51.5170,  -0.1232),
    "AP News":              (40.7561, -73.9870),
    "CBS News":             (40.7656, -73.9883),
    "France 24":            (48.8566,   2.3522),  # Paris
    "Bloomberg.com":        (40.7567, -73.9712),
    "WSJ":                  (40.7572, -73.9869),
    "ynetnews":             (32.0853,  34.7818),  # Tel Aviv
    "dw.com":               (52.5200,  13.4050),  # Berlin
    "WION":                 (28.5355,  77.3910),  # Noida, India
    "Politico":             (38.9072, -77.0369),
    "NPR":                  (38.9072, -77.0369),
    "Washington Post":      (38.9046, -77.0398),
    "Voice of America":     (38.8970, -77.0220),
    "Daily Mail":           (51.4933,  -0.1444),
    "ABC News":             (40.7589, -73.9851),
    "Times of India":       (19.0760,  72.8777),
    "South China Morning Post": (22.3193, 114.1694),
    "TRT World":            (41.0082,  28.9784),
    "Sky News":             (51.5040,  -0.4960),
    "The Telegraph":        (51.5121,  -0.1188),
    "Independent":          (51.5074,  -0.1278),
    "Newsweek":             (40.7589, -73.9851),
    "Yahoo News":           (37.4180,-122.0250),
    "USA TODAY":            (38.8800, -77.1100),
}

# ============================================================
# 줌 / 영역 사전 (지도 뷰)
# ============================================================
MAP_VIEWS = {
    "중동":   {"center_lat": 32.5, "center_lon": 47.0, "scope": "asia",  "lataxis": [10, 48], "lonaxis": [15, 70]},
    "한국":   {"center_lat": 36.0, "center_lon": 127.5, "scope": "asia", "lataxis": [33, 39], "lonaxis": [124, 131]},
    "미국":   {"center_lat": 39.0, "center_lon": -97.0, "scope": "north america", "lataxis": [24, 50], "lonaxis": [-125, -65]},
    "글로벌": {"center_lat": 30.0, "center_lon": 30.0, "scope": "world", "lataxis": [-10, 70], "lonaxis": [-130, 140]},
}

# ============================================================
# 이벤트 어노테이션 (시계열 차트에 마커로 표시)
# 분석 데이터에서 헤드라인 패턴 보고 사후적으로 잡은 시점들
# ============================================================
EVENT_ANNOTATIONS = [
    {"date": "2026-01-02", "title": "트럼프 이란 위협",
     "desc": "트럼프 \"이란이 시위대 살해 시 미국 개입\" 경고"},
    {"date": "2026-02-28", "title": "확전 신호 본격화",
     "desc": "Brent 유가 $70 돌파, 키워드 빈도 급증 시작"},
    {"date": "2026-03-05", "title": "ESCALATION 시작",
     "desc": "Brent $90 돌파, 미디어 보도량 폭증 (~3.8배)"},
    {"date": "2026-04-15", "title": "Brent 피크 $120",
     "desc": "유가 사상 최고치, 호르무즈 봉쇄 우려 정점"},
    {"date": "2026-05-04", "title": "종전 협상 시도",
     "desc": "이란 '30일 이내 종전' 제안, 미국 응답"},
]

# 국면 음영 (Phase shading)
PHASES = [
    {"start": "2026-01-01", "end": "2026-02-27", "label": "Calm",      "color": "rgba(0, 255, 136, 0.06)"},
    {"start": "2026-02-28", "end": "2026-03-31", "label": "Escalation", "color": "rgba(255, 68, 68, 0.10)"},
    {"start": "2026-04-01", "end": "2026-05-20", "label": "Sustained",  "color": "rgba(255, 140, 0, 0.07)"},
]

# ============================================================
# STATUS 등급 임계값 (Pearson |r|)
# ============================================================
def status_from_r(r: float) -> tuple[str, str]:
    """Pearson r 절대값으로 등급/색상 반환."""
    abs_r = abs(r) if r == r else 0  # NaN 처리
    if r != r:  # NaN
        return ("N/A", "#444444")
    if abs_r > 0.5:
        return ("CRIT", "#ff4444")
    if abs_r > 0.3:
        return ("HIGH", "#ff8c00")
    if abs_r > 0.1:
        return ("MED", "#ffdd00")
    return ("STABLE", "#00d4ff")
