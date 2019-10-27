# run.py

from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from werkzeug import secure_filename
from azure.storage.blob import BlockBlobService
import string, random, requests
import os
import json
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from tika import parser
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.search.autosuggest import AutoSuggestSearchAPI
from azure.cognitiveservices.search.autosuggest.models import (
    Suggestions,
    SuggestionsSuggestionGroup,
    SearchAction,
    ErrorResponseException
)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
ACCOUNT_NAME = 'arxivpapers'
ACCOUNT_KEY = 'KWUJnGS5h5gZNBU6d86pox02EBGaP5vF5tkhBcIx7Q7zP/rABFPtFgFZL7TLV95g71e6ElaCOG+g+7kEPF+/hQ=='
container_name ='papers'
SUBSCRIPTION_KEY = '92a11f7c8c9140feb2a415b065d641cf'
ENDPOINT = 'https://drstone.cognitiveservices.azure.com/'
credentials = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
text_analytics_url = 'https://westus.api.cognitive.microsoft.com'
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)
block_blob_service = BlockBlobService(
    account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)


#TODO: OPTION TO ADD TO READING LIST --> FEEDS INTO PERSONALIZER API

@app.route('/general')
def generalRecommend():
    #recommends based on what you've clicked/upload'
    #infinite scrolling
    #general recommendation 
    #get all files from 
    # We think you may like
    return 'Hello, World!'

readingList = []
@app.route('/myPapers', methods=['GET', 'PUT'])
def getPapers():
    generator = block_blob_service.list_blobs(container_name)
    return render_template('dashboard.html', myFiles=generator, readingList=readingList)

@app.route('/saveToReadingList', methods=['POST'])
def addPapers():
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            print(key,":",value)
            i = json.loads(key)
            readingList.append(i['value'])
    return 'OK'

@app.route('/', methods=['GET', 'PUT', 'POST'])
def paperRecommend():
    if request.method == 'POST':
        
        file = request.files['file']
        filename = file.filename
        #^if causes trouble, convert to secure_filename(file.filename)
        # fileextension = filename.rsplit('.',1)[1]
        # Randomfilename = id_generator()
        # filename = Randomfilename + '.' + fileextension
        try:
            #first call parseAbstract
            file.save("temp/" + filename)
            tempLocation = "temp/" + filename 
            block_blob_service.create_blob_from_stream(container_name, filename, file)
            tags = keyPhrases(tempLocation)

        except Exception:
            print('Exception=' + Exception)
            pass
        raw = parser.from_file(tempLocation)
        raw = raw['content']
        recs = recommendationModel(raw)
        #ref =  'https://'+ ACCOUNT_NAME + '.blob.core.windows.net/' + container_name + '/' + filename
        
        arr =  tags
        realTag = getAutosuggestions(tags[0])
        websearches = getBing(realTag)
        #call searchFor(tags)
        #df = pandas.read_csv('tags.csv')
        # convert df to dict and see if the tags from uploaded file exist in tags
        title='Example'
        return render_template('listRecommendations.html',tags=tags,websearches=websearches,recommendations=recs)
    return render_template('upload.html')

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def keyPhrases(fileLocation):
    raw = parser.from_file(fileLocation)
    raw = raw['content']
    documents = [
        {
            "id": "1",
            "language": "en",
            "text": raw
                    
        }
    ]
    response = text_analytics.key_phrases(documents=documents)
    phrases = []
    #but for later compare more tags (like maybe 5)
    for document in response.documents:

        length = len(document.key_phrases)
        i = 0
        while i < 6 and i < length:
            print("phrase:", document.key_phrases[i])
            phrases.append(document.key_phrases[i])
            i+=1
    return phrases

def findSimilarIndices(tags, df):
    for tag in tags:
        df[tag] #find its index
        #path_df

def getBing(firstTag):
    #based on very first tag generated, do the tag    
    subkey = 'ac4be630084d4433855037234a2a3b80'
    
    #declare client
    dict = {}
    client = WebSearchAPI(CognitiveServicesCredentials(subkey))
    web_data = client.web.search(query=firstTag)
    print("Searched for Query:  " + firstTag)
    if web_data.web_pages.value:
        length = len(web_data.web_pages.value)
        i = 0
        while i < length and i < 6:
            page = web_data.web_pages.value[i]
            title = page.name
            url = page.url
            print(title, url)
            dict[url] = title
            i+=1
    
    return dict

def getAutosuggestions(firstTag):
    subkey= '09b282e0bff649be998cfb5485e528e5'
    client = AutoSuggestSearchAPI(
        CognitiveServicesCredentials(subkey))
    suggestions = client.auto_suggest(
            query=firstTag)  # type: Suggestions
    if suggestions.suggestion_groups:
        suggestion_group = suggestions.suggestion_groups[0]  # type: SuggestionsSuggestionGroup
        for suggestion in suggestion_group.search_suggestions:  # type: SearchAction
            print("suggestion:", suggestion.query)
            return suggestion.query

def recommendationModel(allText):
    #return  a dict of title to score of recommendations (10)
    recommendations = []
    num = 10
    df = pd.read_csv('path2.csv')
    df.drop(columns=['id'],inplace=True)
    df.rename(columns={'Unnamed: 0':'id'}, inplace=True)
    dicts = [{'id': len(df), 'title':' ','categories': 'cs.lg', 'abstract': allText, 'doi': '0', 
          'created': '2019-09-06' , 'updated':'2019-09-06', 'authors': 'none'}]
    df = df.append(dicts, ignore_index=True, sort=False)
    #print(df.loc[df['id'] == 11]['title'])
    #print(df['title'][1].split(" "))
    
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['abstract'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 

    results = {}
    for idx, row in df.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
        similar_items = [(cosine_similarities[idx][i], df['id'][i]) for i in similar_indices] 
        results[row['id']] = similar_items[1:]
    id = len(df)-1
    recs = results[id][:num]
    for rec in recs: 
        print('score', rec[0]) #score
        print('title', df.loc[df['id'] == rec[1]]['title'].values )
        recommendations.append([str(df.loc[df['id'] == rec[1]]['title'].values)[2:-2], rec[0]*1000]) 
    return recommendations