Start an encoding task with passing the full ffmpeg command to the `cenc` command.

A trivial example that prints the version of ffmpeg on our system:

```bash
cenc ffmpeg --help
```

A more complex example that resizes a video file hosted on a remote server:

```bash
cenc ffmpeg -i 'https://storage.googleapis.com/kapan_public_videos/SampleVideo_1280x720_1mb%20(1).mp4' -vf scale=320:240 output.mp4
```

Task ID is returned immediately after the task is created. 
You can use the task ID to check the status of the task.
The logs will be printed to the standard output until the task is finished.

You can download the outputs of the task, after the task is finished.
The url for the each output file will be printed to the console, such as:

```
{
  "id": "b6c0d5607f224dc3b646068710d2e08a",
  "output.mp4": "https://storage.googleapis.com/store/tmp/ffmpeg/b6c0d5607f224dc3b646068710d2e08a/output.mp4",
  "returncode": "0",
  "status": "done"
}
```


## Using the API directly

The API is available at `https://ffmpeg-kopg2w5bka-ez.a.run.app`.
You can start a task by sending a POST request to the `/ffmpeg` endpoint with the full ffmpeg command in the params.

```python
endpoint = "https://ffmpeg-kopg2w5bka-ez.a.run.app"
command = "ffmpeg -i 'https://storage.googleapis.com/kapan_public_videos/SampleVideo_1280x720_1mb%20(1).mp4' -vf scale=320:240 output.mp4"
response = requests.post(endpoint, params={"command": command})
task_id = response.json()["id"]
```

You can check the status of the task by sending a GET request to the `/ffmpeg/<task_id>` endpoint.

```python
while True:
    time.sleep(2)
    response = requests.get(f"{endpoint}/ffmpeg/{task_id}")
    if response.status_code != 200:
        # Task has not been started processing yet
        continue
    
    results = response.json()

    if results.get("returncode"):
        # Task has finished processing
        print(results)
        break
```