import os
import uuid
from pathlib import Path
import argparse
import typing
from typing import List

import requests

'''
Script to download images using Google's Custom Search Engine API

Steps:
1. Set query string params as payload
2. Use the requests module to retrieve 100 urls, looping 10 times
    - store resulting links in an array
3. Use links array (img_urls) to fetch images, and save to filesystem

reference api call from docs
GET https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures

IMPORTANT - replace values below with your key and cx values
key = your API key
cx = your custom search engine id
note - could set up argparse to allow 'q' to be set from command line, if desired
'''


def get_urls(q: str='flower'):
    ''' Generate a list of URLs, that can later be used to download files
    '''

    # create an array to hold list of urls for images
    img_urls: List(str) = []

    api_key =  'YOUR API KEY HERE'
    custom_search_engine_id = 'YOUR SEARCH ENGINE ID HERE'

    payload: dict = {'key': api_key,
                    'cx': custom_search_engine_id,
                    'searchType': 'image',
                    'start': '0',
                    'q': q}


    # Get Image URLs from google search
    while len(img_urls) < 10:
        print(f'Current number of images in list": {len(img_urls)}')

        # make request to your Custom Search Engine
        resp: Requests.Response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)

        #convert response item to json (method from requests)
        results: List['dict'] = resp.json()['items']

        # iterate over results, add img urls to list
        for result in results:
              img_urls.append(result['link'])

        # start next loop at a number 1 greater than the number of images in the list
        payload['start']: str = str(len(img_urls) + 1)

    return img_urls

def mkdir():
    ''' Create a randomly named directory for the files
    '''

    dir_name = str(uuid.uuid4())
    os.mkdir(dir_name)
    return(dir_name)

def get_ext(url):
    ''' Grab content type header, and use it to return extenion
    '''
    try:
        header_request = requests.head(url, allow_redirects=True, timeout=6)
        content_type = header_request.headers.get('content-type')

        if 'jpeg' in content_type.lower():
            ext = ".jpg"
        elif 'png' in content_type.lower():
            ext = ".png"
        else:
            ext = None

    except:
        ext = None

    return ext

def download_image(url: str):
    ''' Retrieve image content
    '''
    request = requests.get(url, timeout=6)
    return request.content


def save_image(image, ext):
    ''' Save image content to random filepath location
    '''
    file_name = str(uuid.uuid4()) + ext
    filepath = Path(dir_name + '/' + file_name)
    print(f'Saving image to: {filepath}')

    with open(filepath, 'wb') as f:
        f.write(image)

def get_imgs(img_urls):
    ''' Download and save images from URLs

    Serves as wrapper function for most of the script
    '''

    for url in img_urls:
        print(f'Processing: {url}')

        # Determine img type from header, so we know what extension to save it as
        ext = get_ext(url)

        # if header is None, we don't download file
        if ext is not None:
            try:
                image = download_image(url)
                save_image(image, ext)
            except:
                pass
        else:
            # if content-type is none, don't save file
            img_urls.remove(url)


if __name__ == "__main__":
    # set up command line argument parsing
    parser = argparse.ArgumentParser(description='Parse search term.')
    parser.add_argument('-q', '--query', type=str, help='keyword to search for')
    args = parser.parse_args()

    img_urls = get_urls(q=args.query)
    dir_name = mkdir()
    get_imgs(img_urls)



