"""
IRAN-US CONFLICT MONITOR — v6 Dashboard
worldmonitor.app 스타일 다크 인텔리전스 대시보드.

실행:
    streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd

from dashboard_app import data as D
from dashboard_app import meta
from dashboard_app import components as C
from dashboard_app.theme import THEME_CSS

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title='print("cps")',
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Open Graph / Twitter Card 메타 태그 (링크 공유 시 미리보기)
SHARE_TITLE = 'print("cps")'
SHARE_DESC = 'Iran-US Conflict Monitor — Real-time intelligence dashboard'
SHARE_URL = 'https://monitor.printcps.cloud'

st.markdown(f"""
<meta name="description" content='{SHARE_DESC}'>
<meta property="og:title" content='{SHARE_TITLE}'>
<meta property="og:description" content='{SHARE_DESC}'>
<meta property="og:type" content='website'>
<meta property="og:url" content='{SHARE_URL}'>
<meta property="og:site_name" content='print("cps")'>
<meta name="twitter:card" content='summary'>
<meta name="twitter:title" content='{SHARE_TITLE}'>
<meta name="twitter:description" content='{SHARE_DESC}'>
""", unsafe_allow_html=True)

st.markdown(THEME_CSS, unsafe_allow_html=True)

# ============================================================
# 데이터 로딩
# ============================================================
news_kr = D.load_news_kr()
news_us = D.load_news_us()
oil = D.load_oil()
daily_kr_raw = D.load_daily_kr()
daily_us_raw = D.load_daily_us()
daily_kr = D.add_ratio_columns(daily_kr_raw, list(meta.KEYWORDS_KR.keys()))
daily_us = D.add_ratio_columns(daily_us_raw, list(meta.KEYWORDS_US.keys()))
kr_src_counts = D.source_counts(news_kr, top_n=30)
us_src_counts = D.source_counts(news_us, top_n=40)

# 지표 계산
heat = D.conflict_heat_index(daily_kr, daily_us)
brent = float(oil["Brent"].iloc[-1])
wti = float(oil["WTI"].iloc[-1])
brent_pct = float(oil["Brent"].iloc[-1] / oil["Brent"].iloc[0] - 1) * 100
wti_pct = float(oil["WTI"].iloc[-1] / oil["WTI"].iloc[0] - 1) * 100

# 상관관계
corr_kr_brent = D.best_lag_correlations(daily_kr, "Brent", list(meta.KEYWORDS_KR.keys()))
corr_us_brent = D.best_lag_correlations(daily_us, "Brent", list(meta.KEYWORDS_US.keys()))
top_kw = corr_kr_brent.iloc[0]["keyword"] if len(corr_kr_brent) else "—"
top_r = float(corr_kr_brent.iloc[0]["r"]) if len(corr_kr_brent) else 0.0

# ============================================================
# Topbar (worldmonitor 스타일)
# ============================================================
st.markdown(f"""
<div class="topbar">
    <span class="brand">⬤ IRAN-US MONITOR <span style="color:#888;">v6.0</span></span>
    <span style="color:#888;">|</span>
    <span><span class="live-dot"></span>AS OF 2026-05-20 KST</span>
    <span style="color:#888;">|</span>
    <span>⚡ <span class="heat-badge">HEAT {heat:.1f}/10</span></span>
    <span style="color:#888;">|</span>
    <span style="color:#ff4444;">$ {brent:.2f} BRENT</span>
    <span style="color:#aa44ff;">$ {wti:.2f} WTI</span>
    <span style="margin-left:auto; color:#888;">🟢 v6 | {len(news_kr)+len(news_us):,} sources</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 사이드바 (좌측 KEYWORDS 패널 — worldmonitor의 LAYERS와 동일 위치)
