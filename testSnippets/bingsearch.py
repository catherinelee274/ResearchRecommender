#using bing search api
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials



subkey = ''
firstTag = 'neural networks'
#declare client
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
        i+=1