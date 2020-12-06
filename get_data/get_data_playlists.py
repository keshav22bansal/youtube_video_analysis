import urllib.request 
import json

channels = []
key_umang = "AIzaSyBvUdfzgIifNy5NK11jyv8bSPRUp2y9fB4"
  
channel_to_id_map = {
    "physics_wallah" : "UCiGyWN6DEbnj2alu7iapuKQ",
    "mit" : "UCEBb1b_L6zDS3xTUrIALZOw",
    "khan_academy" : "UC4a-Gbdw7vOaccHmFo40b9g",
    "unacademy_jee" : "UCZNNx4KYmCkwxCLdsHyWqQA",
    "nptel" : "UC640y4UvDAlya_WOj5U4pfA",
    "study_iq_education" : "UCrC8mOqJQpoB7NuIMKIS6rQ"
}

def get_playlist_data(channel_id):
    ''' Returns a dictionary containing playlists for a channel'''
    # First fetch all playlists for the channel. Then find videos for each playlist.
    api_key = key_umang
    all_items = []
    first_playlist_url = "https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=50&channelId={}&key={}".format(channel_id,api_key)
    url = first_playlist_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        all_items.extend(resp['items'])
        try:
            next_page_token = resp['nextPageToken']
            url = first_playlist_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    
    d = {}
    playlist_ids  = []
    for item in all_items:
        playlist_id = item['id']
        playlist_ids.append(playlist_id)
        d[playlist_id] = {}
        d[playlist_id]['playlist_info'] = {}
        for key in ['publishedAt','title','description']:
            d[playlist_id]['playlist_info'][key] = item['snippet'][key]
    count=0
    for playlist_id in playlist_ids:
        count+=1
        print('{}/{}'.format(count,len(playlist_ids)))
        first_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={}&key={}".format(playlist_id,api_key)
        url = first_url
        video_ids = []
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)
            for i in resp['items']:
                video_ids.append(i['contentDetails']['videoId'])
            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except:
                break

        d[playlist_id]['video_ids'] = video_ids
    return d

# Get video ids for all channels
channel_list = ["nptel","physics_wallah","mit","khan_academy","unacademy_jee","study_iq_education"]
all_video_ids = {}
for channel_name in channel_list:
    video_ids = get_playlist_data(channel_to_id_map[channel_name])
    all_video_ids[channel_name] = video_ids

outfile = open("test.json", "w")
json.dump(all_video_ids, outfile , indent = 4)
