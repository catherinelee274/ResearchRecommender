#find key phrases from a string
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY = ''

ENDPOINT = ''


credentials = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
text_analytics_url = ''
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)


from tika import parser

raw = parser.from_file('karpathyshort.pdf')
raw = raw['content']

documents = [
    {
        "id": "1",
        "language": "en",
        "text": raw
                
    }
]
response = text_analytics.key_phrases(documents=documents)
#PRINT ONLY the first 4 (the more important phrases come earlier)

#but for later compare more tags (like maybe 5)
for document in response.documents:
    print("Document Id: ", document.id)
    print("\tKey Phrases:")
    length = len(document.key_phrases)
    i = 0
    while i < 5 and i < length:
        print("\t\t", document.key_phrases[i])
        i+=1