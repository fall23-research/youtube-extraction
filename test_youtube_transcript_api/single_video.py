from youtube_transcript_api import YouTubeTranscriptApi
from pykospacing import Spacing
import time
from xlwt import Workbook

start_time = time.time()

# Workbook is created
wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')

# Youtube Video id ?v=
video_id = 'QJAsxuPmbK0'

transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
text = ""
# iterate over all available transcripts
for transcript in transcript_list:
    text += transcript['text']

text_wo_space = text.replace(" ", "")

spacing = Spacing()
text = spacing(text_wo_space)

print(text)
sheet1.write(1, 0, text)
wb.save('xlwt example.xls')

end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")