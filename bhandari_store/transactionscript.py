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
    sql1 = "SELECT sellingprice, pl, quantity, date, remark, totalamount, product FROM 'transaction' WHERE sn=?"
    result_from_pasal = c.execute(sql1, (x,))
    for r in result_from_pasal:
        sp = r[0]
        pl = r[1]
        qt = r[2]
        dt = r[3]
        rm = r[4]
        ttl = r[5]
        prd = r[6]
        cart_id = x

    sql2 = "SELECT ID FROM products WHERE name=?"
    result_backend = c.execute(sql2, (prd, ))
    for r2 in result_backend:
        pid = r2[0]

    #insert into the database
    sql3 = "INSERT INTO shop_transaction (selling_price, profit_or_loss, sold_on, remark,  total_amount, product_id, quantity, cart_id) VALUES(?,?,?,?,?,?,?,?)"
    cursor.execute(sql3, (sp, pl, dt, rm, ttl, pid, qt, x))
    connection.commit()
    print("Added " + str(x))
    x += 1
    
