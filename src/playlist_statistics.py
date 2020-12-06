import json
import statistics

def playlist_statistics():
    with open('data/all_playlists.json','r') as f:
        playlists = json.load(f)

    with open('data/all_videos.json','r') as f:
        vids = json.load(f)

    data = {}
    # considered_channels_list = ['nptel','physics_wallah','mit','khan_academy','unacademy_jee','study_iq_education']
    considered_channels_list = ['mit']
    for channel in playlists:
        if channel not in considered_channels_list:
            continue
        for playlist in playlists[channel]:
            videos = playlists[channel][playlist]["video_ids"]
            valid_videos = []
            for vid in videos:
                try:
                    views = int(vids[vid]["statistics"]["viewCount"])
                    likes = int(vids[vid]["statistics"]["likeCount"])
                    valid_videos.append((vid,views,likes))
                except:
                    pass
            if(len(valid_videos) >= 4): #Only consider playlists with at least 4 videos
                data[playlist] = sorted(valid_videos,key = lambda x: -x[1])
    cutoff_length = 75
    freq_list = [[] for _ in range(cutoff_length+2)] # a[101] means more than 100

# ===========================================================================
    # # Median views with length
    # for playlist in data:
    #     if len(data[playlist]) <= cutoff_length:
    #         freq_list[len(data[playlist])].append(sum([x[1] for x in data[playlist]])/len(data[playlist]))
    #     else:
    #         freq_list[cutoff_length+1].append(sum([x[1] for x in data[playlist]])/len(data[playlist]))
    # med_views_freq = [None] + [statistics.median(freq_list[i])  if freq_list[i] else None for i in range(1,cutoff_length+2)] # median views
    # return med_views_freq
# ===========================================================================
    # views in last/first video.
    # for playlist in data:
    #     if len(data[playlist]) <= cutoff_length:
    #         freq_list[len(data[playlist])].append(data[playlist][-1][1]/data[playlist][0][1])
    # med_freq = [None] + [statistics.median(freq_list[i])  if freq_list[i] and len(freq_list[i])>1 else None for i in range(1,cutoff_length+2)] # median
    # return med_freq
# =============================================================================
    # Average relative decrease:
    # for playlist in data:
    #     if len(data[playlist]) <= cutoff_length:
    #         l = [(data[playlist][i][1]-data[playlist][i+1][1])/data[playlist][i][1] for i in range(len(data[playlist])-1)]
    #         avg_dec = sum(l)/len(l)
    #         freq_list[len(data[playlist])].append(avg_dec)
    # med_freq = [None] + [statistics.median(freq_list[i])  if freq_list[i] and len(freq_list[i])>1 else None for i in range(1,cutoff_length+2)] # median
    # return med_freq
# ================================================================================
    # Trend of relative retention with each passing video.
    # for playlist in data:
    #     if len(data[playlist]) <= cutoff_length:
    #         l = [data[playlist][i+1][1]/data[playlist][i][1] for i in range(len(data[playlist])-1)]
    #         for i in range(len(l)):
    #             freq_list[i+1].append(l[i])
    # med_freq = [None] + [statistics.median(freq_list[i])  if freq_list[i] and len(freq_list[i])>3 else None for i in range(1,cutoff_length+2)] # median
    # return med_freq[:45]
# =================================================================================
    # Trend of viewer retention for a playlist.
    # for playlist in data:
    #     if len(data[playlist]) <= cutoff_length:
    #         l = [data[playlist][i][1]/data[playlist][0][1] for i in range(len(data[playlist])-1)]
    #         for i in range(len(l)):
    #             freq_list[i+1].append(l[i])
    # med_freq = [None] + [100*statistics.mean(freq_list[i])  if freq_list[i] and len(freq_list[i])>3 else None for i in range(1,cutoff_length+2)] # median
    # return med_freq[:25]
# =================================================================================
    # Trend of viewer retention from 3rd video (assumption: people who watch till 3rd video are 'serious watchers')
    for playlist in data:
        if len(data[playlist]) <= cutoff_length:
            l = [data[playlist][i][1]/data[playlist][2][1] for i in range(len(data[playlist])-1)]
            for i in range(len(l)):
                freq_list[i+1].append(l[i])
    med_freq = [None] + [100*statistics.mean(freq_list[i])  if freq_list[i] and len(freq_list[i])>3 else None for i in range(1,cutoff_length+2)] # median
    return med_freq[3:45]

def top_peaks():
    with open('data/all_playlists.json','r') as f:
        playlists = json.load(f)

    with open('data/all_videos.json','r') as f:
        vids = json.load(f)

    data = {}
    # considered_channels_list = ['nptel','physics_wallah','mit','khan_academy','unacademy_jee','study_iq_education']
    considered_channels_list = ['mit','nptel']
    for channel in playlists:
        if channel not in considered_channels_list:
            continue
        for playlist in playlists[channel]:
            videos = playlists[channel][playlist]["video_ids"]
            valid_videos = []
            for vid in videos:
                try:
                    views = int(vids[vid]["statistics"]["viewCount"])
                    valid_videos.append((vid,views))
                except:
                    pass
            if(len(valid_videos) >= 8): #Only consider playlists with at least 8 videos
                # Handle reversed course playlists:
                if valid_videos[0][1] >= valid_videos[-1][1]:
                    data[playlist] = valid_videos
                else:
                    data[playlist] = valid_videos[::-1]
    cutoff_length = 75
    ratio_list = [[] for _ in range(cutoff_length+2)] # a[101] means more than 100
    for playlist in data:
        if len(data[playlist]) <= cutoff_length:
            l = [0] + [(data[playlist][i+1][1]-data[playlist][i][1])/data[playlist][i][1] for i in range(len(data[playlist])-1)]
            for i in range(len(l)):
                ratio_list[i+1].append(l[i])
    mean_ratio = [statistics.mean(ratio_list[i]) if ratio_list[i] else None for i in range(len(ratio_list))]
    stdev_ratio = [statistics.stdev(ratio_list[i]) if len(ratio_list[i])>1 else 1 for i in range(len(ratio_list))]

    zscores_list = []
    for playlist in data:
        if len(data[playlist]) <= cutoff_length:
            videos = data[playlist]
            # only consider from 3rd video to second last video.
            for i in range(2,len(videos)-1):
                cur_ratio = (videos[i][1] - videos[i-1][1])/videos[i-1][1]
                zscore = (cur_ratio - mean_ratio[i+1])/stdev_ratio[i+1]
                zscores_list.append((zscore,i+1,videos[i][0],playlist)) #(zscore, position, video id, playlist id)
    
    sorted_zscores = (sorted(zscores_list))[::-1]
    return sorted_zscores[:100]

data = top_peaks()
outfile = open("test.json", "w")
json.dump(data, outfile , indent = 4)