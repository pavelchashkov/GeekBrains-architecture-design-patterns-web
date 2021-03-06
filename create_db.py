import sqlite3

connection = sqlite3.connect('app.sqlite')
cursor = connection.cursor()
with open('create_db.sql', 'r') as f:
    sql_text = f.read()
cursor.executescript(sql_text)
cursor.close()
connection.close()