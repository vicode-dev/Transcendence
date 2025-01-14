FROM python:3.12-alpine

RUN adduser -D -h /app -s /bin/sh -u 1001 app
WORKDIR /app
EXPOSE 8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# USER app
COPY --chown=app:app ./app/ .
RUN mkdir -p /app/app/migrations

CMD ["./entrypoint.sh"]
