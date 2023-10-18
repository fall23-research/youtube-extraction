import sqlite3
from extract_video_transcript import *

database = sqlite3.connect("news_video.sqlite")
databaseCursor = database.cursor()


# databaseCursor.execute('''CREATE TABLE IF NOT EXISTS news_video(
#                             id INTEGER PRIMARY KEY ASC,
#                             video_id TEXT, 
#                             channel_id TEXT,
#                             channel_name TEXT,
#                             title TEXT, 
#                             published_at TEXT,
#                             transcript TEXT
#                             )''')
# database.commit()


def execute_batch(query, data):
    """
    일괄 삽입을 위한 도우미 함수
    """
    databaseCursor.executemany(query, data)


def insert_news_video_batch_metadata(video_data_list):
    """
    여러 비디오 데이터를 일괄로 DB에 삽입
    """
    print('db executed')
    
    query = '''INSERT INTO news_video(video_id, channel_id, channel_name, title, published_at)
                VALUES (?, ?, ?, ?, ?)'''

    # 리스트 내 각 항목이 딕셔너리인지 확인하고 데이터 추출
    data = [(video.get('video_id', ''), video.get('channel_id', ''), video.get('channel_name', ''),
                video.get('title', ''), video.get('published_at', ''))
            for video in video_data_list]

    execute_batch(query, data)
    database.commit()


def insert_batch_transcript():
    """
    여러 비디오 데이터를 일괄로 DB에 삽입
    """
    databaseCursor.execute("SELECT video_id FROM news_video_video")
    video_ids = [row[0] for row in databaseCursor.fetchall()]

    for video_id in video_ids[15:]:
        # YouTube Transcript API를 사용하여 트랜스크립트 추출
        transcript = process_transcript_extraction(video_id)

        # 추출한 트랜스크립트를 데이터베이스에 업데이트
        databaseCursor.execute("UPDATE news_video SET transcript = ? WHERE video_id = ?", (transcript, video_id))
        database.commit()
        print(f"Transcript updated for video_id: {video_id}")


def get_video_ids():
    databaseCursor.execute('''SELECT video_id FROM news_video''')
    rows = databaseCursor.fetchall()
    video_ids = [row[0] for row in rows]
    return video_ids