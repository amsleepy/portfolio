from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import f1_score, fbeta_score
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

def classify(xSample, ySample):
    xtrain, xtest, ytrain, ytest = train_test_split(xSample, ySample)

    clf = MultinomialNB().fit(xSample, ySample, sample_weight=1)                #apply naive bayes classifier
    scores = cross_val_score(clf, xSample, ySample, cv=2, scoring='accuracy')   #use 2fold due to dataset being on the small side

    clf.fit(xtrain, ytrain, sample_weight=1)
    ypred = clf.predict(xtest)

    f1_avg = 0       #will average scores to get a better picture of performance
    beta_avg = 0
    count = 0

    while(count < 10):
        f1_avg += f1_score(ytest, ypred, average='macro')                
        beta_avg += fbeta_score(ytest, ypred, average='macro', beta=2.0)     #weights recall over precision
        count += 1
    

    print("\nF1 Score Average Over 10 Iterations:", f1_avg/10)
    print("F2 Score Average Over 10 Iterations:", beta_avg/10)
    print("2fold Cross Val Scores:", scores)


text = open('clean.txt', 'r', encoding='utf-8')
with open('clean.txt', 'r', encoding='utf-8') as f:
    lbls = [line.split(None, 1)[0] for line in f]              #assign first word as label for each line

# count_vect = CountVectorizer()                               
tokenizer = TreebankWordTokenizer()                            #Create Tokenizer
# count_vect.set_params(tokenizer=tokenizer.tokenize)          #Using tfidf_vectorizer instead of tfidf_transformer results in marginal accuracy increase
# count_vect.set_params(ngram_range=(1,1))                     

# X_counts = count_vect.fit_transform(text)

tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.set_params(tokenizer=tokenizer.tokenize)
tfidf_vectorizer.set_params(ngram_range=(1,1))                 #ngram range of 1,1 is optimal. Setting to 1,2 drops accuracy by a at least 10%
X_tfidf = tfidf_vectorizer.fit_transform(text)

ros = RandomOverSampler()                                      #Random Over Sampling gives best accuracy
xOver, yOver = ros.fit_resample(X_tfidf, lbls)                 #Oversamples minority class as they are generally underrepresented in data
classify(xOver, yOver)