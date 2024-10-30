import requests
import json
deeplx_api = "http://127.0.0.1:1188/translate"

data = {
	"text": "Hello World"
}
post_data = json.dumps(data)
a = requests.post(deeplx_api, post_data)
print(a.text)