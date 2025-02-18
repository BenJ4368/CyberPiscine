all:
	@echo "Building inquisitor docker..."
	@docker build -t inquisitor .
	@docker run -it inquisitor /bin/bash

term:
	@docker run -it inquisitor /bin/bash

clean:
	@docker stop $$(docker ps -qa);\
	 docker rm $$(docker ps -qa);\
	 docker rmi $$(docker images -qa);\
	 docker volume rm $$(docker volume ls -q);\
	 docker network rm $$(docker network ls -q)

list:
	@echo "======== CONTAINERS"
	@docker ps -a
	@echo "======== IMAGES"
	@docker images -a
	@echo "======== VOLUMES"
	@docker volume ls
	@echo "======== NETWORKS"
	@docker network ls

.PHONY: all down clean list