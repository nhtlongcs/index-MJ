# 1110427330981146627/1110477862303186976
USER_TOKEN = "NDQ2NzEzMDYyNjA3NTUyNTEy.GnP6vN.aVuYNvBc0zFeovNl_ScSzDkZ7W8bDoU00_OVz8"
BOT_TOKEN = "MTEwODM0MjM5ODI4MDU1MjQ4OA.G7J-TW.YNv1rF4YMZwbA0bIZkim5Y2P6JwQ8p7R-5TUeE"
SERVER_ID = "1110427330981146627"

CHANNEL_IDS = {
    "test": "1112062466529181827",
    "test2": "1112080990446309377",
    "201901": None,
    "201902": None,
    "201903": None,
    "201904": None,
    "201905": None,
    "201906": None,
    "201907": None,
    "201908": None,
    "201909": None,
    "201910": None,
    "201911": None,
    "201912": None,
    "202001": "1112092424060289024",
    "202002": "1110427400220721212",
    "202003": None,
    "202004": None,
    "202005": None,
    "202006": None,
}
from argparse import ArgumentParser
import subprocess
import os 
import time

def run_process(cmd, env_vars):
    print("=====================================")
    process = subprocess.Popen(cmd, env=env_vars)
    process.wait()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--command", type=str, required=True)
    parser.add_argument("--channel", type=str, default="test")
    parser.add_argument("--docker", type=str, default="midjourney-proxy", help="Docker container name")
    parser.add_argument("--port", type=str, default="8080", help="Port number")
    args = parser.parse_args()

    CHANNEL_ID = CHANNEL_IDS[args.channel]

    assert CHANNEL_ID is not None, "Channel ID is not set"

    PORT = args.port
    PROXY_URL = f"http://localhost:{PORT}/mj"

    env_vars = {
        "USER_TOKEN": USER_TOKEN,
        "BOT_TOKEN": BOT_TOKEN,
        "SERVER_ID": SERVER_ID,
        "CHANNEL_ID": CHANNEL_ID,
        "PROXY_URL": PROXY_URL,
        "PORT": PORT,
        "DOCKER_NAME": args.docker,
    }
    env_vars.update(os.environ)

    command = args.command.split(" ")
    start_docker_cmd = ["sh", "start_docker.sh"]
    stop_docker_cmd = ["sh", "stop_docker.sh"]
    
    try:
        run_process(start_docker_cmd, env_vars)
        run_process(command, env_vars)
    except KeyboardInterrupt:
        pass
    run_process(stop_docker_cmd, env_vars)


    
    