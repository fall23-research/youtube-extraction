import sqlite3
from extract_video_transcript import *

database = sqlite3.connect("news_comment.sqlite")
databaseCursor = database.cursor()


# databaseCursor.execute('''CREATE TABLE IF NOT EXISTS news_comment(
#                             id INTEGER PRIMARY KEY ASC,
#                             comment_id TEXT, 
#                             video_id TEXT, 
#                             text_display TEXT,
#                             author_name TEXT,
#                             author_channel_url TEXT, 
#                             like_count INTEGER,
#                             published_at TEXT,
#                             total_reply_count INTEGER
#                             )''')
# database.commit()


def execute_batch(query, data):
    """
    일괄 삽입을 위한 도우미 함수
    """
    databaseCursor.executemany(query, data)

def insert_news_comment_batch_metadata(news_comment_data_list):
    """
    여러 댓글 데이터를 일괄로 DB에 삽입
    """
    print('db executed')
    
    query = '''INSERT INTO news_comment(comment_id, video_id, text_display, author_name, author_channel_url, like_count, published_at, total_reply_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    data = [(
            video.get('comment_id', ''), video.get('video_id', ''), video.get('text_display', ''),
            video.get('author_name', ''), video.get('author_channel_url', ''), video.get('like_count', ''),
            video.get('published_at', ''), video.get('total_reply_count', '')
            ) for video in news_comment_data_list]

    execute_batch(query, data)
    database.commit()