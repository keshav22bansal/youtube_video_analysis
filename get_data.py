import urllib
import json

channels = []
key_umang = "AIzaSyBnLh96mbiSTPFVZsm16LUln0M8HMwMpK4"
  
channel_to_id_map = {
    "physics_wallah" : "UCiGyWN6DEbnj2alu7iapuKQ",
    "mit" : "UCEBb1b_L6zDS3xTUrIALZOw",
    "khan_academy" : "UC4a-Gbdw7vOaccHmFo40b9g",
    "unacademy_jee" : "UCZNNx4KYmCkwxCLdsHyWqQA",
    "nptel" : "UC640y4UvDAlya_WOj5U4pfA",
    "study_iq_education" : "UCrC8mOqJQpoB7NuIMKIS6rQ"
}

def get_all_video_in_channel(channel_id):
    ''' Returns a list of video_ids for a channel'''
    # First get the playlist corresponding to "all videos" of the channel. Then fetch the items in that playlist.
    api_key = key_umang
    all_videos_url = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}".format(channel_id,api_key)
    inp = urllib.request.urlopen(all_videos_url)
    resp = json.load(inp)
    all_videos_playlist_id = resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    first_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={}&key={}".format(all_videos_playlist_id,api_key)
    count=0
    url = first_url
    video_ids = []
    while True:
        count+=1
        print(count)
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        for i in resp['items']:
            video_ids.append(i['contentDetails']['videoId'])
        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_ids

# Get video ids for all channels
channel_list = ["physics_wallah","nptel","mit","khan_academy","unacademy_jee","study_iq_education"]
all_video_ids = {}
for channel_name in channel_list:
    video_ids = get_all_video_in_channel(channel_to_id_map[channel_name])
    all_video_ids[channel_name] = video_ids

outfile = open("data/video_ids_test.json", "w")
json.dump(all_video_ids, outfile , indent = 4)
