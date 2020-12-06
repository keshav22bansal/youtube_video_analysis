# CS685 PROJECT - Youtube Educational Content Analysis

This repository contains all code created as a part of CS685A course project.


### Getting Started

A step by step series of examples that tell you how to get the code running

Clone the repo

```
git clone https://github.com/keshav22bansal/youtube_video_analysis
```
#### Create and start a virtual environment
##### Using virtualenv
```
virtualenv -p python3 env --no-site-packages

source env/bin/activate
```
#### Using conda
```
conda create -n env python=3.6

source activate env
```
#### Install the project dependencies:
```
pip3 install -r requirements.txt
```

### Files and usage

#### Files
Heuristic_NER.py: We obtain the college-level data from NPTEL’s website and then apply Named entity recognition to give college and branch tags. “Heuristic_NER.py” contains code for giving college and branch tags to videos using the video description. 

topic_rankings.py - Performs clustering of playlist courses into similar topics for nptelhrd and MITOCW channels and then ranks the top 100 viewed topics on both channels. It also plots graphs of percetntwise distribution of the top 10 topics of both channels and also plots the rate

get_comment_polarity.json - assign a polarity value in range [-1,1] to each comment.

Get_optimal_length.py - plot graphs of number of likes/vies/comments with video length

#### Directories

get_data directory: This directory contains files used for generating the dataset from the Youtube Data API. get_data.py gets videos for a channel, get_data_playlists.py gets the playlists for a channel, get_data_each_video.py gets the data about each video from all channels, get_data_comments.

