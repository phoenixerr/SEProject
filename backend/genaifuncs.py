# for genai
import os

import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_transcript(video_id):
    all_transcripts = []
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript_text = " ".join([i["text"] for i in transcript])
        all_transcripts.append(transcript_text)
    except Exception as e:
        return f"Error getting Transcript for video {video_id}"

    return all_transcripts[0]


# for genai
def generate_summary_from_transcript(transcript, prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript)
    return response.text
