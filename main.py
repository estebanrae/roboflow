import requests
import json 
import os
from tqdm import tqdm
from inference_sdk import InferenceHTTPClient
from google_auth_oauthlib.flow import InstalledAppFlow
save_dir = "analog_pics"
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly', 
          'https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata']
id = "custom-workflow-single-label-classification-hihhv"
v = 4
roboflow_key = ""

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',  # Path to your downloaded file
    SCOPES
)
credentials = flow.run_local_server(port=0)
access_token = credentials.token
headers = {
    'Authorization': f'Bearer {access_token}',
    "Content-Type": "application/json"
}

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=roboflow_key
)

os.makedirs(save_dir, exist_ok=True)
analog_images_ids = []
nextPageToken = None
for i in tqdm(range(10)):
    url = f'https://photoslibrary.googleapis.com/v1/mediaItems?pageSize=20'
    if nextPageToken is not None:
       url += f"&pageToken={nextPageToken}" 
    response = requests.get(
        url,
        headers=headers
    )

    nextPageToken = response.json()["nextPageToken"]
    items = response.json()["mediaItems"]
    # Filter out videos
    items = [item for item in items if item["filename"].split('.')[1] != 'MOV']
    images_payload = [f"{item['baseUrl']}=w300-h300-c" for item in items]
    result = client.infer(images_payload, model_id=f"{id}/{v}")
    i = 0
    for r in result:
        item = items[i]
        if r["top"] == "analog" and r["confidence"] > 0.8:
            response = requests.get(f"{item['baseUrl']}=w300-h300")
            filepath = os.path.join(save_dir, item["filename"])
            with open(filepath, 'wb') as f:
                f.write(response.content)
        i += 1


