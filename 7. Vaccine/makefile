
all:
	@docker pull bkimminich/juice-shop:latest
	@docker run -p 3000:3000 --name juice-shop bkimminich/juice-shop:latest

clean:
	@docker stop $$(docker ps -qa);\
	 docker rm $$(docker ps -qa); \
	 docker volume rm $$(docker volume ls -q);\
	 docker network rm $$(docker network ls -q)

iclean:
	@docker rmi $$(docker images -q);

list:
	@echo "======== CONTAINERS"
	@docker ps -a
	@echo "======== IMAGES"
	@docker images -a
	@echo "======== VOLUMES"
	@docker volume ls
	@echo "======== NETWORKS"
	@docker network ls

.PHONY: all down clean list client attacker