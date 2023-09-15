import requests
import os
from dotenv import load_dotenv
load_dotenv()

# YouTube video ID for which you want to retrieve captions
video_id = 'QfzWF2Od7xY'

API_KEY = os.getenv('API_KEY')

# URL for the GET request
url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'

# Make the GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    video_metadata = response.json()
    print("YouTube Category: ", video_metadata['items'][0]['snippet']['categoryId']) # 25 is under News & Politics
    
else:
    print(f"Error: {response.status_code} - {response.text}")
