FROM python:3.9.6-alpine

WORKDIR /app

COPY requirements.txt .

# ref: https://orolog.hatenablog.jp/entry/2018/09/03/233609
RUN apk --no-cache add gcc libc-dev libxml2-dev libxslt-dev
RUN pip install -r requirements.txt

EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]