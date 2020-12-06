## Code to extract college names from video description of videos on nptel youtube channel.
import json
import numpy as np
import statistics
college_map = {
    "IITK": "IITK",
    "IIT Kanpur": "IITK",
    "Indian Institute of Technology Kanpur": "IITK",
    "IITB": "IITB",
    "IIT Bombay": "IITB",
    "Indian Institute of Technology Bombay": "IITB",
    "IITM": "IITM",
    "IIT Madras": "IITM",
    "Indian Institute of Technology Madras": "IITM",
    "IITD": "IITD",
    "IIT Delhi": "IITD",
    "Indian Institute of Technology Delhi": "IITD",
    "IITKGP": "IITKGP",
    "IIT Kharagpur": "IITKGP",
    "Indian Institute of Technology Kharagpur": "IITKGP",
}

department_map = {
    "Computer Science":"CSE",
    "Computer":"CSE",
    "computer":"CSE",
    "CSE":"CSE",
    "Electrical Engineering":"EE",
    "electrical":"EE",
    "Electrical":"EE",
    "EE": "EE",
    "Mechanical Engineering":"ME",
    "Mechanical": "ME",
    "ME":"ME",
    "Chemical":"CHE",
    "CHE":"CHE"
}
considered_channels_id = ['UC640y4UvDAlya_WOj5U4pfA']
def get_college_name():
    ''' Gets upto 50 comments for all videos with at least 5 comments. Only fetch for nptel and mit '''
    with open('data/all_videos.json','r') as f:
        vids = json.load(f)
    i=0
    map_vide_college = {}
    college_count = {}
    college_to_videos = {}
    college_to_dep_video = {}
    for vid in vids:
        if vids[vid]['snippet']['channelId'] not in considered_channels_id:
            continue
        video_description = vids[vid]['snippet'].get('description',None)
        if video_description:
            for key in college_map:
                if key in video_description:
                    print(video_description, college_map[key])

                    map_vide_college[vid] = college_map[key]
                    if college_map[key] not in college_to_videos:
                        college_to_videos[college_map[key]]= [vid]
                    else:
                        college_to_videos[college_map[key]].append(vid)
                    
                    for dep in department_map:
                        if dep in video_description:

                            if college_map[key] not in college_to_dep_video:
                                college_to_dep_video[college_map[key]] = {}
                                college_to_dep_video[college_map[key]][department_map[dep]] = {}
                                college_to_dep_video[college_map[key]][department_map[dep]]["videos"] = [vid]
                                college_to_dep_video[college_map[key]][department_map[dep]]["viewCount"] = [int(vids[vid]["statistics"]["viewCount"])]
                                college_to_dep_video[college_map[key]][department_map[dep]]["likeCount"] = int(vids[vid]["statistics"]["likeCount"])
                                college_to_dep_video[college_map[key]][department_map[dep]]["dislikeCount"] = int(vids[vid]["statistics"]["dislikeCount"])
                            else:
                                if department_map[dep] not in college_to_dep_video[college_map[key]]:
                                    college_to_dep_video[college_map[key]][department_map[dep]] = {}
                                    college_to_dep_video[college_map[key]][department_map[dep]]["videos"] = [vid]
                                    college_to_dep_video[college_map[key]][department_map[dep]]["viewCount"] = [int(vids[vid]["statistics"]["viewCount"])]
                                    college_to_dep_video[college_map[key]][department_map[dep]]["likeCount"] = int(vids[vid]["statistics"]["likeCount"])
                                    college_to_dep_video[college_map[key]][department_map[dep]]["dislikeCount"] = int(vids[vid]["statistics"]["dislikeCount"])
                                else:
                                    college_to_dep_video[college_map[key]][department_map[dep]]["videos"].append(vid)
                                    college_to_dep_video[college_map[key]][department_map[dep]]["viewCount"].append(int(vids[vid]["statistics"]["viewCount"]))
                                    college_to_dep_video[college_map[key]][department_map[dep]]["likeCount"] += int(vids[vid]["statistics"]["likeCount"])
                                    college_to_dep_video[college_map[key]][department_map[dep]]["dislikeCount"] += int(vids[vid]["statistics"]["dislikeCount"])
                    
            # video_description = int(count)
            # if count >= 5:
            #     comments[vid] = get_comments_for_video(vid)
            #     i+=1
            #     if(i%5 == 0):
            #         print(i)
    return map_vide_college,college_to_videos,college_to_dep_video

map_videos,college_to_videos,college_dep_to_videos = get_college_name()
for college in college_to_videos:
    print(college, len(college_to_videos[college]))
# li = []
college_views = {}
for college in college_dep_to_videos:
    if college not in college_views:
        college_views[college] = [0,0]
    for dep in college_dep_to_videos[college]:
        count_videos = len(college_dep_to_videos[college][dep]["videos"])
        median_views = np.median(college_dep_to_videos[college][dep]["viewCount"])
        college_views[college][0]+= sum(college_dep_to_videos[college][dep]["viewCount"])
        college_views[college][1] +=len(college_dep_to_videos[college][dep]["videos"])
        # li.append([college, dep, count_videos, college_dep_to_videos[college][dep]["viewCount"]/count_videos, college_dep_to_videos[college][dep]["likeCount"]/count_videos, college_dep_to_videos[college][dep]["likeCount"]/(college_dep_to_videos[college][dep]["likeCount"] + college_dep_to_videos[college][dep]["dislikeCount"]))])
        print("(%s, %s, %d, %0.3f, %0.3f, %0.3f)" %(college, dep, count_videos, median_views, college_dep_to_videos[college][dep]["likeCount"]/count_videos, college_dep_to_videos[college][dep]["likeCount"]/(college_dep_to_videos[college][dep]["likeCount"] + college_dep_to_videos[college][dep]["dislikeCount"])))
for college in college_views:
    print(college, college_views[college][0]/college_views[college][1])

outfile = open("data/college_to_videos.json", "w")
json.dump(college_to_videos, outfile , indent = 4)

outfile = open("data/college_dep_to_videos.json", "w")
json.dump(college_dep_to_videos, outfile , indent = 4)