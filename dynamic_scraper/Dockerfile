# Python 공식 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 및 Playwright 브라우저 설치에 필요한 라이브러리 설치
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
    libgl1-mesa-glx \
    libfontconfig1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 Python 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치 (캐시 경로 지정)
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright
RUN mkdir -p $PLAYWRIGHT_BROWSERS_PATH && playwright install --with-deps chromium

# 모든 애플리케이션 코드 복사
COPY . .

# 애플리케이션 실행 명령어 (main.py 실행)
CMD ["python", "main.py"]