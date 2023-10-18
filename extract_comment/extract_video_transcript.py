from youtube_transcript_api import YouTubeTranscriptApi
from pykospacing import Spacing

# function for extracting transcript from a single video
def process_transcript_extraction(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        text = ""
        # iterate over all available transcripts
        for transcript in transcript_list:
            text += transcript['text']

        text_wo_space = text.replace(" ", "")

        spacing = Spacing()
        text = spacing(text_wo_space)

        return text
    except Exception as e:
        print(f"Error updating transcripts: {e}")