import matplotlib.pyplot as plt
import numpy as np
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()


# What was the most popular dish at each restaurant?
# Plot 1 bar chart for each restaurant. With all dishes per restaurant. Bar chart.
# A: Bean Juice Stand, Honey, 1185
# Johnny's Cashew Stand, Juice, 1196
# The Ice Cream Parlor, Beans, 1151
# The Restaurant at the End of the Universe, Cheese, 1158

# Direct answer
res = cur.execute("""
SELECT restaurant_name, food_name, dish_count \
FROM \
    (SELECT restaurant_name, food_name, dish_count, row_number() \
    OVER (PARTITION BY restaurant_name ORDER BY dish_count DESC) as row_number \
    FROM ( \
        SELECT restaurant_name, food_name, COUNT(*) as dish_count \
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
fig.suptitle("Top 5 popular dishes by restaurant", fontsize=16)
for i, restaurant in enumerate(restaurant_names):
    res = cur.execute(
        "SELECT food_name, COUNT(*) "
        "FROM orders "
        "WHERE restaurant_name = :restaurant "
        "GROUP BY food_name "
        "ORDER BY COUNT(*) DESC "
        "LIMIT 5",
        {"restaurant": restaurant},
    )
    res1 = res.fetchall()
    dish_names, num_orders = zip(*res1)
    x = 0.5 + np.arange(len(res1))
    bars = ax[i].bar(x, num_orders, width=1, edgecolor="white", linewidth=0.3)
    ax[i].bar_label(bars)
    ax[i].set(
        xlim=(0, 5),
        xticks=0.5 + np.arange(0, 5),
        xticklabels=dish_names,
        ylim=(1000, 1300),
        yticks=np.arange(1000, 1300, 100),
    )
    ax[i].set_xlabel(restaurant)
plt.savefig("plots/plot_3.png")
