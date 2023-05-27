echo "Stopping midjourney-proxy container..."
echo "DOCKER_NAME=${DOCKER_NAME}"
docker rm -f ${DOCKER_NAME}