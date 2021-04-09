"""
Downloads image thumbnails from google image search. Please note that this is a quite simple implementation with some limitations. First of all it is only possible to download low res thumbnails. Also, you can download 20 thumbnails at max.
If you need a more advanced solution please take a look at the serpAPI https://serpapi.com/images-results from google itself.

This program is published under the CC BY-SA 4.0 license.
By therealpeterpython https://github.com/therealpeterpython - 2021
"""


from pathlib import Path

import os
import shutil
import requests


def _create_url(query):
    """
    Creates the google image search url for the search term query
    """
    return "https://www.google.com/search?q={}&tbm=isch".format(query)


def _download_html(url):
    """
    Downloads the html page for the given url
    """
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    html = requests.get(url, headers=headers).text
    return html


def _get_image_links(html):
    """
    Extracts the image links from the raw html.
    """
    start_token = 'src="'
    end_token = '&amp;s'
    offset_token = "/url?q="
    offset = html.find(offset_token)
    html = html[offset:]
    links = list()
    while True:
        start = html.find(start_token)
        end = html.find(end_token, start)
        if start == -1:  # nothing found
            break
        links.append(html[start+len(start_token):end])
        html = html[end+1:]

    return links


def _download_images(query, links, num, dir):
    """
    Takes a list of image links and downloads the first num of them. If num is negativ all images will be downloaded. The dir parameter determines the folder to save the images in.
    Returns the relative paths to the images.
    """
    if num > 0:
        links = links[:num]

    os.makedirs(dir, exist_ok=True)  # create image dir
    image_paths = list()
    headers={}
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    for i, link in enumerate(links):
        try:
            req = requests.get(link, headers=headers, stream=True)
            try:
                type_guess = req.headers["Content-Type"].split("/")[1]
            except:
                type_guess = "jpg"

            file_name = "{}_{}.{}".format(query, i, type_guess).replace("/", "\\/")  # escape stuff
            file_name = str(Path(dir, file_name))
            with open(file_name, "wb") as fp:  # save image in file
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, fp)
            image_paths.append(file_name)

        except Exception as e:
            print("Failed at image {} with -> {} <-!".format(file_name, str(e)))
    return image_paths


def download(query, num=-1, dir="images"):
    """
    Main function to download images. Takes a string query to search for and downloads the first max(num, 20) images. If num < 1, all 20 images will be downloaded. The output directory is dir.
    Returns the relative paths to the images.
    """
    url = _create_url(query)
    html = _download_html(url)
    links = _get_image_links(html)
    image_paths = _download_images(query, links, num=num, dir=dir)
    return image_paths


def download_one(query):
    """
    Download one image to the standard dir "images".
    Returns the relative path to the image.
    """
    return download(query, num = 1)[0]