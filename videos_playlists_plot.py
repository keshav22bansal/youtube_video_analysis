import json
with open('data/all_playlists.json','r') as f:
    playlists = json.load(f)

with open('data/video_ids.json','r') as f:
    vids = json.load(f)
obj = {}
for channel in vids:
    obj[channel] = (len(vids[channel]),len(playlists[channel]))

with open('test.json','w') as f:
    json.dump(obj,f,indent=4)