from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import csv
from concurrent.futures import ThreadPoolExecutor

MAX_CELL_SIZE = 32767

def get_youtube_url(file_path, url_column):
    video_urls = set()      # Store unique YouTube video URLs

    try:
        with open(file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                video_url = row[url_column]
                video_urls.add(video_url)

    except FileNotFoundError:
        print(f"The CSV file '{file_path}' was not found.")
    except KeyError:
        print(f"The specified column '{url_column}' was not found in the CSV file.")

    unique_video_urls = list(video_urls)

    return unique_video_urls

def get_youtube_video_info(video_url):
    # 옵션 지정
    ydl_opts = {          
        'quiet': True,                    # suppresses output messages
        'no_warnings': True,
        'extract_flat': True,               # gets only basic information about the video
        'force_generic_extractor': True     # speeds up the process a bit but may cause issues in rare cases
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)    # 비디오 정보 추출
            channel = video_info['channel']                             # 비디오 정보에서 채널이름 추출
            channel_id = video_info['channel_id']                       # 비디오 정보에서 채널 ID 추출
            video_id = video_info['id']                                 # 비디오 정보에서 비디오 ID 추출
            title = video_info['title']
            timestamp = video_info['release_timestamp']

            return channel, channel_id, video_id, title, timestamp
    except:
        return None, None, None, None, None

def is_official_news_channel(channel_id):
    # official_news_channel_names = ['YTN', 'SBS 뉴스', 'MBCNEWS', 'JTBC News', 'KBS News', '채널A 뉴스', 'MBN News', '뉴스TVCHOSUN', '연합뉴스TV']
    official_news_channel_ids = ['UChlgI3UHCOnwUGzWzbJ3H5w', 'UCkinYTS9IHqOEwR1Sze2JTw', 'UCF4Wxdo3inmxP-Y59wXDsFw', 'UCsU-I-vHLiaMfV_ceaYz5rQ', 'UCcQTRi69dsVYHN3exePtZ1A', 'UCfq4V1DAuaojnr2ryvWNysw', 'UCG9aFJTZ-lMCHAiO1KJsirg', 'UCWlV3Lz_55UaX4JsMj-z__Q', 'UCTHCOPwqNfZ0uiKOvFyhGwg']
    return channel_id in official_news_channel_ids

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        text = " ".join([line["text"] for line in transcript])
    except:
        text = '해당 영상은 자막을 제공하지 않습니다.'
    return text

def fetch_info_and_transcript(video_url):
    channel, channel_id, video_id, title, timestamp = get_youtube_video_info(video_url)
    if channel is None or channel_id is None or video_id is None:
        return None, None, None, None, None
    
    if is_official_news_channel(channel_id):
        transcript_text = get_video_transcript(video_id)
        return video_id, channel_id, transcript_text, title, timestamp
    return None, None, None, None, None

def main():
    # Extract Youtube Video URLs from the csv file
    csv_file_path = "/Users/siwon/Desktop/Fall-23/research/Datasets/hashtag_youtube_dataset.csv"    
    youtube_url_column = '해시태그영상ID'
    youtube_urls = get_youtube_url(csv_file_path, youtube_url_column)

    data_to_write = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_info_and_transcript, youtube_urls))
        print(results)
        for video_id, channel, transcript_text in results:
            if video_id:
                data_to_write.append((video_id, channel, transcript_text))

    for idx, (video_id, channel_id, transcript_text, title, timestamp) in enumerate(data_to_write, start=1):
        print(idx, video_id, channel_id, transcript_text, title, timestamp)

if __name__ == "__main__":
    main()
