docker pull novicezk/midjourney-proxy:1.5.1

echo "SERVER_ID=${SERVER_ID}"
echo "CHANNEL_ID=${CHANNEL_ID}"
echo "USER_TOKEN=${USER_TOKEN}"
echo "BOT_TOKEN=${BOT_TOKEN}"


docker run -d \
 -p 8080:8080 \
 -e mj.discord.guild-id=${SERVER_ID} \
 -e mj.discord.channel-id=${CHANNEL_ID} \
 -e mj.discord.user-token=${USER_TOKEN} \
 -e mj.discord.bot-token=${BOT_TOKEN} \
 --restart=always \
 --name midjourney-proxy \
 novicezk/midjourney-proxy:1.5.1


echo "Waiting for midjourney-proxy container to start..."
sleep 5
echo "midjourney-proxy container started!"