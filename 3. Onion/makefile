all:
	@sudo docker-compose up --build

onionaddr:
	@sudo docker exec -it 3onion_web_1 /bin/bash -c "cat /var/lib/tor/hidden_service/hostname"

ipaddr:
	@sudo docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 3onion_web_1

fclean:
	@sudo rm -rf data

clean:
	@sudo docker stop $$(sudo docker ps -qa);\
	 sudo docker rm $$(sudo docker ps -qa);\
	 sudo docker rmi $$(sudo docker images -qa);\
	 sudo docker volume rm $$(sudo docker volume ls -q);\
	 sudo docker network rm $$(sudo docker network ls -q)

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