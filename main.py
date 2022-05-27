from bs4 import BeautifulSoup
from math import ceil
import asyncio
import json
import time

from asyncfuntion import parse_all
from sql_function import query_all, update

def chop(list, chunk):
    max_c = ceil(len(list)/chunk)
    series = [i*chunk if i < max_c else len(list) for i in range(max_c+1)]
    chunks = [list[series[i]:series[i+1]] for i in range(len(series)-1)]
    return chunks

def parser(url, http, html):
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find("html")
    output = dict(url=url,http=http,lang=None)
    if "lang" in tag.attrs:
        print("✅ " + url)
        output['lang'] = tag['lang']
    else:
        print("❎ " + url)
    return output

# start the timestamp
start = time.time()
with open("parse 5000 websites.txt","a") as f:

    # parse all urls
    results = []
    count = 0
    chunks = chop(query_all(),30)
    for urls in chunks:
        result = asyncio.run(parse_all(parser,urls))
        for entry in result:
            if entry != None:
                update(entry)
                count += 1

    # define calculation time
    end = time.time()
    f.write(f"{count} {end-start:.2f} sec\n")