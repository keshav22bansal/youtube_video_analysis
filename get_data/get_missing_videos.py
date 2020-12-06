import urllib.request
import json

key_umang = "AIzaSyBvUdfzgIifNy5NK11jyv8bSPRUp2y9fB4"

def get_video_data(video_ids):
    '''Returns the information for a list of videos'''
    api_key = key_umang
    video_ids_csv_str = ','.join(video_ids)
    video_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}".format(video_ids_csv_str, api_key)
    inp = urllib.request.urlopen(video_url)
    resp = json.load(inp)
    return resp['items']

with open('data/all_playlists.json','r') as f:
    playlists = json.load(f)

with open('data/all_videos.json','r') as f:
    vids = json.load(f)

# Find list of missing videos.
missing_videos_list = []
for channel in playlists:
    for playlist in playlists[channel]:
        videos = playlists[channel][playlist]["video_ids"]
        for vid in videos:
            if not vids.get(vid,None):
                missing_videos_list.append(vid)
missing_videos_info = {}
step_length = 50
print(missing_videos_list)
# print(len(missing_videos_list))
# for i in range(0,len(missing_videos_list),step_length):
#     print('{}/{}'.format(i,len(missing_videos_list)))
#     videos_info = get_video_data(missing_videos_list[i:i+step_length])
#     for x in videos_info:
#         vids[x['id']] = x



# outfile = open("test.json", "w")
# json.dump(vids, outfile , indent = 4)
