from yaml import load
from youtube import API
from youtube_transcript_api import YouTubeTranscriptApi

with open("keys.yaml", "r") as keys:
    config = load(keys)
api = API(client_id=config['client_id'], client_secret=config["client_secret"], api_key=config["api_key"])

def get_transcript(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

def get_search_ids(term, max_ids=10000):
    ids = list()
    token = None
    while len(ids) < max_ids:
        response = api.get(
            'search',
            q=term,
            type="video", 
            videoCaption="closedCaption", 
            relevanceLanguage="en",
            maxResults=50,
            pageToken=token
        )
        token = response["nextPageToken"]
        for item in response["items"]:
            if item["id"]["videoId"] not in ids:
                ids.append(item["id"]["videoId"])
    return ids

if __name__ == "__main__":
    print(get_search_ids("hello", max_ids=400))