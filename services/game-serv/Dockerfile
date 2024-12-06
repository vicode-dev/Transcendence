FROM python:3.12-alpine

RUN adduser -D -h /app -s /bin/sh -u 1001 app
USER app
WORKDIR /app
EXPOSE 8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app ./app/ .
# RUN echo "* * * * * python /app/manage.py clear_lobby >> /var/log/clear_lobby.log 2>&1" > /etc/crontabs/root
# RUN crond
# RUN git clone --depth=1 https://github.com/mrdoob/three.js.git
# EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]