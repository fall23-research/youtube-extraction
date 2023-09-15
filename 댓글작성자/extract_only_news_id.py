import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_category(video_id):
    API_KEY = os.getenv('API_KEY')

    # URL for the GET request
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
        # Parse the JSON response
            video_metadata = response.json()
            print(video_id, ": YouTube Category =", video_metadata['items'][0]['snippet']['categoryId']) # 25 is under News & Politics
            return video_metadata['items'][0]['snippet']['categoryId']
        except Exception as e:
            print("Category Unavailable") 
        
    else:
        print(f"Error: {response.status_code} - {response.text}")


# append video_id only with categoryId == 25
wf = open('comment_news_video_ids.txt', 'a') 

with open('comment_video_id.txt', 'r') as rf:
    # Read all lines from the file and store them in a list
    lines = rf.readlines()

for id in lines[5001:15001]:
    video_id = id.replace("\n", "")
    if get_category(video_id) != '25':
        continue
    else:
        wf.write(video_id)
        wf.write('\n')