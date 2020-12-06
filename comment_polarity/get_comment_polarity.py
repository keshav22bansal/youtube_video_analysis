import json
from textblob import TextBlob
from collections import defaultdict

def get_polarity(comment):
    x = TextBlob(comment).sentiment
    return x.polarity,x.subjectivity

comments_data = json.loads(open('../data/comments.json').read())
d = defaultdict(list) 

for video_id, comments in comments_data.items():
    for comment in comments:
        comment['polarity'],comment['subjectivity'] = get_polarity(comment['text'])
        d[video_id].append(comment)


open('../data/comments_with_polarity.json','w').write(json.dumps(d,indent = 4))