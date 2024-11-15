import requests

url = "http://127.0.0.1:8000/api/query"
data = {
    "doc_id": "c22ce54a93cdb9a2371cfe6224e6a65b",
    "question": "what are the main points  which raise questions",
    "context": "None"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.json()}")