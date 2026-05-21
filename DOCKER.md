# Docker 실행 가이드

## 사전 준비

WSL에서 Docker를 사용하려면 다음 중 하나:

### Option A — Docker Desktop for Windows (권장)
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치
2. Settings → Resources → WSL Integration → 본인 배포판 활성화
3. WSL 터미널에서 `docker --version` 확인

### Option B — Docker Engine in WSL (sudo 필요)
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl start docker
sudo usermod -aG docker $USER
# 로그아웃 후 재로그인
```

## 빌드 및 실행

### 1단계: 이미지 빌드 (5-10분, 의존성 다운로드 포함)
```bash
docker compose build
```

또는 docker 단독:
```bash
docker build -t iran-us-monitor:v6 .
```

### 2단계: 컨테이너 실행
```bash
docker compose up -d        # 백그라운드 실행
# 또는
docker compose up           # 포어그라운드 (로그 보면서)
```

### 3단계: 브라우저 접속
- http://localhost:8501

### 4단계: 정지
```bash
docker compose down
```

## 자주 쓰는 명령어

```bash
# 로그 보기
docker compose logs -f dashboard

# 컨테이너 상태
docker compose ps

# 헬스체크 상태
docker inspect iran-us-monitor --format='{{.State.Health.Status}}'

# 재시작 (코드 변경 시)
docker compose restart

# 이미지 다시 빌드 (의존성 변경 시)
docker compose up -d --build

# 컨테이너 + 이미지 + 볼륨 모두 삭제
docker compose down --rmi all -v
```

## 데이터 업데이트

`data/` 폴더가 read-only 볼륨으로 마운트돼 있어서 **CSV 파일 갱신 시 재빌드 불필요**:
```bash
# 노트북에서 새 CSV 만든 후
docker compose restart   # 컨테이너만 재시작
```

## 이미지 사양

| 항목 | 값 |
|------|---|
| 베이스 | python:3.12-slim |
| 빌드 방식 | multi-stage (builder + runtime) |
| 예상 크기 | ~800MB-1GB |
| 포트 | 8501 |
| 사용자 | appuser (UID 1000, non-root) |
| 헬스체크 | Streamlit `/_stcore/health` 엔드포인트 |
| 시간대 | Asia/Seoul |

## 배포 (옵션)

### 로컬 네트워크 공유
```bash
# 다른 기기에서 접속하려면 호스트 IP 확인
ip addr show eth0 | grep inet

# 같은 네트워크에서 http://<host-ip>:8501 접속
```

### 클라우드 배포 (예시)
- **Streamlit Cloud**: 무료, 깃허브 연동 (Docker 불필요)
- **Railway/Render**: Docker 이미지 직접 배포
- **AWS ECS / GCP Cloud Run**: 프로덕션급
- **fly.io**: 글로벌 엣지 배포 무료 tier

`docker push` + 각 플랫폼 README 참고.
