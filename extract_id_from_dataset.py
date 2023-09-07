import re
import csv

id_list = []

with open('TC_VC_VIDO_CMNTR_WRTER_20211126104910_1.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        # Access and process the values in each row
        match = re.search(r'v=([^,]+)', row[-1])
        if match:
            video_id = match.group(1)
            id_list.append(video_id)
            print("Extracted Video ID:", video_id)

        else:
            print("Video ID not found in the input string.")

with open('comment_writer.txt', 'w') as f:
    for line in id_list:
        f.write(line)
        f.write('\n')