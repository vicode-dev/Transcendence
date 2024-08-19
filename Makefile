all:
# put webhook uri for alertmanager
	sed "s|{{DISCORD_WEBHOOK_URL}}|$(shell grep '^DISCORD_WEBHOOK_URL=' .env | cut -d '=' -f2-)|g" ./services/alertmanager/config.yml.default > ./services/alertmanager/config.yml
# launch docker
	docker compose up --build -d

clean:
	docker compose down

# fclean: clean
# 	docker system prune -af
# 	docker volume prune -f

re: fclean all

.PHONY: all clean fclean re