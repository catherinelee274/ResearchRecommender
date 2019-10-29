#run microsoft azure text analytics
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import pandas
from tika import parser
import nltk
from nltk.corpus import stopwords
#nltk.download("stopwords")
#set(stopwords.words('english'))
import pandas


SUBSCRIPTION_KEY = '92a11f7c8c9140feb2a415b065d641cf'
ENDPOINT = 'https://drstone.cognitiveservices.azure.com/'
credentials = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
text_analytics_url = 'https://westus.api.cognitive.microsoft.com'
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

df = pandas.read_csv('path2.csv')

dict = {}
x = 0
for index, row in df.iterrows():
    print(index)
    abstract = row['abstract']
    #filtered_words = list(filter(lambda word: word not in stopwords.words('english'), abstract))
    #print(filtered_words)
    #remove stop words

    documents = [
        {
            "id": "1",
            "language": "en",
            "text": abstract
                    
        }
    ]
    response = text_analytics.key_phrases(documents=documents)
    for document in response.documents:
        length = len(document.key_phrases)
        i = 0
        while i < 5 and i < length:
            if document.key_phrases[i] in dict:
                dict.get(document.key_phrases[i]).append(index)
                print(document.key_phrases[i], dict.get(document.key_phrases[i]))
            else:
                arr = [index]
                dict[document.key_phrases[i]] = arr
                #rint(dict)
            i+= 1
    x+= 1
    if x > 5000:
        break

import csv
csv_columns = ['tag','index']
csv_file = "tags2.csv"
try:
    with open(csv_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for key in dict.keys():
            f.write("%s,%s\n"%(key,dict[key]))
except IOError:
    print("I/O error") 
        