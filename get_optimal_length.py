import json
import numpy as np
import matplotlib.pyplot as plt
import re
import pandas as pd
import seaborn as sns
from collections import defaultdict


def get_duration(time):

    time = time.replace('PT','').lower()
    duration = 0
    for i,timestamp in enumerate(['s','m','h']):
        val = re.findall('[\d]*'+timestamp,time)
        if len(val) is not 0:
            val = int(val[0].replace(timestamp,''))
        else:
            val = 0
        duration += val*(60**i)
    return duration



all_video_data = json.loads(open('../data/all_videos.json').read())


def global_frequency():
    y = []

    for data in all_video_data:
        duration = (all_video_data[data]['contentDetails'].get('duration','0'))
        y.append(get_duration(duration))
    plt.hist(y,bins = np.arange(0,1000,100))
    plt.savefig('global_frequency.png')
    mean = np.mean(y)
    std = np.std(y)

    print(mean,std)

def global_optimal(statistic='viewCount'):
    y = []
    x = []

    max_duration = 2000
    bin_width = 100
    for data in all_video_data:
        duration = (all_video_data[data]['contentDetails'].get('duration','0'))
        duration = get_duration(duration)
        val = int(all_video_data[data]['statistics'].get(statistic,0))
        if duration <= max_duration and val<=20000:
            x.append(duration)
            y.append(val)
    df = pd.DataFrame({'duration':x,statistic:y})
    df['VideoLength'] = pd.cut(df['duration'], bins=range(0,max_duration,bin_width), labels=[f'{l}-{l+bin_width}' for l in range(0,max_duration-bin_width,bin_width)])
    fig,ax = plt.subplots(1,1, figsize=(15,8))
    
    sns.barplot(x='VideoLength',y = statistic,data = df,ax = ax)
    plt.xticks(rotation = 90,fontsize = 6)
    plt.xlabel('Video Length (seconds)')
    plt.ylabel(stats_display_names[statistic])
    plt.title('{} vs Video Length'.format(stats_display_names[statistic]))
    # plt.boxplot(x,y)
    plt.savefig('global_optimal_{}.png'.format(statistic))

def heatmap():
    d = defaultdict(list)
    for data in all_video_data:
        for s in statistics:
            d[s].append(all_video_data[data]['statistics'].get(s,0))
    df = pd.DataFrame(d).astype(float)
    corr = df.corr(method = 'spearman')
    print('**',corr)
    fig,ax = plt.subplots(1,1, figsize=(15,8))
    sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
    )
    plt.title('Spearman Correlation Heatmap')
    plt.savefig('correlation_heatmap.png')
    
def heatmap_channel_wise():
    channel_data = json.loads(open('../data/video_ids.json').read())
    for channel,ids in channel_data.items():
        d = defaultdict(list)
        for data in ids:
            for s in statistics:
                d[s].append(all_video_data[data]['statistics'].get(s,0))
        df = pd.DataFrame(d).astype(float)
        corr = df.corr(method = 'spearman')
        print('**',channel,corr)
        fig,ax = plt.subplots(1,1, figsize=(15,8))
        sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
        )
        channel_display_name = channel.replace('_',' ').title()
        plt.title('Spearman Correlation Heatmap for {}'.format(channel_display_name))
        plt.savefig('correlation_heatmap_{}.png'.format(channel))
# global_frequency()
statistics = ['likeCount','viewCount','commentCount']
stats_display_names = {"likeCount":"Like Count","viewCount":"View Count","commentCount":"View Count"}
# for stat in statistics:
#     global_optimal(stat)
heatmap()
heatmap_channel_wise()