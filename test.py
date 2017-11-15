import sqlite3

conn = sqlite3.connect('wishlist.db')
# conn.execute("""CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, complete BOOLEAN, year TEXT)""")
cur = conn.cursor()
# cursor.execute("""INSERT INTO people (name, complete, year) VALUES ('Christian', 'False', strftime('%Y'))""")
cur.execute("""SELECT * FROM people""")
rows = cur.fetchall()
conn.commit()
for row in rows:
    print(row[1])
conn.close()
