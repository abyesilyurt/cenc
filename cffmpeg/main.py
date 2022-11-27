import sys
import time
import requests

DEBUG_ENDPOINT = "http://localhost:9000/ffmpeg"
ENDPOINT = "https://ffmpeg-kopg2w5bka-ez.a.run.app/ffmpeg"

def main():
    command = ["ffmpeg", *sys.argv[1:]]
    str_command = " ".join(command)
    task_id = create_task(str_command)
    if task_id is None:
        return
    track_progress(task_id)

def create_task(command : str):
    response = requests.post(ENDPOINT, params={"command": command})
    if response.status_code == 200:
        task_id = response.json()["id"]
        return task_id
    else:
        print("Error: ", response.text)
        return None

def track_progress(task_id):
    prev_log_length = 0
    while True:
        time.sleep(2)
        # Get the status of the task
        response = requests.get(f"{ENDPOINT}/{task_id}")
        if response.status_code != 200:
            continue
        data = response.json()
        if data is None:
            continue

        # Print the log
        if 'logs' in data and len(data['logs']) > prev_log_length:
            print(data['logs'][prev_log_length:], end='')
            prev_log_length = len(data['logs'])

        # Check if the task is done
        returncode = data.get("returncode")
        if returncode is not None:
            break
