# Python 공식 이미지 사용 (slim 버전을 사용해 용량을 최소화)
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
# Playwright는 브라우저를 실행하기 위해 특정 시스템 라이브러리가 필요합니다.
# 이 명령은 Debian/Ubuntu 기반 이미지에 필요한 의존성을 설치합니다.
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libatspi2.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxshmfence1 \
    libxxf86vm1 \
    libdbus-glib-1-2 \
    procps \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 Python 라이브러리 설치
# 먼저 의존성 파일만 복사해서 Docker의 빌드 캐시를 효율적으로 사용합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치 (가장 중요)
# pip install과는 별개로 이 명령어를 통해 브라우저를 다운로드해야 합니다.
RUN playwright install --with-deps chromium

# 모든 애플리케이션 코드 복사
COPY . .

# 애플리케이션 실행 명령어
# 오류 메시지에서 main.py가 실행되는 것으로 보이므로 이 파일을 지정합니다.
# 만약 Flask 서버를 gunicorn 등으로 실행한다면 이 부분을 수정해야 합니다.
# 예시: CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
CMD ["python", "main.py"]