import requests
import os
from dotenv import load_dotenv
load_dotenv()

def contains_covid_keyword(input_string):
    covid_keywords = ['코로나', '코로나19', 'corona', '코로나 바이러스', 'COVID-19', 'covid-19', 'covid19', 'COVID19', 'covid 19', 'COVID', 'coronavirus', 'covid', '팬데믹', 'pandemic']
    for keyword in covid_keywords:
        if keyword in input_string:
            return True
    return False

official_news_channel_ids = ['UChlgI3UHCOnwUGzWzbJ3H5w', 'UCkinYTS9IHqOEwR1Sze2JTw', 'UCF4Wxdo3inmxP-Y59wXDsFw', 'UCsU-I-vHLiaMfV_ceaYz5rQ', 'UCcQTRi69dsVYHN3exePtZ1A', 'UCfq4V1DAuaojnr2ryvWNysw', 'UCG9aFJTZ-lMCHAiO1KJsirg', 'UCWlV3Lz_55UaX4JsMj-z__Q', 'UCTHCOPwqNfZ0uiKOvFyhGwg']

def get_covid_news_video_id(video_id):
    API_KEY = os.getenv('API_KEY')

    # URL for the GET request
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
        # Parse the JSON response
            video_raw_metadata = response.json()
            video_metadata = video_raw_metadata['items'][0]['snippet']

            # check if the video issued by the official channel
            channelId = video_metadata['channelId']
            print(video_id, end=" ")

            if channelId in official_news_channel_ids:
                print("- Official Channel", end=" ")

                # check if the content is related to COVID-19
                title = video_metadata['title'] 
                description = video_metadata['description']

                if contains_covid_keyword(title):
                    return video_id
                if contains_covid_keyword(description):
                    return video_id
            else:
                return False
        except Exception as e:
            print("READ Operation Error: ", e) 
        
    else:
        print(f"Error: {response.status_code} - {response.text}")


wf = open('commenter_covid_video_ids.txt', 'a') 

with open('commenter_video_id.txt', 'r') as rf:
    # Read all lines from the file and store them in a list
    lines = rf.readlines()

for id in lines[30000:]:
    video_id = id.replace("\n", "")
    if get_covid_news_video_id(video_id):
        print("COVID topic found")
        wf.write(video_id)
        wf.write('\n')
    else:
        continue