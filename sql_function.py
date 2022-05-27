from rich.progress import track
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

def insert(entries: dict, table: str="websites"):
    n = len(entries)
    columns = ",".join([*entries])
    value = ",".join(["?" for _ in range(n)])
    values = [*entries.values()]
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"""INSERT or IGNORE into {table} ({columns}) VALUES ({value})"""
        cur.execute(cmd,(*values,))
        con.commit()

def query_all(table: str = "websites"):
    with sqlite3.connect("data/websites.db") as con:
        cur = con.cursor()
        cmd = f"SELECT url FROM {table} WHERE lang IS NULL;"
        cur.execute(cmd)
        queries = cur.fetchall()
    return [j[0] for j in queries]


if __name__ == "__main__":

    # create new table
    # field = dict(
    #     url="TEXT UNIQUE",
    #     lang="TEXT"
    # )

    # create_table("websites",field)

    # load urls into databaes
    # urls = json.load(open("data/the_first_5000.json"))
    # for url in track(urls):
    #     insert(dict(url=url,lang=None))

    # query test
    urls =  query_all()
    print(urls)