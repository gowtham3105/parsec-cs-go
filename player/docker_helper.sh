# Description: Run docker container for player

# check if 1 arg is passed
if [ $# -eq 1 ]; then
  # if first argument is "build" then build the docker image
  if [ "$1" = "build" ]; then
    # stop and remove the docker containers
    docker compose stop web-red
    docker compose stop web-blue
    docker compose rm web-red -f
    docker compose rm web-blue -f

    # build docker image
    docker compose build --pull --no-cache

  # if first argument is "delete" then delete the docker container
  elif [ "$1" = "delete" ]; then
    # if docker container is present then delete it
    docker compose stop web-red
    docker compose stop web-blue
    docker compose rm web-red -f
    docker compose rm web-blue -f
  else
    echo "Invalid arguments"
    echo "Usage: ./docker_helper.sh <build|start|stop|logs|delete> <player_name>"
  fi
fi

if [ $# -eq 2 ]; then
  if [ "$1" = "start" ]; then
    docker compose up web-"$2" -d
  elif [ "$1" = "stop" ]; then
    docker compose stop web-"$2"
  elif [ "$1" = "logs" ]; then
    docker compose logs web-"$2"
  else
    echo "Invalid arguments"
    echo "Usage: ./docker_helper.sh <build|start|stop|logs|delete> <player_name>"
  fi

fi

# if more than 2 arguments are passed
if [ $# -gt 2 ]; then
  echo "Invalid arguments"
  echo "Usage: ./docker_helper.sh <build|start|stop|logs|delete> <player_name>"
fi
