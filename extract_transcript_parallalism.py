from youtube_transcript_api import YouTubeTranscriptApi
from pykospacing import Spacing
import concurrent.futures
import time
from xlwt import Workbook

start_time = time.time()

# function for extracting transcript from a single video
def process_transcript_extraction(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
    text = ""
    # iterate over all available transcripts
    for transcript in transcript_list:
        text += transcript['text']

    text_wo_space = text.replace(" ", "")

    spacing = Spacing()
    text = spacing(text_wo_space)

    return text

# contain video ids in a list
count = 0
video_ids = []
f = open('news_video_ids.txt', 'r')
for id in f:
    video_id = id.replace("\n", "")
    video_ids.append(video_id)

    count += 1
    if count >= 100:
        break 

print(video_ids)
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

# Write the column headers
sheet1.write(0, 0, 'Video ID')
sheet1.write(0, 1, 'Transcript')

MAX_CELL_LENGTH = 32767

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_transcript_extraction, video_id): video_id for video_id in video_ids}
    
    row = 1

    # Collect results
    for future in concurrent.futures.as_completed(futures):
        video_id = futures[future]
        try:
            transcript = future.result()

            if len(transcript) > MAX_CELL_LENGTH:
                # Truncate the transcript to the maximum allowed length
                transcript = transcript[:MAX_CELL_LENGTH]

            sheet1.write(row, 0, video_id)
            sheet1.write(row, 1, transcript)
            row += 1
        except Exception as e:
            print(f"An error occurred for video ID {video_id}: {str(e)}")

wb.save('news_dataset_w_transcript.xls')

end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")
