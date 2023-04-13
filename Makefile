.DEFAULT_GOAL := up

up:
	docker-compose -f ./docker/docker-compose.yml up -d

restart:
	docker-compose -f ./docker/docker-compose.yml restart

down:
	docker-compose -f ./docker/docker-compose.yml down -v