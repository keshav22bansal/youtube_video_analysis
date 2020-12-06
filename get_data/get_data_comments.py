import json
import urllib.request

key_umang = "AIzaSyBvUdfzgIifNy5NK11jyv8bSPRUp2y9fB4"

channel_to_id_map = {
    "physics_wallah" : "UCiGyWN6DEbnj2alu7iapuKQ",
    "mit" : "UCEBb1b_L6zDS3xTUrIALZOw",
    "khan_academy" : "UC4a-Gbdw7vOaccHmFo40b9g",
    "unacademy_jee" : "UCZNNx4KYmCkwxCLdsHyWqQA",
    "nptel" : "UC640y4UvDAlya_WOj5U4pfA",
    "study_iq_education" : "UCrC8mOqJQpoB7NuIMKIS6rQ"
}

# Considering only mit and nptel
# considered_channels_id = ['UCEBb1b_L6zDS3xTUrIALZOw','UC640y4UvDAlya_WOj5U4pfA']
# Consider physics_wallah and unacademy jee.
considered_channels_id = ['UCiGyWN6DEbnj2alu7iapuKQ','UCZNNx4KYmCkwxCLdsHyWqQA']

def get_comments():
    ''' Gets upto 50 comments for all videos with at least 5 comments.'''
    with open('data/all_videos.json','r') as f:
        vids = json.load(f)
    i=0
    comments = {}
    for vid in vids:
        if vids[vid]['snippet']['channelId'] not in considered_channels_id:
            continue
        count = vids[vid]['statistics'].get('commentCount',None)
        if count:
            count = int(count)
            if count >= 5:
                comments[vid] = get_comments_for_video(vid)
                i+=1
                if(i%5 == 0):
                    print(i)
    return comments
    
def get_comments_for_video(vid):
    '''for the video, returns a list of comment objects  [{text: String , likes: Integer}]'''
    api_key = key_umang
    url = "https://www.googleapis.com/youtube/v3/commentThreads?textFormat=plainText&part=snippet&maxResults=50&order=relevance&videoId={}&key={}".format(vid,api_key)
    inp = urllib.request.urlopen(url)
    resp = json.load(inp)
    comments = []
    for item in resp['items']:
        comments.append({
            'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
            'likes': item['snippet']['topLevelComment']['snippet']['likeCount']
        })
    return comments


comments = get_comments()
outfile = open("data_comments_physicswallah_unacademy.json", "w")
json.dump(comments, outfile , indent = 4)
