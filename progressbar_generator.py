import json
import requests
import time

GENERATION_DELAY = 2


def main():
    target_url = "http://127.0.0.1:8888/publish/?cid=progressbar"
    data = {'value': 0}
    direction = +1

    while True:
        r = requests.post(target_url, data=json.dumps(data))
        if data['value'] >= 100:
            direction = -1
        elif data['value'] <= 0:
             direction = +1
        data['value'] += direction
        time.sleep(GENERATION_DELAY)

if __name__ == "__main__":
    main()