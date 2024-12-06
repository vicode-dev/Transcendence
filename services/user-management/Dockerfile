FROM python:3.12-alpine

RUN adduser -D -h /app -s /bin/sh -u 1001 app
USER app
WORKDIR /app
EXPOSE 8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app ./app/ .

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]