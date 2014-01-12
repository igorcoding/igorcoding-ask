# coding=utf8

import json
import requests

data = {'value': 70}
json_data = json.dumps(data)
r = requests.post("http://127.0.0.1:8888/publish/?cid=progressbar", data=json_data)
print r.text