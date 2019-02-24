import requests
import pprint
import hidden
from googleapiclient.discovery import build

# New York Times API use-case
req = 'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=' + hidden.nyt_api
response = requests.get(req)
data = response.json()
pprint.pprint(data)


# Google Books API use-case
service = build('books', 'v1', developerKey=hidden.google_api)
request = service.volumes().list(source='public', q='flowers+intitle')
response = request.execute()
pprint.pprint(response)

