import requests

url = "http://localhost:5678/webhook-test/analyze-audio"
data = {"track_path": "audio/Great Spirit.flac"}

res = requests.post(url, json=data)
print("Status Code:", res.status_code)
print("Response:", res.text)
