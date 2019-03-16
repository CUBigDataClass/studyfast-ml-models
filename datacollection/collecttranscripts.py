import json
from yaml import load, FullLoader
from youtube import API
from youtube_transcript_api import YouTubeTranscriptApi

with open("keys.yaml", "r") as keys:
    config = load(keys, Loader=FullLoader)
api = API(client_id=config['client_id'], client_secret=config["client_secret"], api_key=config["api_key"])

terms = [
    "linear algebra",
    "calculus", 
    "derivative", 
    "shakespear",
    "python coding tutorial"
]

def get_transcript(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

def write_transcript_to_file(name, transcript):
    with open("transcripts/" + name + '.json', 'w') as writefile:  
        json.dump(transcript, writefile)

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
        try:
            token = response["nextPageToken"]
        except KeyError:
            return set(ids)
        for item in response["items"]:
            ids.append(item["id"]["videoId"])
    return set(ids)

def download_transcripts():
    searched = list()
    for term in terms:
        print(f"Exploring term: {term}")
        ids = get_search_ids(term)
        for i in ids:
            if i not in searched:
                searched.append(i)
                try:
                    transcript = get_transcript(i)
                except YouTubeTranscriptApi.CouldNotRetrieveTranscript: 
                    print(f"couldn't retrieve transcript for {i}")
                    continue
                write_transcript_to_file(i, transcript)


if __name__ == "__main__":
    download_transcripts()