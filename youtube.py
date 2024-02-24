import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set the API key
api_key = "AIzaSyA95CnGJFP58xxnCquO8lwPtu4g2CQ2zmo"

# Create a YouTube API service
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_data(channel_id):
    try:
        # Get channel information
        channel_request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
        channel_response = channel_request.execute()
        if channel_response.get('items'):
            channel_data = channel_response['items'][0]
            return channel_data
        else: 
            return None
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def get_video_data(video_id):
    try:
        # Get video information
        video_request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id)
        video_response = video_request.execute()
        video_data = video_response['items'][0]
        return video_data
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example: Retrieving data for a YouTube channel and video
    channel_id = 'UC7cs8q-gJRlGwj4A8OmCmXg'
    video_id = 'rGx1QNdYzvs'

    channel_data = get_channel_data(channel_id)
    video_data = get_video_data(video_id)

    if channel_data:
        print("Channel Data:")
        print(channel_data)

    # if video_data:
    #     print("\nVideo Data:")
    #     print(video_data)
