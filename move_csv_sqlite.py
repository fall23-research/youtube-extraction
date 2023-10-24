import pandas as pd
import sqlite3

# Excel 파일 경로
excel_file = '/Users/siwon/Desktop/Fall-23/research/official_news_dataset/videos_information_transcripts_with_covid.xls' 

# SQLite 데이터베이스 연결
conn = sqlite3.connect("/Users/siwon/Desktop/Fall-23/research/youtube_transcript/news_video.sqlite")
cursor = conn.cursor()

# Excel 파일 읽기
df = pd.read_excel(excel_file)

# 데이터베이스에 데이터 삽입
df.to_sql('news_video', conn, if_exists='append', index=False)

# 커밋 및 연결 종료
conn.commit()
conn.close()
