import os 
USER_TOKEN = os.environ.get('USER_TOKEN')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SERVER_ID = os.environ.get('SERVER_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
PROXY_URL = os.environ.get('PROXY_URL')
PORT = os.environ.get('PORT')


assert USER_TOKEN is not None, "USER_TOKEN is not set"
assert BOT_TOKEN is not None, "BOT_TOKEN is not set"
assert SERVER_ID is not None, "SERVER_ID is not set"
assert CHANNEL_ID is not None, "CHANNEL_ID is not set"
assert PROXY_URL is not None, "PROXY_URL is not set"

print("USER TOKEN: ", USER_TOKEN)
print("BOT TOKEN: ", BOT_TOKEN)
print("SERVER ID: ", SERVER_ID)
print("CHANNEL ID: ", CHANNEL_ID)
print("PROXY URL: ", PROXY_URL)
print("PORT: ", PORT)
print("SANITY CHECK LINK: ", f"https://discord.com/channels/{SERVER_ID}/{CHANNEL_ID}")