# ============================================================
with st.sidebar:
    st.markdown("<div class='section-header'>🎯 LAYERS / KEYWORDS</div>",
                unsafe_allow_html=True)
    default_keywords = ["호르무즈 해협", "혁명수비대(IRGC)", "헤즈볼라 연계",
                        "제재 경제", "핵협상(JCPOA)", "테헤란 정권"]
    selected_keywords = []
    for kw in meta.KEYWORDS_KR.keys():
        default = kw in default_keywords
        if st.checkbox(kw, value=default, key=f"kw_{kw}"):
            selected_keywords.append(kw)

    st.markdown("<div class='section-header'>⚙️ OPTIONS</div>", unsafe_allow_html=True)
    metric_choice = st.radio("METRIC", ["raw", "ratio"], horizontal=True)
    show_oil_opts = st.multiselect("OIL", ["Brent", "WTI"], default=["Brent", "WTI"])
    show_events = st.checkbox("📌 EVENT MARKERS", value=True)
    show_phases = st.checkbox("🎭 PHASE SHADING", value=True)

    st.markdown("<div class='section-header'>🎨 LEGEND</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:11px; line-height:1.8;'>
    <span style='color:#ff4444;'>●</span> Conflict Zone<br>
    <span style='color:#ff8c00;'>●</span> Strategic Hub<br>
    <span style='color:#aa44ff;'>●</span> Proxy Network<br>
    <span style='color:#00d4ff;'>●</span> Diplomacy<br>
    <span style='color:#00ff88;'>●</span> KR News Source<br>
    <span style='color:#ffdd00;'>●</span> US/Global Source<br>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 메인 KPI 카드
# ============================================================
C.render_kpi_cards(heat, brent, brent_pct, wti, wti_pct, top_kw, top_r)

# ============================================================
# SITUATION 섹션 — 지도 ↔ 차트 탭 전환
# ============================================================
st.markdown(
    f"<div class='section-header' style='display:flex; justify-content:space-between;'>"
    f"<span>📍 SITUATION</span>"
    f"<span style='color:#888'>FRI, 20 MAY 2026 21:30 KST</span>"
    f"</div>", unsafe_allow_html=True)

# 뷰 토글 (지도 영역)
view_col1, view_col2 = st.columns([3, 1])
with view_col1:
    main_view = st.radio("VIEW", ["🗺️ MAP", "📊 CHART"],
                         horizontal=True, label_visibility="collapsed")
with view_col2:
    if main_view == "🗺️ MAP":
        map_zoom = st.radio("ZOOM", ["중동", "한국", "미국", "글로벌"],
                            horizontal=True, label_visibility="collapsed")
    else:
        map_zoom = "중동"

if main_view == "🗺️ MAP":
    C.render_map(selected_keywords, map_zoom,
                 daily_kr, daily_us, corr_kr_brent, corr_us_brent,
                 kr_src_counts, us_src_counts)
else:
    C.render_main_chart(selected_keywords, daily_kr, daily_us, oil,
                        metric=metric_choice,
                        show_oil=tuple(show_oil_opts),
                        show_events=show_events,
                        show_phases=show_phases)

# ============================================================
# 하단 3분할: HEADLINES | CALENDAR | INSIGHTS
# ============================================================
b1, b2, b3 = st.columns([1.2, 1.2, 1])

with b1:
    country_tabs = st.tabs(["🇰🇷 KR", "🇺🇸 US"])
    with country_tabs[0]:
        # 날짜 선택
        date_opts = sorted(news_kr["date"].dropna().unique(), reverse=True)[:30]
        sel_date = st.selectbox("날짜", date_opts, key="kr_date", label_visibility="collapsed")
        C.render_headlines(news_kr, "KR", sel_date)
    with country_tabs[1]:
        date_opts_us = sorted(news_us["date"].dropna().unique(), reverse=True)[:30]
        sel_date_us = st.selectbox("날짜", date_opts_us, key="us_date", label_visibility="collapsed")
        C.render_headlines(news_us, "US", sel_date_us)

with b2:
    st.markdown("<div class='section-header'>📅 KEYWORD INTENSITY</div>",
                unsafe_allow_html=True)
    cal_kw = st.selectbox("KEYWORD", selected_keywords or list(meta.KEYWORDS_KR.keys())[:1],
                          key="cal_kw", label_visibility="collapsed")
    C.render_calendar(daily_kr, cal_kw, f"{cal_kw} (KR)")
    # US도 (영문 매핑)
    us_map = {
        "호르무즈 해협":"Strait of Hormuz","혁명수비대(IRGC)":"IRGC",
        "테헤란 정권":"Tehran Regime","샤헤드 드론":"Shahed Drone",
        "헤즈볼라 연계":"Hezbollah","페르시아만 긴장":"Persian Gulf",
        "솔레이마니 사망 사건":"Soleimani","핵협상(JCPOA)":"JCPOA","제재 경제":"Sanctions",
    }
    us_kw = us_map.get(cal_kw)
    if us_kw and us_kw in daily_us.columns:
        C.render_calendar(daily_us, us_kw, f"{us_kw} (US)")

with b3:
    C.render_insights(corr_kr_brent, corr_us_brent, heat)
