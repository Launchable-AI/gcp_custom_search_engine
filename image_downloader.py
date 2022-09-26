import requests

url = "https://www.googleapis.com/customsearch/v1?"

api_key =  'YOUR API KEY HERE'
cx = 'YOUR SEARCH ENGINE ID HERE'
q = "flower"

payload = {
    "key": api_key,
    "cx": cx,
    "q": q,
    "start": '0',
    "searchType": "image"
}

list_of_urls = []

while len(list_of_urls) < 10:
    r = requests.get(url, params=payload)
    
    for item in r.json()['items']:
        list_of_urls.append(item['link'])
    payload['start'] = str(len(list_of_urls) + 1)

print(list_of_urls)
print(len(list_of_urls))

for index, url in enumerate(list_of_urls):
    # make http request to url
    r = requests.get(url)
    image = r.content

    # save content of that request to disk
    filename = f'{index}-{payload["q"]}.jpg'
    with open(filename, 'wb') as f:
        f.write(image)
