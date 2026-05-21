# Iran-US Conflict Monitor — Dashboard 사용 가이드

worldmonitor.app 스타일 인터랙티브 인텔리전스 대시보드.

## 실행

```bash
cd iran-us-news-oil-analysis
.venv/bin/streamlit run dashboard.py
```

자동으로 브라우저가 열리거나, 수동 접속:
- Local: http://localhost:8501
- Network: 터미널에 표시된 Network URL (다른 기기에서 접속할 때)

## UI 가이드

### 🔝 상단 바
- ⬤ IRAN-US MONITOR — 프로젝트 라벨
- 🟢 AS OF 2026-05-20 KST — 데이터 시점
- ⚡ HEAT N/10 — Conflict Heat Index
- $ Brent / WTI — 최신 유가

### 📊 KPI 5장 카드
- CONFLICT HEAT (0-10)
- BRENT 가격 + 변화율
- WTI 가격 + 변화율
- TOP SIGNAL (최강 상관 키워드 + r 값)
- STATUS (정적 데이터 라벨)

### 🎯 사이드바 (좌측)
- 14개 키워드 체크박스 → 지도/차트 동기화
- METRIC: raw 또는 ratio
- OIL: Brent/WTI 선택
- EVENT MARKERS, PHASE SHADING 토글
- LEGEND (색상 범례)

### 🗺️ 지도 (MAP 탭)
4가지 줌 뷰:
- **중동** (디폴트) — 키워드 좌표 (호르무즈, 테헤란, Beirut 등)
- **한국** — 한국 매체 본사 위치 (점 크기 = 기사 수)
- **미국** — 미국/글로벌 매체 분포
- **글로벌** — 위 모든 점 + Vienna(JCPOA), London(BBC, Reuters), Doha(AlJazeera) 등

마우스 hover → 누적 빈도, 상관 r 값 툴팁.

### 📈 시계열 (CHART 탭)
- 한국·미국 키워드 빈도 (좌측 y축)
- Brent / WTI 유가 (우측 y축)
- 이벤트 마커 (⚡): 트럼프 위협, escalation 시작, 종전 협상 등
- Phase 음영: Calm(녹색)/Escalation(빨강)/Sustained(주황)

### 📰 헤드라인 (하단 좌)
- KR/US 탭
- 날짜 선택 박스 (최근 30일)
- 그날 보도된 헤드라인 12건 (출처+시간 포함)

### 📅 캘린더 (하단 중)
- 선택된 키워드의 일별 빈도 (요일 × 주차)
- KR/US 별도 표시

### 🧠 인사이트 (하단 우)
- 분석 브리프 자동 생성
- KEYWORD STATUS 카드: 상위 8개 키워드의 등급 (CRIT/HIGH/MED/STABLE)

## STATUS 등급 기준 (Pearson |r|)
| 등급 | 임계값 | 색상 |
|------|--------|------|
| CRIT | \|r\| > 0.5 | 🔴 빨강 |
| HIGH | \|r\| > 0.3 | 🟠 주황 |
| MED | \|r\| > 0.1 | 🟡 노랑 |
| STABLE | \|r\| ≤ 0.1 | 🔵 시안 |

## Conflict Heat Index
- 최근 7일 평균
- 공식: 상위 5개 키워드 빈도 / total_headlines × 100 / 1.5
- 0-10 스케일

## 트러블슈팅

### 한글이 깨져 보임
matplotlib 폰트 문제와 무관 — Streamlit/Plotly는 시스템 폰트 사용. 브라우저에 한글 폰트가 있으면 정상.

### 포트 8501 사용 중
```bash
.venv/bin/streamlit run dashboard.py --server.port 8502
```

### 데이터 새로고침
사이드바 우상단 ⋮ → "Clear cache" → "Rerun"
