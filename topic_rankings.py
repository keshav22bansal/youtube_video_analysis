import numpy as np
import json
import re
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import seaborn as sns

isShortlisted = lambda x: (x == "nptelhrd" or x == "MIT OpenCourseWare")

# all_tags = {}
# with open("data/all_videos.json", "r") as f:
# 	video_info = json.load(f)
# 	for vid, info in video_info.items():
# 		if "channelTitle" in info["snippet"] and "tags" in info["snippet"] and \
# 			isShortlisted(info["snippet"]["channelTitle"]):
# 				for tag in info["snippet"]["tags"]:
# 					if tag not in all_tags:
# 						all_tags[tag] = 0;
# 					all_tags[tag] += 1

# i = 0
# for k, v in sorted(all_tags.items(), key=lambda x: x[1], reverse=True):
# 	if i == 100:
# 		break
# 	print(k, v)
# 	i += 1
# with open("data/tags_nptel_mitocw.json", "w") as f:
# 	json.dump(all_tags, f, sort_keys=True, indent=4)

# with open("data/all_videos.json", "r") as f:
# 	video_info = json.load(f)
# 	for vid, info in video_info.items():
# 		if "channelTitle" in info["snippet"] and isShortlisted(info["snippet"]["channelTitle"]):
# 			strings = ["data structures", "data_structures", ""]
# 				for tag in info["snippet"]["tags"]:
# 					if tag not in all_tags:
# 						all_tags[tag] = 0;
# 					all_tags[tag] += 1

# #mapping of topic names to {"views": , "likes": , "dislikes": , "comments": }
# playlist_stats = {"nptelhrd": {}, "MIT OpenCourseWare": {}}

# #mapping of video_id to {"views": , "likes": , "comments": }
# video_stats = {}

# with open("data/all_videos.json", "r") as f:
# 	video_info = json.load(f)
# with open("data/all_playlists.json", "r") as f:
# 	ch_playlist = json.load(f)

# for vid, info in video_info.items():
# 	if "statistics" in info:
# 		views = int(info["statistics"]["viewCount"]) if "viewCount" in info["statistics"] else 0
# 		likes = int(info["statistics"]["likeCount"]) if "likeCount" in info["statistics"] else 0
# 		dislikes = int(info["statistics"]["dislikeCount"]) if "dislikeCount" in info["statistics"] else 0
# 		comments = int(info["statistics"]["commentCount"]) if "commentCount" in info["statistics"] else 0
# 		video_stats[vid] = {"views": views, "likes": likes, "dislikes": dislikes, "comments": comments}

