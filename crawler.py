"""
Crawler scirpt

This crawler is used to crawl data from wikipedia site.
Must create a directory Data beforeahnd to run the crawler
"""
from bs4 import BeautifulSoup
import os
import requests

scraped_urls = {}
titles = {}

def scraping(url, site, depth):
    """Recursive crawler."""
    if depth < 0:
        return None
    print(url)
    while 1:
        try:
            req = requests.get(url)
            break
        except:
            continue

    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        title = soup.find(id="firstHeading").text
        content = soup.find(id="mw-content-text").find_all("p")
        content = list(map(lambda x: x.text, content))
    except: 
        return None
    titles[title] = (url, content)

    print(title)
    print(depth)

    entries = soup.find(id="mw-content-text").find_all("a")
    temp_url = set()
    for entry in entries:
        if not entry.has_attr("href"):
            continue
        # check href start "/wiki"
        if entry["href"].find("/wiki") == -1:
            continue
        # check not a Category page - remove if want to crawl (take significantly longer to run - more entry)
        if entry["href"].find("Category:") >= 0:
            continue
        if entry["href"].find("File:") >= 0:
            continue
        if entry["href"].find("Help:") >= 0:
            continue
        if entry["href"].find("Template:") >= 0:
            continue
        if entry["href"].find("Wikipedia:") >= 0:
            continue
        if entry["href"].find("Special:") >= 0:
            continue
        if entry["href"].index("/wiki") != 0:
            continue
        # remove duplicate
        if scraped_urls.get(site + entry["href"] , None):
            continue
        # if depth is about to go to 0, assigned scarped flag to False 
        # this will make sure if the url appears on higher lv while 
        # scarping another url, it will be scraped
        if depth >= 1:
            scraped_urls[site + entry["href"]] = True
        else:
            scraped_urls[site + entry["href"]] = False
        temp_url.add(site + entry["href"])
    for url in temp_url:
        scraping(url, site, depth - 1)
    


site = "https://simple.wikipedia.org"
# initial starting site
url = "https://simple.wikipedia.org/wiki/Reddit"
title = set()
scraping(url, site, depth=3)

working_directory = os.getcwd()

for k, v in titles.items():
    file_name = k.replace("/", "_").replace('"', "'")
    f = open(
        working_directory + f'\\Data\\{file_name}.txt',
        "w",
        encoding="utf-8",
    )
    f.write(f"{k}\n\nlink: {v[0]}\n\n")
    for paragraph in v[1][:-1]:
        f.write(f"{paragraph}")
    f.close()

