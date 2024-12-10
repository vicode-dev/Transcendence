NAME	= Transcendence

# Colors

YELLOW	= \033[1;33m
GREEN	= \033[1;32m
BLUE	= \033[0;36m
DEFAULT	= \033[0;0m

# Exec

# Macro for docker compose
DOCKER_COMPOSE	= docker compose
# To build one or more dockers
DOCKER_BUILD	= $(DOCKER_COMPOSE) build
# To launch and build dockers
DOCKER_RUN		= $(DOCKER_COMPOSE) up --detach --build
# To stop all dockers
DOCKER_STOP		= $(DOCKER_COMPOSE) down

# Main Rules

all: webhook 
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}${NAME} ${DEFAULT}..."
	$(DOCKER_RUN)

clean:
	@echo "${BLUE} [MAKE] ${DEFAULT}Shutting down ${YELLOW}${NAME} ${DEFAULT}..."
	$(DOCKER_STOP)

fclean: clean
	@echo "${BLUE} [MAKE] ${DEFAULT}Cleaning ${YELLOW}${NAME} ${DEFAULT}..."
	docker system prune -af
	docker volume prune -f

re: fclean all

webhook: # put webhook uri for alertmanager
	sed "s|{{DISCORD_WEBHOOK_URL}}|$(shell grep '^DISCORD_WEBHOOK_URL=' .env | cut -d '=' -f2-)|g" ./services/alertmanager/config.yml.default > ./services/alertmanager/config.yml

certificate: clean
	docker run -it -p 80:80 -v ./services/nginx/certificates:/etc/letsencrypt/archive --rm --name certbot certbot/certbot certonly --standalone -d $(shell grep '^DOMAIN_NAME=' .env | cut -d '=' -f2-)

# Specifics dockers

ai-bot:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}AI-Bot ${DEFAULT}..."
	${DOCKER_BUILD} ai-bot

alertmanager:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Alertmanager ${DEFAULT}..."
	${DOCKER_BUILD} alertmanager

authentication:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Authentication ${DEFAULT}..."
	${DOCKER_BUILD} authentication

blockchain:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Blockchain ${DEFAULT}..."
	${DOCKER_BUILD} blockchain

nginx:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Nginx ${DEFAULT}..."
	${DOCKER_BUILD} nginx

user-management:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}User Management ${DEFAULT}..."
	${DOCKER_BUILD} user-management


.PHONY: all clean fclean re certificate webhook \
	ai-bot alertmanager authentication blockchain \
	nginx user-management