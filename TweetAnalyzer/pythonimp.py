import csv
import operator
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric

date = {}
time = {}
text = {}
urls = {}
photos = {}
replies_count = {}
retweets_count = {}
likes_count= {}
hashtags = {}
reply_to = {}
count = 0
count75 = [0, 0, 0] 
count25 = [0, 0, 0] 
count50 = [0, 0, 0] 

def GetInfo(dict, id):
    for key, value in dict.items():
        if (int(key) == int(id)):
            result = value
    return result


with open('elonmusk2015to2020.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader) # skip column headers

    for line in csv_reader: # loading in all dicts, will probably combine into one later
        tweet_id = line[0]
        date[tweet_id] = line[3]
        time[tweet_id] = line[4]
        text[tweet_id] = line[10]
        urls[tweet_id] = line[12]
        photos[tweet_id] = line[13]
        replies_count[tweet_id] = line[14]
        retweets_count[tweet_id] = line[15]
        likes_count[tweet_id] = line[16]
        hashtags[tweet_id] = line[17]
        reply_to[tweet_id] = line[29]

        count += 1

    print(count)

    # calculate "score" based on how popular and how much attention the tweet got
    scores = {}
    for id, replies, retweets, likes in zip(replies_count.keys(), replies_count.values(), retweets_count.values(), likes_count.values()):
        score = int(replies) + int(retweets) + int(likes)
        scores[id] = score

    desc_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    min_score = desc_scores[int(count * 0.25)] # minimum score to be in the 75th percentile of the tweets to be deemed "popular" or "good"
    print(min_score[1])

    with open('wordcollect.csv', 'w', encoding='utf-8', newline='') as keywords:
        writer = csv.writer(keywords)
        writer.writerow(['id', 'keywords', 'score'])
        for id, score in desc_scores[:int(count * 0.25)]:
            keywords = GetInfo(text, id)
            filtered_text = remove_stopwords(keywords)
            filtered_text = strip_punctuation(filtered_text)
            filtered_text = strip_numeric(filtered_text)
            writer.writerow([id, filtered_text, score])

    def ScoreAnalysis(desc_scores, count_, dict, array_index, boundary):
        if boundary == 'upper': # top 25
            for id, score in desc_scores[:int(count * 0.25)]: # 2321 entries
                if dict[id] != '[]':
                    count_[array_index] += 1
        if boundary == 'lower': # bottom 25
            for id, score in desc_scores[int(count * 0.75):]: # 2322 entries
                if dict[id] != '[]':
                    count_[array_index] += 1
        if boundary == 'middle': # middle 50
            for id, score in desc_scores[int(count * 0.25):int(count * 0.75)]: # 4643 entries
                if dict[id] != '[]':
                    count_[array_index] += 1
        return count_

    # hastags
    count75 = ScoreAnalysis(desc_scores, count75, hashtags, 0, 'upper') # 9
    count25 = ScoreAnalysis(desc_scores, count25, hashtags, 0, 'lower') # 0
    count50 = ScoreAnalysis(desc_scores, count50, hashtags, 0, 'middle') # 5

    # photos
    count75 = ScoreAnalysis(desc_scores, count75, photos, 1, 'upper') # 362 
    count25 = ScoreAnalysis(desc_scores, count25, photos, 1, 'lower') # 9
    count50 = ScoreAnalysis(desc_scores, count50, photos, 1, 'middle') # 103

    # urls
    count75 = ScoreAnalysis(desc_scores, count75, urls, 2, 'upper') # 560
    count25 = ScoreAnalysis(desc_scores, count25, urls, 2, 'lower') # 49
    count50 = ScoreAnalysis(desc_scores, count50, urls, 2, 'middle') # 430

    # time of day? Night? Morning? Afternoon?

    # time of year? -- date






