
all:
	@echo "Building inquisitor containers..."
	sudo docker-compose up --build

term:
	@sudo docker exec -it inquisitor /bin/bash

clean:
	@sudo docker stop $$(sudo docker ps -qa);\
	 sudo docker rm $$(sudo docker ps -qa);\
	 sudo docker rmi $$(sudo docker images -qa);\
	 sudo docker volume rm $$(sudo docker volume ls -q);\
	 sudo docker network rm $$(sudo docker network ls -q)

fclean:
	@sudo rm -rf client/uploads/*
	@sudo rm -rf server/*
	@make clean

info:
	@echo "=== ftp-client ==="
	@echo "IP : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-client)"
	@echo "MAC : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-client)"
	@echo ""
	@echo "=== ftp-server ==="
	@echo "IP : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ftp-server)"
	@echo "MAC : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' ftp-server)"
	@echo ""
	@echo "=== inquisitor ==="
	@echo "IP : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inquisitor)"
	@echo "MAC : $(shell sudo docker inspect --format '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' inquisitor)"

list:
	@echo "======== CONTAINERS"
	@sudo docker ps -a
	@echo "======== IMAGES"
	@sudo docker images -a
	@echo "======== VOLUMES"
	@sudo docker volume ls
	@echo "======== NETWORKS"
	@sudo docker network ls

.PHONY: all down clean list