FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

RUN mkdir -p /app/ft_auth/migrations && touch ft_auth/migrations/__init__.py

CMD ["./entrypoint.sh"]
