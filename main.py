from bs4 import BeautifulSoup
import asyncio
import json
import time

from asyncfuntion import parse_all

def parser(url,html):
    soup = BeautifulSoup(html,"html.parser")
    tag = soup.find("html")
    output = dict(url=url,lang=None)
    if "lang" in tag.attrs:
        print("✅" + url)
        output['lang'] = tag['lang']
    else:
        print("❎" + url)
    return output

# start the timestamp
f = open("parse 5000 websites")
start = time.time()

# parse all urls
urls = json.load(open("data/the_first_5000.json"))
results = asyncio.run(parse_all(parser,urls))
print(results)

# define calculation time
end = time.time()
f.write(f"done in {end-start:,2f}")

# dump the results
json.dump(
    results,
    open("results.json","w"),
    indent=4
)

# close the f file
f.close()