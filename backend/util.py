import sqlite3

conn = sqlite3.connect('stocks.db')
curr = conn.cursor()

def create_tables():
    curr.execute("CREATE TABLE sales (ticker text, year integer, percent real, value real, PRIMARY KEY (ticker, year))")
    curr.execute("CREATE TABLE eps (ticker text, year integer, percent real, value real, PRIMARY KEY (ticker, year))")
    curr.execute("CREATE TABLE equity (ticker text, year integer, percent real, value real, PRIMARY KEY (ticker, year))")
    curr.execute("CREATE TABLE cash (ticker text, year integer, percent real, value real, PRIMARY KEY (ticker, year))")
    conn.commit()
    print("Successfully created tables.")

def drop_tables():
    curr.execute("DROP TABLE sales")
    curr.execute("DROP TABLE eps")
    curr.execute("DROP TABLE equity")
    curr.execute("DROP TABLE cash")
    conn.commit()
    print("Successfully dropped tables.")

def upload_snp500():
    import json
    json_data = open('snp.json', 'r').read()

    data = json.loads(json_data)
    tickers = [(d['Symbol'],) for d in data]
    curr.executemany("INSERT INTO stocks VALUES (?)", tickers)
    conn.commit()
    curr.execute("SELECT * FROM stocks")
    stocks = curr.fetchall()
    print(stocks)