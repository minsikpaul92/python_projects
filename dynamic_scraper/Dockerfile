# Python 공식 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 및 Playwright 브라우저 설치에 필요한 라이브러리 설치
# RUN apt-get update && apt-get install -y --no-install-recommends ... 와 동일한 역할을 합니다.
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
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치 (매우 중요)
# --with-deps 옵션으로 필요한 모든 브라우저 의존성을 함께 설치합니다.
RUN playwright install --with-deps chromium

# 모든 애플리케이션 코드 복사
COPY . .

# 애플리케이션 실행 명령어 변경
# main.py 대신 gunicorn을 사용하여 app.py의 Flask 앱을 실행합니다.
# Railway는 PORT 환경 변수를 동적으로 할당하므로 이를 사용합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]