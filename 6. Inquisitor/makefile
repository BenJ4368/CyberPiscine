
all:
	@echo "Building inquisitor containers..."
	docker-compose up --build

attacker:
	@docker exec -it attacker /bin/bash
client:
	@docker exec -it client /bin/bash

clean:
	@docker stop $$(docker ps -qa);\
	 docker rm $$(docker ps -qa); \
	 docker volume rm $$(docker volume ls -q);\
	 docker network rm $$(docker network ls -q)

info:
	@echo "serverIP attackerMAC clientIP clientMAC"
	@echo "$(shell docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server) \
	$(shell docker inspect --format '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' attacker) \
	$(shell docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client) \
	$(shell docker inspect --format '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' client)"

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