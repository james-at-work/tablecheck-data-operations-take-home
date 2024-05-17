import matplotlib.pyplot as plt
import numpy as np
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()


# Q2: How much money did the "Restaurant at the end of the universe" make?
# A2: 186944.0

# Direct answer
res = cur.execute(
    "SELECT SUM(food_cost) FROM orders WHERE restaurant_name = 'the-restaurant-at-the-end-of-the-universe'"
)
print(res.fetchone())

# Plot
res = cur.execute(
    "SELECT restaurant_name, SUM(food_cost) "
    "FROM orders "
    "GROUP BY restaurant_name "
    "ORDER BY restaurant_name "
)
res1 = res.fetchall()
fig, ax = plt.subplots(constrained_layout=True)
x = 0.5 + np.arange(len(res1))
restaurant_names, revenue = zip(*res1)
bars = ax.bar(x, revenue, width=1, edgecolor="white", linewidth=0.3)
ax.bar_label(bars)
ax.set(
    xlim=(0, 4),
    xticks=0.5 + np.arange(0, 4),
    xticklabels=restaurant_names,
    ylim=(186000, 190000),
    yticks=np.arange(186000, 190000, 1000),
)
ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")
fig.suptitle("Revenue by restaurant", fontsize=16)
plt.savefig("plots/plot_2.png")
