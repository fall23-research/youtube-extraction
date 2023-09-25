import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_channelId(video_id):
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
            channelId = video_metadata['items'][0]['snippet']['channelId']
            print(video_id, ": YouTube Channel ID =", channelId)
            return channelId
        except Exception as e:
            print("News Channel Unavailable") 
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

official_news_channel_ids = ['UChlgI3UHCOnwUGzWzbJ3H5w', 'UCkinYTS9IHqOEwR1Sze2JTw', 'UCF4Wxdo3inmxP-Y59wXDsFw', 'UCsU-I-vHLiaMfV_ceaYz5rQ', 'UCcQTRi69dsVYHN3exePtZ1A', 'UCfq4V1DAuaojnr2ryvWNysw', 'UCG9aFJTZ-lMCHAiO1KJsirg', 'UCWlV3Lz_55UaX4JsMj-z__Q', 'UCTHCOPwqNfZ0uiKOvFyhGwg']

# append video_id only with categoryId == 25
wf = open('commenter_news_video_ids.txt', 'a') 

with open('commenter_video_id.txt', 'r') as rf:
    # Read all lines from the file and store them in a list
    lines = rf.readlines()

for id in lines[0:10000]:
    video_id = id.replace("\n", "")
    if get_channelId(video_id) in official_news_channel_ids:
        wf.write(video_id)
        wf.write('\n')
    else:
        continue