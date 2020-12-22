# read database script
import sqlite3
import csv
# create connection to database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

with conn:
    c.execute("""SELECT * FROM myapp_products""")
    #c.execute("""SELECT * FROM myapp_products WHERE id=3""")
    data = c.fetchall()
    #data = c.fetchmany(3)
    #data = c.fetchone()
    # print(data)
# export db to csv file
with open('products.csv', 'w', newline='', encoding='utf-8') as f:
    fw = csv.writer(f)
    fw.writerows(data)
