"""대시보드 UI 컴포넌트들."""
from __future__ import annotations
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from . import meta


# ============================================================
# 다크 plotly 템플릿
# ============================================================
DARK_LAYOUT = dict(
    paper_bgcolor="#0a0d14",
    plot_bgcolor="#0a0d14",
    font=dict(family="Pretendard Variable, Pretendard, sans-serif", color="#e0e6ed", size=11),
    margin=dict(l=20, r=20, t=30, b=20),
    hoverlabel=dict(bgcolor="#12161f", font_color="#e0e6ed",
                    font_family="Pretendard Variable, Pretendard, sans-serif"),
)


# ============================================================
# 상단 KPI 카드
# ============================================================
def render_kpi_cards(heat_index: float, brent: float, brent_pct: float,
                     wti: float, wti_pct: float, top_keyword: str, top_r: float):
    cols = st.columns(5)
    cards = [
        ("CONFLICT HEAT", f"{heat_index:.1f}/10", "ELEVATED" if heat_index < 7 else "CRITICAL",
         "#ff4444" if heat_index > 7 else "#ff8c00"),
        ("BRENT", f"${brent:.2f}", f"▲ {brent_pct:+.1f}%" if brent_pct > 0 else f"▼ {brent_pct:.1f}%",
         "#ff4444" if brent_pct > 0 else "#00ff88"),
        ("WTI", f"${wti:.2f}", f"▲ {wti_pct:+.1f}%" if wti_pct > 0 else f"▼ {wti_pct:.1f}%",
         "#ff4444" if wti_pct > 0 else "#00ff88"),
        ("TOP SIGNAL", top_keyword[:14], f"r = {top_r:.3f}", "#00d4ff"),
        ("STATUS", "LIVE", "AS OF 2026-05-20", "#00ff88"),
    ]
    for col, (label, value, delta, color) in zip(cols, cards):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div style="color:{color}; font-size:11px; margin-top:2px;">{delta}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 지도 컴포넌트
