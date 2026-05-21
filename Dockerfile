# Iran-US Conflict Monitor — v6 Dashboard
# Single-stage build (대부분 패키지가 pre-built wheel 사용 가능)

FROM python:3.12-slim

WORKDIR /app

# 런타임 의존성만 (curl: 헬스체크)
# DNS 이슈 회피를 위해 apt 옵션 추가
RUN echo 'Acquire::http::Timeout "120";' > /etc/apt/apt.conf.d/99timeout \
    && echo 'Acquire::Retries "3";' >> /etc/apt/apt.conf.d/99timeout \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

COPY requirements.txt .

# pre-built wheel 우선 사용 (--prefer-binary)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefer-binary \
        -r requirements.txt \
        streamlit>=1.50.0 \
        plotly>=6.0.0

# 코드 + 데이터 + Streamlit 설정 복사
COPY --chown=appuser:appuser dashboard.py ./
COPY --chown=appuser:appuser dashboard_app/ ./dashboard_app/
COPY --chown=appuser:appuser .streamlit/ ./.streamlit/
COPY --chown=appuser:appuser data/ ./data/

# Streamlit의 정적 index.html에 OG/Twitter 메타 태그 주입
# (소셜 크롤러는 JS 안 돌려서 st.set_page_config의 title은 못 봄)
RUN python -c "\
import pathlib; \
p = pathlib.Path('/usr/local/lib/python3.12/site-packages/streamlit/static/index.html'); \
html = p.read_text(); \
meta = '''    <title>print(\"cps\")</title>\n\
    <meta name=\"description\" content=\"Iran-US Conflict Monitor — real-time intelligence dashboard\">\n\
    <meta property=\"og:title\" content='print(\"cps\")'>\n\
    <meta property=\"og:description\" content=\"Iran-US Conflict Monitor\">\n\
    <meta property=\"og:type\" content=\"website\">\n\
    <meta property=\"og:url\" content=\"https://monitor.printcps.cloud\">\n\
    <meta property=\"og:site_name\" content='print(\"cps\")'>\n\
    <meta name=\"twitter:card\" content=\"summary\">\n\
    <meta name=\"twitter:title\" content='print(\"cps\")'>\n\
    <meta name=\"twitter:description\" content=\"Iran-US Conflict Monitor\">\n'''; \
html = html.replace('<title>Streamlit</title>', meta); \
p.write_text(html); \
print('✅ index.html patched')"

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "dashboard.py"]
