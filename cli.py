# 1110427330981146627/1110477862303186976
USER_TOKEN = "NDQ2NzEzMDYyNjA3NTUyNTEy.GnP6vN.aVuYNvBc0zFeovNl_ScSzDkZ7W8bDoU00_OVz8"
BOT_TOKEN = "MTEwODM0MjM5ODI4MDU1MjQ4OA.G7J-TW.YNv1rF4YMZwbA0bIZkim5Y2P6JwQ8p7R-5TUeE"
SERVER_ID = "1110427330981146627"

CHANNEL_IDS = {
    "test": "1112062466529181827",
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
    "202001": None,
    "202002": None,
    "202003": None,
    "202004": None,
    "202005": None,
    "202006": None,
}
PORT = "8080"
PROXY_URL = f"http://localhost:{PORT}/mj"

from argparse import ArgumentParser
import subprocess
import os 
import time

def run_process(cmd, env_vars):
    process = subprocess.Popen(cmd, env=env_vars)
    process.wait()
    print("=====================================")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--command", type=str, required=True)
    parser.add_argument("--channel", type=str, default="test")
    args = parser.parse_args()

    CHANNEL_ID = CHANNEL_IDS[args.channel]

    assert CHANNEL_ID is not None, "Channel ID is not set"

    env_vars = {
        "USER_TOKEN": USER_TOKEN,
        "BOT_TOKEN": BOT_TOKEN,
        "SERVER_ID": SERVER_ID,
        "CHANNEL_ID": CHANNEL_ID,
        "PROXY_URL": PROXY_URL,
        "PORT": PORT,
    }
    env_vars.update(os.environ)

    command = args.command.split(" ")
    start_docker_cmd = ["sh", "start_docker.sh"]
    stop_docker_cmd = ["sh", "stop_docker.sh"]
    
    run_process(stop_docker_cmd, env_vars)
    run_process(start_docker_cmd, env_vars)
    run_process(command, env_vars)
    run_process(stop_docker_cmd, env_vars)


    
    