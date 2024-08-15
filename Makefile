all:
	docker compose up --build -d

clean:
	docker compose down

# fclean: clean
# 	docker system prune -af
# 	docker volume prune -f

re: fclean all

.PHONY: all clean fclean re