import sqlite3

conn = sqlite3.connect('wish_list.db')
# conn.execute("""CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gift TEXT, complete BOOLEAN, year TEXT)""")
cur = conn.cursor()
cur.execute("""INSERT INTO people (name, gift, complete, year) VALUES ('Christian', 'Gameboy', 'False', strftime('%Y'))""")
cur.execute("""SELECT * FROM people""")
rows = cur.fetchall()
conn.commit()
for row in rows:
    print(row)
conn.close()
