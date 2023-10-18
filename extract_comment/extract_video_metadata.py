import requests
import os
from dotenv import load_dotenv
load_dotenv()

from manage_NewsDB import *

official_news_channel_names = ['YTN', 'SBS 뉴스', 'MBCNEWS', 'JTBC News', 'KBS News', '채널A 뉴스', 'MBN News', '뉴스TVCHOSUN', '연합뉴스TV']
official_news_channel_ids = ['UChlgI3UHCOnwUGzWzbJ3H5w', 'UCkinYTS9IHqOEwR1Sze2JTw', 'UCF4Wxdo3inmxP-Y59wXDsFw', 'UCsU-I-vHLiaMfV_ceaYz5rQ', 'UCcQTRi69dsVYHN3exePtZ1A', 'UCfq4V1DAuaojnr2ryvWNysw', 'UCG9aFJTZ-lMCHAiO1KJsirg', 'UCWlV3Lz_55UaX4JsMj-z__Q', 'UCTHCOPwqNfZ0uiKOvFyhGwg']


API_KEY = os.getenv('API_KEY')

query = '코로나'
MAX_COUNT_PER_PAGE = 50
video_data_list = []

def collect_video_metadata(channel_id, channel_name):
    # Initialize variables
    next_page_token = None
    page_counter = 0

    while True:
        # URL for the GET request
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&q={query}&order=viewCount&maxResults={MAX_COUNT_PER_PAGE}&key={API_KEY}'

        # Include the nextPageToken if available
        if next_page_token:
            url += f'&pageToken={next_page_token}'

        # Make the API request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            try:
            # Parse the JSON response
                result = response.json()

                video_metadata = result['items']
                for video in video_metadata:
                    video_id = video['id']['videoId']
                    title = video['snippet']['title']
                    published_at = video['snippet']['publishedAt']
                    metadata = { 
                        'video_id': video_id, 
                        'channel_id': channel_id, 
                        'channel_name': channel_name,
                        'title': title, 
                        'published_at': published_at
                    }
                    video_data_list.append(metadata)

                # Check if there are more pages
                next_page_token = result.get('nextPageToken')
                page_counter += 1

                # Break the loop if there are no more pages
                if not next_page_token:
                    print(page_counter, "no pages!!")
                    break

            except Exception as e:
                print("API error: ", e) 
            
        else:
            print(f"Error: {response.status_code} - {response.text}")

collect_video_metadata(official_news_channel_ids[8], official_news_channel_names[8]) # 0-8

insert_news_video_batch_metadata(video_data_list)

