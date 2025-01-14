FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

RUN mkdir /app/ft_auth/migrations

CMD ["./entrypoint.sh"]
