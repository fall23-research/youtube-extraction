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
            video_metadata = response.json()['items'][0]['snippet']

            # check if the content is related to COVID-19
            title = video_metadata['title'] 
            description = video_metadata['description']
            print(title, description)
            if contains_covid_keyword(title):
                return True
            if contains_covid_keyword(description):
                return True
            
        except Exception as e:
            print("News Channel Unavailable") 
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

# append video_id only with categoryId == 25
wf = open('commenter_covid_video_ids_test.txt', 'a') 

with open('commenter_video_id.txt', 'r') as rf:
    # Read all lines from the file and store them in a list
    lines = rf.readlines()

video_id = "GFqBkyGOSxE"
if get_channelId(video_id):
    wf.write(video_id)
    wf.write('\n')