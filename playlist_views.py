import json
import statistics

def playlist_views(channel,pid):
    with open('data/all_playlists.json','r') as f:
        playlists = json.load(f)
    with open('data/all_videos.json','r') as f:
        vids = json.load(f)
    videos = playlists[channel][pid]["video_ids"]
    view_count = []
    for vid in videos:
        views = int(vids[vid]["statistics"]["viewCount"])
        view_count.append(views)
    return view_count

d = playlist_views("mit","PLUl4u3cNGP620R91K4KP_fO4l3eeK5lDn") #Abhijit Banerjee
# d = playlist_views("mit","PLUl4u3cNGP62QumaaZtCCjkID-NgqrleA") # sudoku puzzle
# d = playlist_views("mit","PLUl4u3cNGP62esZEwffjMAsEMW_YArxYC") # Introduction to mechanical vibration
# d = playlist_views("mit","PLUl4u3cNGP61FVzAxBP09w2FMQgknTOqu") # quantum
# d = playlist_views("mit","PLUl4u3cNGP62KuY_lVKJl2bmE2JUSZA-R") # spindle girl
# d = playlist_views("nptel","PLbMVogVj5nJSzoQXmu7dsj9ZKJyZ1P4O8") #AJM

outfile = open("test.json", "w")
json.dump(d, outfile , indent = 4)