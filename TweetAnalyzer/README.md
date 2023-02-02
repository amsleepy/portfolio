# Tweet Analyzer

To run:  
  
Run main.py with the provided csv. Using a different csv will require modifications to the format accepted by the main Python code, as well as changing the name the interprer accepts in the source code.
main.py will output some general analytics and scoring of tweet success based on interactions. For more info, read comments in the source code. 
  
Run a mapreduce job using Hadoop on the output from main.py using twitteranalyzer.jar. The code used to generate twitteranalyzer.jar is saved as WordCount.java.

Run twittersortedoccurence.py on the output from Hadoop. This will output data on the statistics relevant to the word count map reduce job. 

The goal of this project was to implement Twitter analytics we deemed lacking in the current build of Twitter and/or interesting to look at. It computes a basic score
for each Tweet in the dataset given based on how many interactions it generates, and a count of each word used in the dataset's Tweets is generated via Hadoop mapreduce
for efficient data processing. The end result is a list of the most successful (i.e. tweets with the most interactions) tweets in the dataset and a list of the most 
used words in said tweets (with stop words removed). 

This code was developed collaboratively with two other students over the course of a semester for a Big Data class. 
