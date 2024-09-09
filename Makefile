all:
# put webhook uri for alertmanager
	sed "s|{{DISCORD_WEBHOOK_URL}}|$(shell grep '^DISCORD_WEBHOOK_URL=' .env | cut -d '=' -f2-)|g" ./services/alertmanager/config.yml.default > ./services/alertmanager/config.yml
# launch docker
	docker compose up --build -d

clean:
	docker compose down

fclean: clean
	docker system prune -af
	docker volume prune -f

re: fclean all

certificate: clean
	docker run -it -p 80:80 -v ./services/nginx/certificates:/etc/letsencrypt/archive --rm --name certbot certbot/certbot certonly --standalone -d $(shell grep '^DOMAIN_NAME=' .env | cut -d '=' -f2-)

.PHONY: all clean fclean re certificate