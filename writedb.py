# read database script
import sqlite3
import csv

# create connection to database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


def writetodb(token, approved, user_id):
    with conn:
        c.execute(
            """INSERT INTO myapp_verifyemail (id, token, approved, user_id) VALUES (?,?,?,?)""", (None, token, approved, user_id))
    conn.commit()
    print('Completed')


#writetodb('testestest', 0, 10)


with open('products.csv', newline='', encoding='utf-8') as f:
    fr = csv.reader(f)
    #data = list(fr)
    # print(list(fr))

    for t, a, u in fr:
        writetodb(t, int(a), int(u))

"""
to use shell instead ->
----------------------------------------------------------------
import myapp.models import VerifyEmail
import django.contrib.auth.models import User
import csv

# check directory
import os
os.listdir()

with open('file.csv', newline='', encoding='utf-8') as f:
    fr = csv.reader(f)
    data = list(fr)

for t,a,u in data:
    new = VerifyEmail()
    new.user = User.objects.get(id=int(u))
    new.token = t
    new.approved = bool(int(a))
    new.save()

"""
