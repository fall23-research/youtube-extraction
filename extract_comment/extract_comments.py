import requests
import os
from dotenv import load_dotenv
load_dotenv()

from manage_CommentsDB import *
from manage_NewsDB import get_video_ids

API_KEY = os.getenv('API_KEY')

MAX_COUNT_PER_PAGE = 100
comment_data_list = []

def collect_comments(video_id):
    # Initialize variables
    next_page_token = None
    page_counter = 0
    order = 'relevance'

    while True:
        # URL for the GET request
        url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&order={order}&maxResults={MAX_COUNT_PER_PAGE}&key={API_KEY}'

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

                comments_metadata = result['items']
                for comment in comments_metadata:
                    comment_id = comment['id']
                    comment_detail = comment['snippet']['topLevelComment']['snippet']
                    text_display = comment_detail['textDisplay']
                    author_name = comment_detail['authorDisplayName']
                    author_channel_url = comment_detail['authorChannelUrl']
                    like_count = comment_detail['likeCount']
                    published_at = comment_detail['publishedAt']
                    total_reply_count = comment['snippet']['totalReplyCount']

                    metadata = { 
                        'comment_id': comment_id,
                        'video_id': video_id, 
                        'text_display': text_display,
                        'author_name': author_name,
                        'author_channel_url': author_channel_url,
                        'like_count': like_count,
                        'published_at': published_at,
                        'total_reply_count': total_reply_count,
                    }
                    comment_data_list.append(metadata)

                # Check if there are more pages
                next_page_token = result.get('nextPageToken')
                page_counter += 1

                # Break the loop if there are no more pages
                if not next_page_token:
                    print(page_counter, "pages!!")
                    break

            except Exception as e:
                print("API error: ", e) 
            
        else:
            print(f"Error: {response.status_code} - {response.text}")

def main():
    video_ids = get_video_ids()
    for video_id in video_ids[3000:]:
        collect_comments(video_id)
        insert_news_comment_batch_metadata(comment_data_list)
        print("Completed!", len(comment_data_list))
        comment_data_list.clear()

if __name__ == "__main__":
    main()