from bs4 import BeautifulSoup
from math import ceil
import asyncio
import json
import time

from asyncfuntion import parse_all

def chop(list, chunk):
    max_c = ceil(len(list)/chunk)
    series = [i*chunk if i < max_c else len(list) for i in range(max_c+1)]
    chunks = [list[series[i]:series[i+1]] for i in range(len(series)-1)]
    return chunks

def parser(url, html):
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find("html")
    output = dict(url=url,lang=None)
    if "lang" in tag.attrs:
        print("✅ " + url)
        output['lang'] = tag['lang']
    else:
        print("❎ " + url)
    return output

# start the timestamp
f = open("parse 5000 websites.txt","w")
start = time.time()

# parse all urls
results = []
urls = json.load(open("data/the_first_5000.json"))
chunks = chop(urls[:275], 50)
for urls in chunks:
    result = asyncio.run(parse_all(parser,urls))
    results.extend(result)

# define calculation time
end = time.time()
f.write(f"done in {end-start:,2f}")

# dump the results
json.dump(
    results,
    open("results.json","w"),
    indent=4
)

# close the file
f.close()