export SERVER_ID=1110427330981146627
export CHANNEL_ID=1112062466529181827
export USER_TOKEN=NDQ2NzEzMDYyNjA3NTUyNTEy.GnP6vN.aVuYNvBc0zFeovNl_ScSzDkZ7W8bDoU00_OVz8
export BOT_TOKEN=MTEwODM0MjM5ODI4MDU1MjQ4OA.Glt6jr.Smxvx25DVIkN5QbMr1DCveq5PlWKSg1Bkgp21s
export DOCKER_NAME=mj1
export PORT=8080
export PROXY_URL=http://localhost:${PORT}/mj

docker rm -f ${DOCKER_NAME}

echo "SERVER_ID=${SERVER_ID}"
echo "CHANNEL_ID=${CHANNEL_ID}"
echo "USER_TOKEN=${USER_TOKEN}"
echo "BOT_TOKEN=${BOT_TOKEN}"
echo "DOCKER_NAME=${DOCKER_NAME}"
echo "PORT=${PORT}"

docker run -d \
 -p ${PORT}:8080 \
 -e mj.discord.guild-id=${SERVER_ID} \
 -e mj.discord.channel-id=${CHANNEL_ID} \
 -e mj.discord.user-token=${USER_TOKEN} \
 -e mj.discord.bot-token=${BOT_TOKEN} \
 --restart=always \
 --name ${DOCKER_NAME} \
 novicezk/midjourney-proxy:1.5.1


echo "Waiting for midjourney-proxy container to start..."
sleep 10
echo "midjourney-proxy container started!"


python descriptor.py