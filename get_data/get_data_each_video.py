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

with open('data/video_ids.json','r') as f:
    video_ids = json.load(f)

all_videos_list = [y for x in video_ids.keys() for y in video_ids[x]]
all_videos_info = {}
step_length = 50

for i in range(0,len(all_videos_list),step_length):
    print('{}/{}'.format(i,len(all_videos_list)))
    videos_info = get_video_data(all_videos_list[i:i+step_length])
    for x in videos_info:
        all_videos_info[x['id']] = x


outfile = open("test.json", "w")
json.dump(all_videos_info, outfile , indent = 4)