# ============================================================
def render_map(selected_keywords: list[str], view: str,
               daily_kr: pd.DataFrame, daily_us: pd.DataFrame,
               corr_kr: pd.DataFrame, corr_us: pd.DataFrame,
               kr_source_counts: pd.DataFrame, us_source_counts: pd.DataFrame):
    """4가지 뷰 (중동/한국/미국/글로벌) 지도."""
    fig = go.Figure()

    if view in ("중동", "글로벌"):
        # 키워드 좌표 점들
        rows = []
        for kw in selected_keywords:
            coords = meta.KEYWORD_COORDS.get(kw)
            if coords is None:
                continue
            lat, lon, category, label = coords
            count = daily_kr[kw].sum() if kw in daily_kr.columns else 0
            r_row = corr_kr[corr_kr["keyword"] == kw]
            r = float(r_row["r"].iloc[0]) if len(r_row) else 0
            rows.append({
                "kw": kw, "label": label, "lat": lat, "lon": lon,
                "count": int(count), "r": r, "category": category,
            })
        if rows:
            df = pd.DataFrame(rows)
            # 크기 정규화 (5~40)
            sizes = np.clip(np.sqrt(df["count"]) * 1.2, 8, 50)
            fig.add_trace(go.Scattergeo(
                lon=df["lon"], lat=df["lat"],
                text=df["label"],
                mode="markers+text",
                marker=dict(
                    size=sizes,
                    color=[meta.CATEGORY_COLORS[c] for c in df["category"]],
                    opacity=0.85,
                    line=dict(color="#fff", width=0.5),
                ),
                textfont=dict(color="#e0e6ed", size=10),
                textposition="top center",
                customdata=df[["count", "r", "kw"]].values,
                hovertemplate=(
                    "<b>%{customdata[2]}</b><br>"
                    "위치: %{text}<br>"
                    "누적 빈도: %{customdata[0]:,}<br>"
                    "유가 상관 r = %{customdata[1]:.3f}<extra></extra>"
                ),
                name="Conflict Zones",
                showlegend=False,
            ))

    if view in ("한국", "글로벌"):
        # 한국 뉴스 출처 좌표
        rows = []
        for _, r_ in kr_source_counts.iterrows():
            src = r_["source"]
            cnt = r_["count"]
            coords = meta.KR_SOURCE_COORDS.get(src)
            if coords is None: continue
            rows.append({"src": src, "lat": coords[0], "lon": coords[1], "count": int(cnt)})
        if rows:
            df = pd.DataFrame(rows)
            sizes = np.clip(np.sqrt(df["count"]) * 0.8, 6, 30)
            fig.add_trace(go.Scattergeo(
                lon=df["lon"], lat=df["lat"],
                text=df["src"], mode="markers",
                marker=dict(
                    size=sizes,
                    color=meta.CATEGORY_COLORS["source_kr"],
                    opacity=0.85,
                    line=dict(color="#0a0d14", width=0.5),
                ),
                customdata=df[["count"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>기사 수: %{customdata[0]:,}<extra></extra>"
                ),
                name="KR Sources",
                showlegend=False,
            ))

    if view in ("미국", "글로벌"):
        rows = []
        for _, r_ in us_source_counts.iterrows():
            src = r_["source"]
            cnt = r_["count"]
            coords = meta.US_SOURCE_COORDS.get(src)
            if coords is None: continue
            rows.append({"src": src, "lat": coords[0], "lon": coords[1], "count": int(cnt)})
        if rows:
            df = pd.DataFrame(rows)
            sizes = np.clip(np.sqrt(df["count"]) * 0.8, 6, 30)
            fig.add_trace(go.Scattergeo(
                lon=df["lon"], lat=df["lat"],
                text=df["src"], mode="markers",
                marker=dict(
                    size=sizes,
                    color=meta.CATEGORY_COLORS["source_us"],
                    opacity=0.85,
                    line=dict(color="#0a0d14", width=0.5),
                ),
                customdata=df[["count"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>기사 수: %{customdata[0]:,}<extra></extra>"
                ),
                name="US/Global Sources",
                showlegend=False,
            ))

    v = meta.MAP_VIEWS[view]
    fig.update_geos(
        scope=v["scope"],
        showcountries=True, countrycolor="#2a2f3a",
        showocean=True, oceancolor="#0a0d14",
        showland=True, landcolor="#12161f",
        showlakes=False,
        showcoastlines=True, coastlinecolor="#2a2f3a",
        projection_type="natural earth",
        lataxis_range=v["lataxis"],
        lonaxis_range=v["lonaxis"],
        bgcolor="#0a0d14",
    )
    layout = {**DARK_LAYOUT, "margin": dict(l=0, r=0, t=10, b=0), "height": 620}
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 메인 시계열 차트
# ============================================================
def render_main_chart(selected_keywords: list[str],
                      daily_kr: pd.DataFrame, daily_us: pd.DataFrame,
                      oil: pd.DataFrame, metric: str = "raw",
                      show_oil: tuple = ("Brent", "WTI"),
                      show_events: bool = True, show_phases: bool = True):
    fig = go.Figure()
    suffix = "" if metric == "raw" else "__ratio"

    # 한국 키워드 빈도 (선택된 키워드 합)
    kr_kw_cols = [f"{k}{suffix}" for k in selected_keywords if f"{k}{suffix}" in daily_kr.columns]
    if kr_kw_cols:
        kr_total = daily_kr[kr_kw_cols].sum(axis=1)
        fig.add_trace(go.Scatter(
            x=daily_kr.index, y=kr_total, name="한국 키워드",
            mode="lines", line=dict(color="#00d4ff", width=1.5),
            fill="tozeroy", fillcolor="rgba(0, 212, 255, 0.15)",
            yaxis="y1",
        ))

    # 미국 키워드 빈도 (영문 키워드명으로 매칭)
    us_keywords = []
    for kr_kw in selected_keywords:
        # KEYWORDS_KR -> KEYWORDS_US 매핑 (좌표 사전을 통해서 추론)
        us_map = {
            "호르무즈 해협": "Strait of Hormuz", "혁명수비대(IRGC)": "IRGC",
            "테헤란 정권": "Tehran Regime", "샤헤드 드론": "Shahed Drone",
            "헤즈볼라 연계": "Hezbollah", "페르시아만 긴장": "Persian Gulf",
            "솔레이마니 사망 사건": "Soleimani", "시아파 영향권": "Shia Influence",
            "대리세력 네트워크": "Proxy Network", "시아 벨트": "Shia Belt",
            "핵협상(JCPOA)": "JCPOA", "제재 경제": "Sanctions",
            "중동 저항축": "Axis of Resistance", "비대칭 전력 전략": "Asymmetric Warfare",
        }
        if kr_kw in us_map: us_keywords.append(us_map[kr_kw])
    us_kw_cols = [f"{k}{suffix}" for k in us_keywords if f"{k}{suffix}" in daily_us.columns]
    if us_kw_cols:
        us_total = daily_us[us_kw_cols].sum(axis=1)
        fig.add_trace(go.Scatter(
            x=daily_us.index, y=us_total, name="미국 키워드",
            mode="lines", line=dict(color="#ff8c00", width=1.5),
            fill="tozeroy", fillcolor="rgba(255, 140, 0, 0.10)",
            yaxis="y1",
        ))

    # 유가 (오른쪽 y축)
    oil_colors = {"Brent": "#ff4444", "WTI": "#aa44ff"}
    for col in show_oil:
        if col in oil.columns:
            fig.add_trace(go.Scatter(
                x=oil.index, y=oil[col], name=col,
                mode="lines", line=dict(color=oil_colors[col], width=2,
                                        dash="solid" if col == "Brent" else "dash"),
                yaxis="y2",
            ))

    # 국면 음영
    if show_phases:
        for phase in meta.PHASES:
            fig.add_vrect(
                x0=phase["start"], x1=phase["end"],
                fillcolor=phase["color"], opacity=1, line_width=0,
                annotation_text=phase["label"],
                annotation_position="top left",
                annotation_font_color="#888",
                annotation_font_size=10,
            )

    # 이벤트 어노테이션
    if show_events:
        for ev in meta.EVENT_ANNOTATIONS:
            fig.add_vline(
                x=ev["date"], line=dict(color="#ffdd00", width=1, dash="dot"),
            )
            fig.add_annotation(
                x=ev["date"], y=1.0, yref="paper",
                text=f"⚡ {ev['title']}",
                showarrow=False, yshift=10,
                font=dict(color="#ffdd00", size=10),
                bgcolor="rgba(10, 13, 20, 0.8)",
                bordercolor="#ffdd00", borderwidth=1, borderpad=2,
            )

    fig.update_layout(
        **DARK_LAYOUT,
        height=600,
        xaxis=dict(
            gridcolor="#2a2f3a", showgrid=True, color="#888",
            type="date",
        ),
        yaxis=dict(
            title="키워드 빈도 (일별)", color="#00d4ff",
            gridcolor="#2a2f3a", showgrid=True,
        ),
        yaxis2=dict(
            title="유가 ($/배럴)", color="#ff4444",
            overlaying="y", side="right", showgrid=False,
        ),
        legend=dict(
            x=0.01, y=0.99, bgcolor="rgba(18, 22, 31, 0.8)",
            bordercolor="#2a2f3a", borderwidth=1, font=dict(size=11),
        ),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 하단: TOP HEADLINES 패널
# ============================================================
def render_headlines(news_df: pd.DataFrame, country_label: str,
                     selected_date: datetime.date | None = None, limit: int = 12):
    """선택된 날짜 (or 최신) 헤드라인 표시."""
    if selected_date is None:
        selected_date = news_df["date"].max()
    day_news = news_df[news_df["date"] == selected_date].sort_values(
        "published_kst", ascending=False
    ).head(limit)
    st.markdown(f"<div class='section-header'>📰 {country_label} HEADLINES — {selected_date}</div>",
                unsafe_allow_html=True)
    if day_news.empty:
        st.markdown("<div style='color:#888; font-size:13px;'>해당일 헤드라인 없음</div>",
                    unsafe_allow_html=True)
        return
    html = ""
    for _, row in day_news.iterrows():
        t = row["published_kst"].strftime("%H:%M") if pd.notna(row["published_kst"]) else ""
        src = (row["source"] or "")[:20]
        title = row["title"][:120]
        html += f"""
        <div class="headline-item">
            <span class="headline-time">{t}</span>
            &nbsp;<span class="headline-source">[{src}]</span>
            <div class="headline-title">{title}</div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# 하단: 캘린더 히트맵
# ============================================================
def render_calendar(daily: pd.DataFrame, keyword: str, title: str = ""):
    if keyword not in daily.columns:
        st.markdown(f"<div style='color:#888'>{keyword} 데이터 없음</div>",
                    unsafe_allow_html=True)
        return
    s = daily[keyword]
    df = pd.DataFrame({
        "date": s.index,
        "week": s.index.isocalendar().week,
        "weekday": s.index.weekday,
        "value": s.values,
    })
    pivot = df.pivot(index="weekday", columns="week", values="value")
    fig = px.imshow(
        pivot,
        color_continuous_scale=[
            [0, "#12161f"],
            [0.15, "#1e3a52"],
            [0.4, "#ff8c00"],
            [0.7, "#ff4444"],
            [1.0, "#ff0000"],
        ],
        aspect="auto",
        labels=dict(x="Week", y="Day", color=keyword),
    )
    layout_cal = {**DARK_LAYOUT,
                  "height": 180,
                  "title": dict(text=title or f"📅 {keyword}",
                                font=dict(size=12, color="#888")),
                  "margin": dict(l=20, r=20, t=30, b=20),
                  "coloraxis_colorbar": dict(thickness=8, len=0.8)}
    fig.update_layout(**layout_cal)
    fig.update_xaxes(showgrid=False, color="#888")
    fig.update_yaxes(showgrid=False, color="#888",
                     tickvals=list(range(7)),
                     ticktext=["M","T","W","T","F","S","S"])
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 하단: INSIGHTS + STATUS 카드
# ============================================================
def render_insights(corr_kr: pd.DataFrame, corr_us: pd.DataFrame,
                    heat_index: float):
    # 분석 브리프
    top_kr = corr_kr.iloc[0] if len(corr_kr) else None
    top_us = corr_us.iloc[0] if len(corr_us) else None
    brief_html = "<div class='insight-card'>"
    brief_html += "<h4>⬤ 분석 브리프</h4>"
    if top_kr is not None:
        brief_html += (f"<b>{top_kr['keyword']}</b> 키워드가 한국 뉴스에서 Brent와 "
                       f"<b style='color:#ff4444'>r={top_kr['r']:.3f}</b> "
                       f"(lag={int(top_kr['lag'])}일, p={top_kr['p']:.1e})의 강한 상관. ")
    if top_us is not None:
        brief_html += (f"미국 뉴스에서는 <b>{top_us['keyword']}</b>가 "
                       f"<b style='color:#ff4444'>r={top_us['r']:.3f}</b> (lag={int(top_us['lag'])}). ")
    brief_html += f"Conflict Heat: <b>{heat_index:.1f}/10</b>."
    brief_html += "</div>"
    st.markdown(brief_html, unsafe_allow_html=True)

    # STATUS 카드
    st.markdown("<div class='section-header'>⚔️ KEYWORD STATUS</div>", unsafe_allow_html=True)
    html = "<div class='insight-card' style='border-left-color:#ff4444; padding: 4px 0;'>"
    for _, row in corr_kr.head(8).iterrows():
        status, color = meta.status_from_r(row["r"])
        html += f"""
        <div class="posture-row">
            <span class="posture-keyword">{row['keyword']}</span>
            <span class="posture-badge" style="background-color:{color}; color:#0a0d14;">{status}</span>
            <span class="posture-r">r={row['r']:+.3f} l={int(row['lag'])}</span>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
