import csv
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()


cur.execute("DROP TABLE orders")
cur.execute("CREATE TABLE orders(restaurant_name, food_name, first_name, food_cost)")

# Load file to database
with open("data/data.csv") as csvfile:
    for row in csv.DictReader(csvfile):
        params = (
            row["restaurant_names"],
            row["food_names"],
            row["first_name"],
            row["food_cost"],
        )
        cur.execute("INSERT INTO orders VALUES(?, ?, ?, ?)", params)
        con.commit()

# Print number of entries loaded
res = cur.execute("SELECT COUNT(*) FROM orders")
print(res.fetchone())
