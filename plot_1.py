import matplotlib.pyplot as plt
import numpy as np
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()

# Q1a: How many customers visited the "Restaurant at the end of the universe"?
# A1a: 37230 visits

# Direct answer
res = cur.execute(
    "SELECT COUNT(*) FROM orders WHERE restaurant_name = 'the-restaurant-at-the-end-of-the-universe'"
)
print(res.fetchone())

# Plot
res = cur.execute(
    "SELECT restaurant_name, COUNT(*) "
    "FROM orders "
    "GROUP BY restaurant_name "
    "ORDER BY restaurant_name "
)
res1 = res.fetchall()
fig, ax = plt.subplots(constrained_layout=True)
x = 0.5 + np.arange(len(res1))
restaurant_names, num_visitors = zip(*res1)
bars = ax.bar(x, num_visitors, width=1, edgecolor="white", linewidth=0.3)
ax.bar_label(bars)
ax.set(
    xlim=(0, 4),
    xticks=0.5 + np.arange(0, 4),
    xticklabels=restaurant_names,
    ylim=(37000, 38000),
    yticks=np.arange(37000, 38000, 200),
)
ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")
# plt.tight_layout()
fig.suptitle("Visits per restaurant", fontsize=16)
plt.savefig("plots/plot_1a.png")


# Q1b: How many DISTINCT customers visited the "Restaurant at the end of the universe"?
# A1b: 689 distinct visitors

# Direct answer
res = cur.execute(
    "SELECT COUNT(DISTINCT first_name) FROM orders WHERE restaurant_name = 'the-restaurant-at-the-end-of-the-universe'"
)
print(res.fetchone())

# Plot
res = cur.execute(
    "SELECT restaurant_name, COUNT(DISTINCT first_name) "
    "FROM orders "
    "GROUP BY restaurant_name "
    "ORDER BY restaurant_name "
)
res2 = res.fetchall()
fig, ax = plt.subplots(constrained_layout=True)
x = 0.5 + np.arange(len(res2))
restaurant_names, num_visitors = zip(*res2)
bars = ax.bar(x, num_visitors, width=1, edgecolor="white", linewidth=0.3)
ax.bar_label(bars)
ax.set(
    xlim=(0, 4),
    xticks=0.5 + np.arange(0, 4),
    xticklabels=restaurant_names,
    ylim=(680, 700),
    yticks=np.arange(680, 700, 10),
)
ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha="right")
fig.suptitle("Unique visitors per restaurant", fontsize=16)
plt.savefig("plots/plot_1b.png")
