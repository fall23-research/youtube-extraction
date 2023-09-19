lines_seen = set() # holds lines already seen
outfile = open('comment_video_id_wo_duplicates.txt', "w")
for line in open("comment_video_id.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()