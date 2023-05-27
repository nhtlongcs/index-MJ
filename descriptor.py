import requests
import base64
import json
from pathlib import Path
import os 
import asyncio

from config import USER_TOKEN, BOT_TOKEN, SERVER_ID, CHANNEL_ID, PROXY_URL

MESSAGE_LIMIT = 5

def describe_image(img_path: str) -> str:
    """
    Function to describe an image given image path
    Args:
        img_path (str): path to the image

    Returns:
        str: id of the describe task
    """
    headers = {
        'Content-type': 'application/json'
    }

    with open(img_path, 'rb') as file:
        image_data = file.read()

    # Convert image data to base64
    base64_data = base64.b64encode(image_data).decode('utf-8')
    payload = {
        "base64": f"data:image/png;base64,{base64_data}"
    }

    return requests.post(f"{PROXY_URL}/trigger/describe", json=payload, headers=headers).json()["result"]


def get_task_status(task_id: str) -> requests.Response:
    """
    Function to show task status base on task_id (returned by others midjourney proxy request)
    Args:
        task_id (str): id of the task

    Returns:
        requests.Response: response contain task status and task information
    """
    return requests.get(f"{PROXY_URL}/task/{task_id}/fetch")



def retrieve_messages():
    headers = {'authorization' : USER_TOKEN}
    r = requests.get(
        f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit={MESSAGE_LIMIT}', headers=headers)
    jsonn = json.loads(r.text)
    return jsonn


def collecting_results():
    """
    collecting describe result in print it out
    """
    results = []
    message_list = retrieve_messages()
    for message in message_list:
        if not message.get('interaction'):
            continue
        if message['author']['username'] == 'Midjourney Bot'  and message['interaction']['name'] == 'describe':
            description = message['embeds'][0]['description']
            img_url = message['embeds'][0]['image']['url']
            results.append((img_url, description))
            # print(img_url)
            # print(description)
    return results

def get_image(path: str):
    # if path is a url
    if path.startswith('http'):
        response = requests.get(path).content
        return response
    path = Path(path)
    if path.is_file():
        with open(path, 'rb') as file:
            return file.read()
    assert False, 'invalid path provided'

def check_image_hash(image1_path, image2_path):
    """
    check if the image is already in the server
    """
    image1 = get_image(image1_path)
    image2 = get_image(image2_path)
    return hash(image1) == hash(image2)

async def describe_image_async(img_path: str) -> str:
    """
    Function to describe an image given image path
    Args:
        img_path (str): path to the image

    Returns:
        str: id of the describe task
    """
    task_id = describe_image(img_path)
    assert task_id is not None, "task_id is returned None"
    print(f"task_id: {task_id}")
    delay = 1
    while True:
        await asyncio.sleep(delay)
        response = get_task_status(task_id).json()
        try: 
            msgs = collecting_results()
            msg = msgs[0]
            image_url = msg[0]
            description = msg[1]
        except Exception as e:
            await asyncio.sleep(1)
            continue
        plain_text = image_url + '\n' + description
        # assert check_image_hash(img_path, image_url), "image is not the same"
        return plain_text
        
    
if __name__ == "__main__":
    asyncio.run(describe_image_async('test3.jpg'))