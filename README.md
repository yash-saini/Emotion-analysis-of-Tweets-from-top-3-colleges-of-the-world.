# Opinion-Mining-of-Tweets-from-top-3-colleges-of-the-world.
The project caters to finding the 5 sentiment scores (Happiness,Fear,Anger, Disgust,Sadness) of each college's tweet using a described formula. The colleges used here are Harvard, MIT and Stanford.
The scores are assigned on the basis of Adverbs or verbs followed by an adjective.
# Downloading the tweets
The tweets are downloaded using Twitter API.

# Preprocessing 
The tweets are cleaned by removing @,http,RT, punctuations etc. Stop words are removed, Non english alphabets are also removed.

# POS Tagging
Using the nltk library of POS tagging, the tweets are POS tagged and only verbs, Adverbs or Adjectives are retained.

# Scoring 
For the purpose of scoring a research based Database of adjectives (1000 words) having their sentiment scores is used along with other databases for verbs and Adverbs. The formula is taken from the mentioned Research Paper.
The method of scoring stems from the fact that a sequence of Adverb/verb followed by an adjective greatly enhances the sentimental value of the adjective. 

# Machine Learning. 
The POS sequence of tweets after Bag of Words is used ; is fed to classifers like KNN, SVM and Naive Bayes to compare their accuracies.

