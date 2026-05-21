"""데이터 로더 + 지표 계산."""
from __future__ import annotations
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import streamlit as st

DATA_DIR = Path("./data")


@st.cache_data
def load_news_kr() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "news_kr.csv")
    df["published_kst"] = pd.to_datetime(df["published_kst"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["published_kst", "title"]).reset_index(drop=True)
    return df


@st.cache_data
def load_news_us() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "news_us.csv")
    df["published_kst"] = pd.to_datetime(df["published_kst"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["published_kst", "title"]).reset_index(drop=True)
    return df


@st.cache_data
def load_oil() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "oil_prices.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


@st.cache_data
def load_daily_kr() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "daily_keyword_freq_kr.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


@st.cache_data
def load_daily_us() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "daily_keyword_freq_us.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


# ============================================================
# 일별 키워드 매트릭스에 ratio 컬럼 추가 (v5 호환)
# ============================================================
@st.cache_data
def add_ratio_columns(daily: pd.DataFrame, keyword_cols: list[str]) -> pd.DataFrame:
    daily = daily.copy()
    total = daily["total_headlines"]
    for kw in keyword_cols:
        if kw in daily.columns:
            daily[f"{kw}__ratio"] = daily[kw] / total.replace(0, np.nan) * 100
    return daily


# ============================================================
# Conflict Heat Index — 옵션 A: 상위 5 키워드 빈도 / total * 100 의 최근 7일 평균
# ============================================================
def conflict_heat_index(daily_kr: pd.DataFrame, daily_us: pd.DataFrame) -> float:
    """최근 7일 평균으로 0-10 스케일 Conflict Heat Index."""
    def _country_heat(daily, top_keywords):
        recent = daily.tail(7)
        if recent.empty: return 0.0
        kw_sum = recent[top_keywords].sum(axis=1)
        total = recent["total_headlines"]
        ratio = (kw_sum / total.replace(0, np.nan)).fillna(0)
        return float(ratio.mean() * 100)  # %

    top_kr = ["호르무즈 해협", "혁명수비대(IRGC)", "헤즈볼라 연계", "제재 경제", "테헤란 정권"]
    top_us = ["Strait of Hormuz", "IRGC", "Hezbollah", "Tehran Regime", "Persian Gulf"]
    top_kr = [k for k in top_kr if k in daily_kr.columns]
    top_us = [k for k in top_us if k in daily_us.columns]

    heat_kr = _country_heat(daily_kr, top_kr)
    heat_us = _country_heat(daily_us, top_us)
    # 두 국가 평균, 100% 기준을 10 스케일로
    combined = (heat_kr + heat_us) / 2
    # 일반적으로 5-15% 정도라 ÷1.5로 10 스케일 맞춤 (관측 데이터 기준)
    return min(10.0, combined / 1.5)


# ============================================================
# 시차 상관 계산
# ============================================================
@st.cache_data
def best_lag_correlations(daily: pd.DataFrame, oil_col: str,
                          keyword_cols: list[str], suffix: str = "") -> pd.DataFrame:
    """키워드별 best |r| + lag 반환 (raw 또는 ratio)."""
    # 유가 일별 forward-fill
    start = daily.index.min()
    end = daily.index.max()
    oil_all = load_oil().reindex(pd.date_range(start, end, freq="D")).ffill()

    rows = []
    for kw in keyword_cols:
        col = f"{kw}{suffix}"
        if col not in daily.columns:
            continue
        best = {"keyword": kw, "r": np.nan, "lag": 0, "p": 1.0, "n": 0}
        for lag in range(-7, 8):
            x = daily[col].shift(-lag)
            y = oil_all[oil_col]
            valid = pd.concat([x, y], axis=1).dropna()
            if len(valid) < 15 or valid.iloc[:, 0].std() == 0:
                continue
            r, p = stats.pearsonr(valid.iloc[:, 0], valid.iloc[:, 1])
            if abs(r) > abs(best["r"]) or best["n"] == 0:
                best = {"keyword": kw, "r": r, "lag": lag, "p": p, "n": len(valid)}
        rows.append(best)
    return pd.DataFrame(rows).sort_values("r", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


# ============================================================
# 소스별 기사 수 집계 (지도 [한국]/[미국] 뷰용)
# ============================================================
@st.cache_data
def source_counts(news_df: pd.DataFrame, top_n: int = 40) -> pd.DataFrame:
    counts = news_df["source"].value_counts().head(top_n).reset_index()
    counts.columns = ["source", "count"]
    return counts