# regex = "(\s*[0-9A-Z]+\.[0-9A-Z\-\:]+\s*(/)?)+"
# for ch_name, playlist_info in ch_playlist.items():
# 	for ch_name_ in ["nptelhrd", "MIT OpenCourseWare"]:
# 		if ch_name == ch_name_:
# 			for plid, plinfo in playlist_info.items():
# 				# plid is playlist id, plinfo is playlist info
# 				avg_views, avg_likes, avg_dislikes, avg_comments = 0, 0, 0, 0
# 				if len(plinfo["video_ids"]) == 0:
# 					continue
# 				for vid in plinfo["video_ids"]:
# 					if vid in video_stats:
# 						avg_views += video_stats[vid]["views"]
# 						avg_likes += video_stats[vid]["likes"]
# 						avg_dislikes += video_stats[vid]["dislikes"]
# 						avg_comments += video_stats[vid]["comments"]
# 				try:
# 					avg_views /= len(plinfo["video_ids"])
# 					avg_likes /= len(plinfo["video_ids"])
# 					avg_dislikes /= len(plinfo["video_ids"])
# 					avg_comments /= len(plinfo["video_ids"])
# 				except ZeroDivisionError:
# 					continue
# 				plname = plinfo["playlist_info"]["title"]
# 				try:
# 					if ch_name == "nptelhrd":
# 						topic = plname.split("-")[1].strip() if "-" in plname else plname.strip()
# 					if ch_name == "MIT OpenCourseWare":
# 						topic = plname.split(re.search(regex, plname).group(0))[1]
# 						topic = re.split("(fall)|(spring)", topic, flags=re.IGNORECASE)[0]
# 						topic = topic.rsplit(",", 1)[0].strip()
# 				except AttributeError:
# 					continue
# 				# check if topic already exists in playlist_stats[ch_name]
# 				print(topic)
# 				topic_eq = None		# equivalent topic
# 				for topic_ in playlist_stats[ch_name]:
# 					if SequenceMatcher(None, topic, topic_).ratio() > 0.7:
# 						#similar topic exists
# 						topic_eq = topic_
# 						break;
# 				if topic_eq is None:
# 					# new topic, no equivalent topic exists
# 					playlist_stats[ch_name][topic] = {
# 						"playlist_names": [plname],
# 						"avg_views": avg_views, "avg_likes": avg_likes, 
# 						"avg_dislikes": avg_dislikes, "avg_comments": avg_comments,
# 						"n_videos": len(plinfo["video_ids"])
# 					}
# 				else:
# 					# equivalent topic exists
# 					playlist_stats[ch_name][topic_eq]["playlist_names"].append(plname)
# 					playlist_stats[ch_name][topic_eq]["avg_views"] = max(avg_views, playlist_stats[ch_name][topic_eq]["avg_views"])
# 					playlist_stats[ch_name][topic_eq]["avg_likes"] = max(avg_likes, playlist_stats[ch_name][topic_eq]["avg_likes"])
# 					playlist_stats[ch_name][topic_eq]["avg_dislikes"] = max(avg_dislikes, playlist_stats[ch_name][topic_eq]["avg_dislikes"])
# 					playlist_stats[ch_name][topic_eq]["avg_comments"] = max(avg_comments, playlist_stats[ch_name][topic_eq]["avg_comments"])
# 					playlist_stats[ch_name][topic_eq]["n_videos"] += len(plinfo["video_ids"])

# with open("data/playlist_detailed_info.json", "w") as f:
# 	json.dump(playlist_stats, f, sort_keys=False, indent=4)

with open("data/playlist_detailed_info.json", "r") as f:
	playlist_stats = json.load(f)

# print("\n\n\n")
views_plot = {"nptelhrd": {"x" : [i for i in range(100)], "y" : []}, 
			  "MIT OpenCourseWare": {"x" : [i for i in range(100)], "y" : []}}
for ch_name in ["nptelhrd", "MIT OpenCourseWare"]:
	i = 0
	for k, v in sorted(playlist_stats[ch_name].items(), key=lambda x: x[1]["avg_views"], reverse=True):
		if i == 100:
			break
		views_plot[ch_name]["y"].append(v["avg_views"])
		# print(k, v["avg_views"])
		i += 1
	# print("\n\n\n")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(views_plot["nptelhrd"]["x"][1:], views_plot["nptelhrd"]["y"][1:])
ax.plot(views_plot["MIT OpenCourseWare"]["x"][1:], views_plot["MIT OpenCourseWare"]["y"][1:])
ax.set_xlabel("Rank of course")
ax.set_ylabel("Average viewership of course playlist")
ax.set_title("Rate of fall of popularity among top course playlists")
ax.legend(["nptelhrd", "MIT OpenCourseWare"])
plt.show()

for ch_name, pal_color in zip([("nptelhrd", "NPTEL:"), ("MIT OpenCourseWare", "MITOCW:")], ["Greens_d", "Blues_d"]):
	data = {"x":views_plot[ch_name[0]]["x"][1:11], "y":views_plot[ch_name[0]]["y"][1:11]}
	pal = sns.color_palette(pal_color, len(data["y"]))
	rank = np.array(data["y"]).argsort().argsort()
	ax = sns.barplot(x="y", y="x", palette=np.array(pal[::1])[rank], data=data, orient="h")
	plt.title(ch_name[1] + " % distribution of views among top 10 course playlists")
	plt.xlabel('Average Viewership')

	total = sum(data["y"])
	for p in ax.patches:
	    percentage = '{:.1f}%'.format(100 * p.get_width()/total)
	    x = p.get_x() + p.get_width() + 0.02
	    y = p.get_y() + p.get_height()/2
	    ax.annotate(percentage, (x, y))

	plt.show()





