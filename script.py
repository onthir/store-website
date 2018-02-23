import sqlite3
import datetime
#get the contents of the databse

conn = sqlite3.connect('database.db')
c = conn.cursor()

#second main database
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()
"""
name, stock, selling price, costprice, totalcp, totalsp, expiry_date, added_date
left_amount
"""
x = 1
while True:
    sql1 = "SELECT name, stock, price, expiry_date FROM products WHERE ID=?"
    result_from_pasal = c.execute(sql1, (x,))
    for r in result_from_pasal:
        name = r[0]
        stock = r[1]
        edate = r[3]

    sql2 = "SELECT costprice, sellingprice, totalcp, totalsp, pl, left_amount FROM backend WHERE ID=?"
    result_backend = c.execute(sql2, (x, ))
    for r2 in result_backend:
        cp = r2[0]
        sp = r2[1]
        totalcp = r2[2]
        totalsp = r2[3]
        pl = r2[4]
        left = r2[5]

    #insert into the database
    added_date = datetime.datetime.now().date()
    slug = name.replace(" ", "-")
    sql3 = "INSERT INTO shop_product (name, cost_price, selling_price, stocks, totalcp, totalsp,  assumed_profit,left_amount, exipry_date, added_date, slug) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(sql3, (name, cp, sp, stock, totalcp, totalsp, pl,left, edate, added_date, slug))
    connection.commit()
    print("Added " + str(x))
    x += 1
    
