import csv
import operator
from gensim.parsing.preprocessing import remove_stopwords

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

print("\n********** TWEET ANALYSIS **********")

with open('elonmusk2015to2020.csv', 'r') as csv_file:
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

    # calculate "score" based on how popular and how much attention the tweet got
    scores = {}
    for id, replies, retweets, likes in zip(replies_count.keys(), replies_count.values(), retweets_count.values(), likes_count.values()):
        score = int(replies) + int(retweets) + int(likes)
        scores[id] = score

    desc_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    min_score = desc_scores[int(count * 0.25)] # minimum score to be in the 75th percentile of the tweets to be deemed "popular" or "good"
    print("Mininum Score = " + str(min_score[1]))

    # write to csv for keyword analysis
    with open('wordcollect.csv', 'w') as keywords:
        writer = csv.writer(keywords)
        writer.writerow(['id', 'keywords', 'score'])
        for id, score in desc_scores[:int(count * 0.25)]:
            keywords = GetInfo(text, id)
            filtered_text = remove_stopwords(keywords)
            writer.writerow([id, filtered_text, score])
    
    # counts how many entries are present in the top 25, bottom 25, and the rest of the dataset
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

    def PercentageAnalysis(count_, index, boundary, factor, percentile):
        percentage = float(count_[index] / len(boundary))
        countPercentage = float(count_[index] / count)
        if percentile == '75th' or percentile == '25th':
            print("Amount of Tweets that contain " + factor + " in the " + percentile + " percentile = " + str(count_[index]) + " (" + str(percentage) + ")" + " (" + str(countPercentage) + ")")
        else:
            print("Amount of Tweets that contain " + factor + " in between the 25th and 75th percentile = " + str(count_[index]) + " (" + str(percentage) + ")" + " (" + str(countPercentage) + ")")


    # hastags
    print("\n")
    print("Hashtag Score Analysis:")
    count75 = ScoreAnalysis(desc_scores, count75, hashtags, 0, 'upper') # 9
    count25 = ScoreAnalysis(desc_scores, count25, hashtags, 0, 'lower') # 0
    count50 = ScoreAnalysis(desc_scores, count50, hashtags, 0, 'middle') # 5

    PercentageAnalysis(count75, 0, desc_scores[:int(count * 0.25)], 'Hastags', '75th')
    PercentageAnalysis(count25, 0, desc_scores[int(count * 0.75):], 'Hastags', '25th')
    PercentageAnalysis(count50, 0, desc_scores[int(count * 0.25):int(count * 0.75)], 'Hastags', '50th')

    # photos
    print("\n")
    print("Photos Score Analysis:")
    count75 = ScoreAnalysis(desc_scores, count75, photos, 1, 'upper') # 362 
    count25 = ScoreAnalysis(desc_scores, count25, photos, 1, 'lower') # 9
    count50 = ScoreAnalysis(desc_scores, count50, photos, 1, 'middle') # 103

    PercentageAnalysis(count75, 1, desc_scores[:int(count * 0.25)], 'Photos', '75th')
    PercentageAnalysis(count25, 1, desc_scores[int(count * 0.75):], 'Photos', '25th')
    PercentageAnalysis(count50, 1, desc_scores[int(count * 0.25):int(count * 0.75)], 'Photos', '50th')


    # urls
    print("\n")
    print("URLs Score Analysis:")
    count75 = ScoreAnalysis(desc_scores, count75, urls, 2, 'upper') # 560
    count25 = ScoreAnalysis(desc_scores, count25, urls, 2, 'lower') # 49
    count50 = ScoreAnalysis(desc_scores, count50, urls, 2, 'middle') # 430

    PercentageAnalysis(count75, 2, desc_scores[:int(count * 0.25)], 'URLs', '75th')
    PercentageAnalysis(count25, 2, desc_scores[int(count * 0.75):], 'URLs', '25th')
    PercentageAnalysis(count50, 2, desc_scores[int(count * 0.25):int(count * 0.75)], 'URLs', '50th')
    print("\n")








