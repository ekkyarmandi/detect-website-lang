from bs4 import BeautifulSoup
from math import ceil
from langdetect import detect_langs
import requests
import asyncio
import string
import random
import re
import os
os.system("cls")

from asyncfuntion import parse_all
from sql_function import query, update

def chop(list, chunk):
    max_c = ceil(len(list)/chunk)
    series = [i*chunk if i < max_c else len(list) for i in range(max_c+1)]
    chunks = [list[series[i]:series[i+1]] for i in range(len(series)-1)]
    return chunks

def parser(url, html):
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find("html")
    output = dict(domain=url,domain_language=None)
    if "lang" in tag.attrs:
        print("✅ " + url)
        output['domain_language'] = tag['lang']
    else:
        print("❎ " + url)
    return output

def lang_identifier(url, html):
    container = []
    soup = BeautifulSoup(html,"html.parser")
    page = soup.find("body")
    for line in page.strings:
        if line.strip() != "":
            punctuation = [p for p in string.punctuation if p not in ["'",'"',",","."]]
            line = "".join([a for a in line if a not in punctuation])
            line = re.sub("\s+"," ",line).strip()
            if len(line.split(" ")) > 1:
                container.append(line)
    container = list(dict.fromkeys(container))
    if len(container) > 5:
        langs = detect_langs(" ".join(container))
        langs = [dict(lang=i.lang,prob=i.prob) for i in langs]
        result = max(langs, key=lambda x: x['prob'])
        print("✅ " + url)
        return dict(
            domain=url,
            domain_language=result['lang']
        )
    else:
        print("❌ " + url)
        return dict(
            domain=url,
            domain_language=None
        )

def get(url):
    headers = {"user-agent": ""}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

if __name__ == "__main__":

    # parse all urls
    cmd = "SELECT domain FROM websites WHERE domain_language='None'"
    chunks = chop(query(cmd),80)
    for urls in chunks:
        result = asyncio.run(parse_all(lang_identifier,urls))
        for entry in result:
            if entry != None:
                update(entry)