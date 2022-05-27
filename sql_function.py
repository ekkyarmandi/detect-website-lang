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


if __name__ == "__main__":

    # field = dict(
    #     url="TEXT UNIQUE",
    #     lang="TEXT"
    # )

    # create_table("websites",field)


    from rich.progress import track

    urls = json.load(open("data/the_first_5000.json"))
    for url in track(urls):
        insert(dict(url=url,lang=None))