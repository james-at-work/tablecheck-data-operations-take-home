import matplotlib.pyplot as plt
import numpy as np
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()


# Q4: What was the most profitable dish at each restaurant?
# A4: Bean Juice Stand, Honey, 5945.5
# Johnny's Cashew Stand, Juice, 5989.0
# The Ice Cream Parlor, Coffee, 5789.5
# The Restaurant at the End of the Universe, Cheese, 5861.5

# Direct answer
res = cur.execute("""
    SELECT restaurant_name, food_name, dish_cost \
    FROM \
        (SELECT restaurant_name, food_name, dish_cost, row_number() \
        OVER (PARTITION BY restaurant_name ORDER BY dish_cost DESC) as row_number \
        FROM ( \
            SELECT restaurant_name, food_name, SUM(food_cost) as dish_cost \
            FROM orders \
            GROUP BY restaurant_name, food_name)) \
    WHERE row_number = 1
    ORDER BY restaurant_name
    """)
res1 = res.fetchall()
restaurant_names, _, _ = zip(*res1)
print(res1)


# Plot
fig, ax = plt.subplots(4, 1, constrained_layout=True)
fig.suptitle("Top 5 dishes by revenue per restaurant", fontsize=16)
for i, restaurant in enumerate(restaurant_names):
    res = cur.execute(
        "SELECT food_name, SUM(food_cost) AS revenue "
        "FROM orders "
        "WHERE restaurant_name = :restaurant "
        "GROUP BY food_name "
        "ORDER BY revenue DESC "
        "LIMIT 5",
        {"restaurant": restaurant},
    )
    res1 = res.fetchall()
    print(res1)
    dish_names, revenue = zip(*res1)
    x = 0.5 + np.arange(len(res1))
    bars = ax[i].bar(x, revenue, width=1, edgecolor="white", linewidth=0.3)
    ax[i].bar_label(bars)
    ax[i].set(
        xlim=(0, 5),
        xticks=0.5 + np.arange(0, 5),
        xticklabels=dish_names,
        ylim=(5600, 6100),
        yticks=np.arange(5600, 6100, 100),
    )
    ax[i].set_xlabel(restaurant)
plt.savefig("plots/plot_4.png")
