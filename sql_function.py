from rich.progress import track
from pandas import DataFrame
import sqlite3
import json

def create_table(table: str, field: dict) -> None:
    field = [key+" "+value for key,value in field.items()]
    field = ",".join(field)
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"""CREATE TABLE {table} (
            {field}
        )
        """
        cur.execute(cmd)
        con.commit()

def insert(entries: dict, table: str = "websites"):
    n = len(entries)
    columns = ",".join([*entries])
    value = ",".join(["?" for _ in range(n)])
    values = [*entries.values()]
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"""INSERT or IGNORE into {table} ({columns}) VALUES ({value})"""
        cur.execute(cmd,(*values,))
        con.commit()

def update(entry: dict, table: str = "websites"):
    for k,v in entry.items():
        entry[k] = v if v!=None else "None"
    values = ",".join([f"{k}='{v}'" for k,v in entry.items() if k!='url'])
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"""UPDATE {table} SET {values} WHERE url=?"""
        cur.execute(cmd,(entry['url'],))
        con.commit()

def query_all(table: str = "websites"):
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"SELECT url FROM {table} WHERE lang IS NULL;"
        cur.execute(cmd)
        queries = cur.fetchall()
    return [j[0] for j in queries]

def to_csv(filename: str, table: str = "websites"):
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"SELECT url,lang FROM {table};"
        cur.execute(cmd)
        queries = cur.fetchall()
        dataframe = DataFrame(queries)
        dataframe.columns = ["url","language"]
        dataframe.to_csv(filename, index=False)


if __name__ == "__main__":

    # # create new table
    # field = dict(
    #     url="TEXT UNIQUE",
    #     http="TEXT",
    #     lang="TEXT"
    # )

    # create_table("websites",field)

    # load urls into database
    # urls = json.load(open("data/the_first_5000.json"))
    # for url in track(urls):
    #     insert(dict(url=url,lang=None))

    # query test
    to_csv(filename="example_5000websites.csv")