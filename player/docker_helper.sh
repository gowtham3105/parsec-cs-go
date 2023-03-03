# Description: Run docker container for player

# check if 1 arg is passed

if [ $# -eq 1 ]; then
  # if first argument is "build" then build the docker image
  if [ "$1" = "build" ]; then
    # if docker image is present then delete it
    if [ "$(docker images -q player 2>/dev/null)" != "" ]; then
      echo "-> Deleting the existing docker image.."
      docker rmi player
    fi

    # build docker image
    docker build -t player .

    exit 0
  fi

  # if first argument is "delete" then delete the docker container
  if [ "$1" = "delete" ]; then
    # if docker container is present then delete it
    if [ "$(docker ps -q -f name=player 2>/dev/null)" != "" ]; then
      echo "-> Deleting the existing docker container.."
      docker rm player
    fi

    exit 0
  fi
fi

if [ $# -eq 2 ]; then
  if [ "$1" = "run" ]; then
    # run docker container
    docker run -it player -e PLAYER_TEAM=$2 -p 9000:9000 -p 9001:9001

    exit 0
  fi
fi

echo "Invalid arguments"
echo "Usage: ./docker_helper.sh <build|run|delete> <player_name>"
