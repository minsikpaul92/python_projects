# 1. Python 공식 이미지 사용
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 의존성 설치
# Playwright는 브라우저를 실행하기 위해 여러 라이브러리가 필요합니다.
# 이 명령어는 Debian/Ubuntu 기반 이미지에 필요한 의존성을 설치합니다.
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

# 4. requirements.txt 복사 및 Python 라이브러리 설치
# 먼저 의존성 파일만 복사해서 캐싱 효율을 높입니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Playwright 브라우저 설치 (가장 중요)
# 이 명령어가 Railway 오류를 해결하는 핵심입니다.
# --with-deps 플래그를 사용하여 필요한 모든 의존성을 함께 설치합니다.
# 필요한 브라우저(chromium, firefox, webkit)를 지정할 수 있습니다.
RUN playwright install --with-deps chromium

# 6. 애플리케이션 코드 복사
COPY . .

# 7. 애플리케이션 실행 명령어
# Flask 애플리케이션에 맞게 CMD를 수정하세요.
# 예: CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
# 또는 간단한 실행의 경우: CMD ["python", "main.py"]
CMD ["python", "main.py"]