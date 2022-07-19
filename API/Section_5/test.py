import sqlite3


connection = sqlite3.connect('data.db')

cursor = connection.cursor()


create_table = "CREATE TABLE IF NOT exists users (id int, username text, password text)"


cursor.execute(create_table)



user = [(1,'aayush','aaa'),
        (2,'abc','bcd')]

insert ="INSERT INTO users VALUES (?,?,?)"
cursor.executemany(insert,user)

# cursor.execute(insert,user)




select = "select * from users"
for row in cursor.execute(select):
        print(row)

connection.commit()

connection.close()
