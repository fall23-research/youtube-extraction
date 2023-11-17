import sqlite3
import yt_dlp

def get_youtube_video_info(video_url):
    ydl_opts = {          
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'force_generic_extractor': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            view_count = video_info.get('view_count', None)
            like_count = video_info.get('like_count', None)
            comment_count = video_info.get('comment_count', None)
            timestamp = video_info.get('upload_date', None)

            print(like_count, view_count, comment_count, timestamp)
            return like_count, view_count, comment_count, timestamp
    except Exception as e:
        print(f"Error in get_youtube_video_info: {e}")
        return None, None, None, None


table_name = "news_video"
db_path = "/Users/siwon/Desktop/Fall-23/research/official_news_dataset/covid_news_data.sqlite"

conn_existing = sqlite3.connect(db_path)
cursor_existing = conn_existing.cursor()

cursor_existing.execute(f'SELECT video_id FROM {table_name}')
video_ids = cursor_existing.fetchall()

for video_id in video_ids[5:]:
    like_count, view_count, comment_count, timestamp = get_youtube_video_info(f"https://www.youtube.com/watch?v={video_id[0]}")
    
    # video_id[0]로 수정하여 튜플에서 video_id를 추출
    update_query = f"UPDATE {table_name} SET like_count = ?, view_count = ?, comment_count = ?, upload_date = ? WHERE video_id = ?;"
    cursor_existing.execute(update_query, (like_count, view_count, comment_count, timestamp, video_id[0]))

conn_existing.commit()
conn_existing.close()
