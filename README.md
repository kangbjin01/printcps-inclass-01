# Iran-US Conflict Monitor

이란-미국 분쟁(2026.01-05) 뉴스 헤드라인의 키워드 빈도와 국제 유가(Brent/WTI)의 상관관계를 분석하고, worldmonitor.app 스타일 인터랙티브 대시보드로 시각화한 프로젝트.

🌐 **Live**: [https://monitor.printcps.cloud](https://monitor.printcps.cloud)

---

## 📋 개요

| 항목 | 내용 |
|------|------|
| 분석 기간 | 2026-01-01 ~ 2026-05-20 (KST 기준) |
| 뉴스 데이터 | Google News RSS (한국/미국 분리, 50,298건) |
| 유가 데이터 | yfinance Brent (`BZ=F`) + WTI (`CL=F`) |
| 분석 대상 키워드 | 14개 (호르무즈 해협, 혁명수비대, 헤즈볼라 등) |
| 시각화 | Jupyter Notebook + Streamlit 대시보드 |
| 배포 | Docker + Cloudflare Tunnel |

## 🔍 핵심 발견

**호르무즈 해협 / Strait of Hormuz**가 양국 뉴스 모두에서 유가와 가장 강한 상관:
- 한국 뉴스: r = 0.676 (p < 10⁻¹⁸), lag = +6일
- 미국 뉴스: r = 0.592 (p < 10⁻¹³), lag = +7일

정규화 후에도 견고한 진짜 신호 vs 보도량에 휘둘린 가짜 신호 구분 — 자세한 내용은 [METHODOLOGY.md](./METHODOLOGY.md) 참조.

## 🏗️ 프로젝트 구조

```
iran-us-news-oil-analysis/
├── 📓 news_oil_analysis.ipynb     # 메인 분석 노트북 (50셀)
├── 🚀 dashboard.py                # Streamlit 대시보드 엔트리
├── 📦 dashboard_app/              # 대시보드 컴포넌트
│   ├── meta.py                    # 키워드/좌표/이벤트 상수
│   ├── data.py                    # CSV 로더 + 지표 계산
│   ├── theme.py                   # 다크 테마 CSS
│   └── components.py              # KPI/지도/차트/헤드라인
├── 🐳 Dockerfile                  # 컨테이너 빌드
├── 🐳 docker-compose.yml          # 대시보드 + Cloudflare Tunnel
├── 📊 data/                       # 분석 데이터
│   ├── news_kr.csv               # 한국 헤드라인 (21,455건)
│   ├── news_us.csv               # 미국 헤드라인 (28,843건)
│   ├── oil_prices.csv            # Brent + WTI 일별 종가
│   └── daily_keyword_freq_*.csv   # 일별 키워드 빈도 매트릭스
├── 📚 METHODOLOGY.md              # 수집/분석 방법론
├── 📚 DASHBOARD.md                # 대시보드 사용 가이드
└── 📚 DOCKER.md                   # Docker 배포 가이드
```

## 🚀 빠른 시작

### Option 1 — 로컬에서 노트북 실행

```bash
# 1. 의존성 설치
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 노트북 실행
jupyter notebook news_oil_analysis.ipynb
```

### Option 2 — 로컬에서 대시보드 실행

```bash
# 의존성 + Streamlit
pip install -r requirements.txt streamlit plotly

# 실행
streamlit run dashboard.py
# → http://localhost:8501
```

### Option 3 — Docker로 실행 (권장)

```bash
docker compose build
docker compose up -d
# → http://localhost:8501 (포트 노출 활성화 시)
```

상세 가이드는 [DOCKER.md](./DOCKER.md) 참조.

### Option 4 — Docker + Cloudflare Tunnel (공개 배포)

```bash
# 1. .env.example을 .env로 복사하고 토큰 채우기
cp .env.example .env
# vim .env  → TUNNEL_TOKEN= 채우기

# 2. 실행
docker compose up -d
# → https://monitor.<your-domain> (Cloudflare DNS 자동 생성)
```

## 📊 분석 흐름

1. **수집** — Google News RSS에 30개 키워드 × 20개 7일 윈도우 = 600 쿼리 × 한/미 → 5만+ 헤드라인
2. **정제** — KST 기준 발행일 정렬, 중복 제거
3. **카운트** — 14개 분석 키워드별 일별 매트릭스 생성
4. **정규화** — `raw` (절대 카운트) vs `ratio` (% of total headlines)
5. **상관분석** — Pearson 시차(lag) −7~+7일, Brent/WTI 각각
6. **시각화** — 시계열·히트맵·산점도·워드클라우드·캘린더 + 인터랙티브 대시보드

## 🛠️ 기술 스택

- **분석**: Python 3.12, pandas 3.0, scipy, yfinance, feedparser
- **시각화**: matplotlib, seaborn, plotly, wordcloud
- **대시보드**: Streamlit + Plotly + Pretendard
- **배포**: Docker, Cloudflare Tunnel

## ⚠️ 한계 및 주의

- Google News RSS는 과거 데이터 완전성 보장 X (1월 초 헤드라인 적음)
- 상관관계 ≠ 인과관계
- `laplace`/`smooth` 정규화는 저-count 키워드에서 인공물 생성 → 제외 (v5 이후)
- 자세한 한계는 [METHODOLOGY.md](./METHODOLOGY.md) 참조

## 📝 라이선스

학술/연구 목적. 데이터는 Google News RSS 공개 피드, 분석 코드는 자유롭게 사용/수정 가능.

---

🤖 *Built with Claude Code*
