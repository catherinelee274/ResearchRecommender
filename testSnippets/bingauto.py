#autosuggest
from azure.cognitiveservices.search.autosuggest import AutoSuggestSearchAPI
from azure.cognitiveservices.search.autosuggest.models import (
    Suggestions,
    SuggestionsSuggestionGroup,
    SearchAction,
    ErrorResponseException
)
from msrest.authentication import CognitiveServicesCredentials

subkey= ''

client = AutoSuggestSearchAPI(
        CognitiveServicesCredentials(subkey))

suggestions = client.auto_suggest(
            query="convolutional")  # type: Suggestions

if suggestions.suggestion_groups:
    suggestion_group = suggestions.suggestion_groups[0]  # type: SuggestionsSuggestionGroup
    #print(suggestion_group.search_suggestions[1].display_text)
    for suggestion in suggestion_group.search_suggestions:  # type: SearchAction
        print(suggestion.query)
        break
