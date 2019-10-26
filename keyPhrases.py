#run microsoft azure text analytics
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY = '92a11f7c8c9140feb2a415b065d641cf'

ENDPOINT = 'https://drstone.cognitiveservices.azure.com/'


credentials = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
text_analytics_url = 'https://westus.api.cognitive.microsoft.com'
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)


#MAKE NOT HARDCODEED
documents = [
    {
        "id": "1",
        "language": "en",
        "text": "We present a model that generates natural language descriptions of images and their regions. Our approach leverages datasets of images and their sentence descriptions to learn about the inter-modal correspondences between language and visual data. Our alignment model is based on a "
                + "novel combination of Convolutional Neural Networks over " +
                "image regions, bidirectional Recurrent Neural Networks " +
                 "over sentences, and a structured objective that aligns the " +
                 "two modalities through a multimodal embedding. We then " +
                 "describe a Multimodal Recurrent Neural Network architecture that uses the inferred alignments to learn to generate " +
                 "novel descriptions of image regions. We demonstrate that " +
                 "our alignment model produces state of the art results in retrieval experiments on Flickr8K, Flickr30K and MSCOCO " +
                 "datasets. We then show that the generated descriptions significantly outperform retrieval baselines on both full images " +
                "and on a new dataset of region-level annotations."
                
    }
]
response = text_analytics.key_phrases(documents=documents)

#PRINT ONLY the first 3 (the more important phrases come earlier)

#but for later compare more tags (like maybe 5)
for document in response.documents:
    print("Document Id: ", document.id)
    print("\tKey Phrases:")
    length = len(document.key_phrases)
    i = 0
    while i < 4 and i < length:
        print("\t\t", document.key_phrases[i])
        i+=1