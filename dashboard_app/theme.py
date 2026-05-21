"""worldmonitor 스타일 다크 테마 CSS — Pretendard 폰트."""

THEME_CSS = """
<style>
/* Pretendard 폰트 로드 (variable 버전 — 모든 weight 포함) */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css');

/* 전역 다크 + Pretendard */
.stApp {
    background-color: #0a0d14 !important;
    color: #e0e6ed !important;
    font-family: 'Pretendard Variable', 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* 메인 컨테이너 패딩 줄이기 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* 헤더/타이틀 */
h1, h2, h3, h4, h5, h6 {
    color: #e0e6ed !important;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif !important;
    letter-spacing: 0.5px;
}

/* 사이드바 (좌측 KEYWORDS) */
section[data-testid="stSidebar"] {
    background-color: #12161f !important;
    border-right: 1px solid #2a2f3a;
}
section[data-testid="stSidebar"] * {
    color: #e0e6ed !important;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif !important;
}

/* 체크박스 */
.stCheckbox label, .stCheckbox span {
    color: #e0e6ed !important;
}

/* 라디오/탭 버튼 */
.stRadio label {
    color: #e0e6ed !important;
}
button[kind="secondary"], .stButton button {
    background-color: #1a1f2e !important;
    color: #e0e6ed !important;
    border: 1px solid #2a2f3a !important;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif !important;
    border-radius: 0 !important;
}
button[kind="secondary"]:hover, .stButton button:hover {
    border-color: #00d4ff !important;
    color: #00d4ff !important;
}

/* tab 스타일 */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background-color: #12161f;
    border-bottom: 1px solid #2a2f3a;
}
.stTabs [data-baseweb="tab"] {
    background-color: #12161f;
    color: #888 !important;
    border-radius: 0 !important;
    padding: 8px 16px !important;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif !important;
    text-transform: uppercase;
    font-size: 13px !important;
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
    background-color: #12161f !important;
}

/* 카드 - 상태 표시 */
.kpi-card {
    background-color: #12161f;
    border: 1px solid #2a2f3a;
    padding: 12px 16px;
    margin: 4px;
    border-radius: 0px;
}
.kpi-label {
    color: #888;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.kpi-value {
    color: #e0e6ed;
    font-size: 24px;
    font-weight: bold;
    line-height: 1.1;
}
.kpi-delta-up   { color: #ff4444; }
.kpi-delta-down { color: #00ff88; }
.kpi-delta-flat { color: #888; }

/* 톱바 */
.topbar {
    background-color: #0a0d14;
    border-bottom: 1px solid #2a2f3a;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 24px;
    font-size: 13px;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif;
    color: #e0e6ed;
}
.topbar .brand {
    color: #00ff88;
    font-weight: bold;
    letter-spacing: 1px;
}
.topbar .live-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #00ff88;
    margin-right: 6px;
    box-shadow: 0 0 8px #00ff88;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* HEAT 라벨 */
.heat-badge {
    background-color: #ff4444;
    color: #fff;
    padding: 2px 8px;
    font-weight: bold;
    font-size: 12px;
}

/* status posture card */
.posture-row {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-bottom: 1px solid #2a2f3a;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif;
    font-size: 13px;
}
.posture-row:last-child { border-bottom: none; }
.posture-keyword { flex: 1; color: #e0e6ed; }
.posture-badge {
    padding: 2px 10px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-right: 8px;
    min-width: 60px;
    text-align: center;
}
.posture-r {
    color: #888;
    font-size: 12px;
    min-width: 90px;
    text-align: right;
}

/* 헤드라인 리스트 */
.headline-item {
    border-left: 2px solid #2a2f3a;
    padding: 6px 10px;
    margin-bottom: 8px;
    font-size: 13px;
    font-family: 'Pretendard Variable', 'Pretendard', sans-serif;
}
.headline-item:hover {
    border-left-color: #00d4ff;
    background-color: #12161f;
}
.headline-time { color: #00d4ff; font-size: 11px; }
.headline-source { color: #ff8c00; font-size: 11px; }
.headline-title { color: #e0e6ed; margin-top: 2px; }

/* insights 카드 */
.insight-card {
    background-color: #12161f;
    border-left: 3px solid #00d4ff;
    padding: 12px 16px;
    margin-bottom: 12px;
    font-size: 13px;
    line-height: 1.6;
    color: #e0e6ed;
}
.insight-card h4 { color: #00d4ff; margin: 0 0 6px 0; font-size: 12px; }

/* 헤더 줄 */
.section-header {
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 11px;
    margin-top: 16px;
    margin-bottom: 8px;
    border-bottom: 1px solid #2a2f3a;
    padding-bottom: 4px;
}

/* Streamlit 텍스트 색상 일관성 */
p, span, div, label {
    color: #e0e6ed;
}
/* 텍스트 입력 */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #12161f !important;
    color: #e0e6ed !important;
    border: 1px solid #2a2f3a !important;
}
</style>
"""
