# -*- coding: utf-8 -*-
"""TwitterSortedOccurrences.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WSV8V_NN2bXmplhkCeNfx8CLkMv6y4__
"""

# importing pandas package
import pandas as pandasForSortingCSV
import ast
import matplotlib.pyplot as plt

# assign dataset
csvData = pandasForSortingCSV.read_csv(r"/content/sample_data/TwitterdataDelimited.csv",header=None, error_bad_lines=False, encoding='unicode_escape')
csvData = csvData[1].str.split(',', expand=True)                                         
# displaying unsorted data frame
print("\nBefore sorting:")
print(csvData)
# sort data frame
csvData.sort_values(["Occurences"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True,
                    na_position='first')
  
# displaying sorted data frame
print("\nAfter sorting:")
print(csvData)

#Histogram of updated Twitter data
csvData.plot(kind='bar')
plt.ylabel('Occurrences')
plt.xlabel('Character Count')
plt.title('Character Occurence')
plt.show()

plt.pie(csvData, labels=country_data, explode=explode, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

#Pie Chart Word Occurrences
plt.title("Word Occurrences")
plt.show()