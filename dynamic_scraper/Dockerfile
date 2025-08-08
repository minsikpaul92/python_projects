FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# playwright 브라우저 엔진 설치
RUN playwright install

# Flask 앱 실행
CMD ["python", "app.py"]