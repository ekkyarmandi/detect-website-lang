from venv import create
from rich.progress import track
from pandas import DataFrame
import sqlite3
import json

def value2str(dict):
    list = []
    for value in dict.values():
        if type(value) == str and value != "NULL":
            value = '"' + value + '"'
        elif value == None:
            value = "None"
        list.append(value)
    return ",".join(list)

def create_table(table: str, field: dict) -> None:
    field = [key+" "+value for key,value in field.items()]
    field = ",".join(field)
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"""CREATE TABLE {table} ({field})"""
        cur.execute(cmd)
        con.commit()

def insert(entry: dict, table: str = "websites"):
    columns = ",".join([*entry])
    values = value2str(entry)
    try:
        with sqlite3.connect("data/websites.db") as con:
            cur = con.cursor()
            cmd = f"INSERT or IGNORE into {table} ({columns}) VALUES ({values})"
            cur.execute(cmd)
            con.commit()
    except:
        with open("data/failed.txt","a",encoding="utf-8") as f:
            f.write(str(entry)+"\n")

def update(entry: dict, table: str = "websites"):
    values = ",".join([f"{k}='{v}'" for k,v in entry.items() if k!='domain'])
    with sqlite3.connect("data/websites.db") as con:
        try:
            cur = con.cursor()
            cmd = f"UPDATE {table} SET {values} WHERE domain=?"
            cur.execute(cmd,(entry['domain'],))
            con.commit()
        except:
            print(entry['domain'])

def query_all(table: str = "websites"):
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"SELECT domain FROM {table} WHERE domain_language IS NULL LIMIT 50000;"
        cur.execute(cmd)
        queries = cur.fetchall()
    return [j[0] for j in queries]

def query(cmd: str) -> list:
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cur.execute(cmd)
        queries = cur.fetchall()
    return [j[0] for j in queries]

def export(filename: str, table: str = "websites"):
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"SELECT url,lang FROM {table};"
        cur.execute(cmd)
        queries = cur.fetchall()
        dataframe = DataFrame(queries)
        dataframe.columns = ["url","language"]
        if filename.endswith("csv"):
            dataframe.to_csv(filename, index=False)
        elif filename.endswith("xlsx"):
            dataframe.to_excel(filename, index=False)


if __name__ == "__main__":

    # create new table
    columns = [
        "source",
        "domain",
        "site",
        "usd_spent",
        "usd_revenue",
        "company",
        "vertical",
        "tranco",
        "page_rank",
        "majestic",
        "umbrella",
        "telephones",
        "emails",
        "twitter",
        "facebook",
        "linkedin",
        "google",
        "pinterest",
        "github",
        "instagram",
        "vk",
        "vimeo",
        "youtube",
        "tiktok",
        "people",
        "city",
        "state",
        "zip",
        "country",
        "first_detected",
        "last_found",
        "first_indexed",
        "last_indexed",
        "exclusion",
        "compliance",
        "domain_language"
    ]
    field = {key:'"TEXT"' for key in columns}
    create_table("websites",field)

    # load urls into database
    # urls = json.load(open("data/the_first_5000.json"))
    # for url in track(urls):
    #     insert(dict(url=url,lang=None))

    # query test
    # export(filename="output/example_5000websites.xlsx")