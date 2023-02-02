# Tweet Analyzer

To run:  
  
Run main.py with the provided csv. Using a different csv will require modifications to the format accepted by the main Python code, as well as changing the name the interprer accepts in the source code.
main.py will output some general analytics and scoring of tweet success based on interactions. For more info, read comments in the source code. 
  
Run a mapreduce job using Hadoop on the output from main.py using twitteranalyzer.jar. The code used to generate twitteranalyzer.jar is saved as WordCount.java.

Run twittersortedoccurence.py on the output from Hadoop. This will output data on the statistics relevant to the word count map reduce job. 
