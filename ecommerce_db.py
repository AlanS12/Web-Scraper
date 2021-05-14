import sqlite3

def db_connect(products):
    conn=sqlite3.connect("products.db")
    #conn.execute("create table if not exists Products(Name text not null, Picture text, Price real not null, Description text, Rating int, No_of_Ratings int)")
    conn.execute("create table if not exists Products(Name text not null, Price real not null, Rating int)")
    print("Table created successfully!")
    conn.close()

def set_shoe_info(products, values):
    conn=sqlite3.connect("products.db")
    print("Inserted into table: "+str(values))

    conn.execute("insert into Products values (?, ?, ?)",values)
    conn.commit()
    conn.close()

def get_shoe_info(products):
    conn=sqlite3.connect("products.db")
    cur=conn.cursor()

    cur.execute("select * from Products")
    info=cur.fetchall()

    for entry in info:
        print(entry)
    conn.close()
