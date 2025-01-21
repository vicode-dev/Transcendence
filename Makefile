NAME	= Transcendence
# Colors

YELLOW	= \033[1;33m
GREEN	= \033[1;32m
BLUE	= \033[0;36m
DEFAULT	= \033[0;0m
ENV_FILE=.env

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

all: check-env webhook images
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}${NAME} ${DEFAULT}..."
	@chmod 777 -R ./services/elasticsearch
	@$(DOCKER_RUN)

clean:
	@echo "${BLUE} [MAKE] ${DEFAULT}Shutting down ${YELLOW}${NAME} ${DEFAULT}..."
	$(DOCKER_STOP)

fclean:
	@echo "${BLUE} [MAKE] ${DEFAULT}Cleaning ${YELLOW}${NAME} ${DEFAULT}..."
	@docker compose down -v --rmi all

re: fclean all

webhook: # put webhook uri for alertmanager
	@sed "s|{{DISCORD_WEBHOOK_URL}}|$(shell grep '^DISCORD_WEBHOOK_URL=' .env | cut -d '=' -f2-)|g" ./services/alertmanager/config.yml.default > ./services/alertmanager/config.yml

certificate:
	@echo "[🔄] Generating certificate..."
	@docker compose down nginx
	@docker run -it -p 80:80 -v ./services/nginx/certificates:/etc/letsencrypt/archive --rm --name certbot certbot/certbot certonly --standalone -d $(shell grep '^DOMAIN_NAME=' .env | cut -d '=' -f2-)

check-env:
	@echo -n "[🔄] Checking .env file"
	@if [ -f $(ENV_FILE) ]; then \
		keys="POSTGRES_PASSWORD= ELASTIC_PASSWORD= DISCORD_WEBHOOK_URL= KIBANA_ENCRYPTION_KEY= DOMAIN_NAME= JWT_SECRET_KEY= SALT= KIBANA_PASSWD="; \
		for key in $$keys; do \
			if ! grep -q "^$$key" $(ENV_FILE); then \
				echo -e "\r[❌] Missing argument in .env file"; \
				exit 1; \
			fi; \
		done; \
		echo -e "\r[✅] .env complete"; \
	else \
		echo -e "\r[❌] .env file needed."; \
		exit 1; \
	fi;

test:
	@echo -n "This is the initial line. Waiting for replacement..."
	@sleep 2	
	@echo "\rThis is the replacement line.                       "
# Specifics dockers

ai-bot:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}AI-Bot ${DEFAULT}..."
	${DOCKER_RUN} ai-bot

alertmanager:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Alertmanager ${DEFAULT}..."
	${DOCKER_RUN} alertmanager

authentication:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Authentication ${DEFAULT}..."
	${DOCKER_RUN} authentication

blockchain:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Blockchain ${DEFAULT}..."
	${DOCKER_RUN} blockchain

nginx:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Nginx ${DEFAULT}..."
	${DOCKER_RUN} nginx

user-management:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}User Management ${DEFAULT}..."
	${DOCKER_RUN} user-management

game-serv:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Game Serv ${DEFAULT}..."
	${DOCKER_RUN} game-serv

adminer:
	@echo "${BLUE} [MAKE] ${DEFAULT}Building ${YELLOW}Adminer ${DEFAULT}..."
	${DOCKER_RUN} adminer

php-base:
	docker build -t php-base:sources ./images/php-base/.
	docker build -t php-base:7.4 ./images/php-7.4/.

images:
	docker build -t php-base:sources ./images/php-base/.
	docker build -t php-base:7.4 ./images/php-7.4/.
	docker build -t game-serv ./services/game-serv/.

migrations:
	# mkdir -p ./services/authentication/app/ft_auth/migrations
	# mkdir -p ./services/user-management/app/profile/migrations
	# mkdir -p ./services/game-serv/app/app/migrations

.PHONY: all clean fclean re certificate webhook \
	ai-bot alertmanager authentication blockchain \
	nginx user-management images
