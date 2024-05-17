import matplotlib.pyplot as plt
import numpy as np
import sqlite3


con = sqlite3.connect("food_orders.db")
cur = con.cursor()


# Q5a: Who visited each store the most, and who visited the most stores?
# A5a: Bean Juice Stand, Michael, 855
# Johnny's Cashew Stand, Michael, 843
# The Ice Cream Parlor, Michael, 915
# The Restaurant at the End of the Universe, Michael, 849

# Direct answer
res = cur.execute("""
    SELECT restaurant_name, first_name, visits
    FROM
        (SELECT restaurant_name, first_name, visits, row_number() OVER (PARTITION BY restaurant_name ORDER BY visits DESC) as row_number
        FROM (
            SELECT restaurant_name, first_name, COUNT(*) as visits
            FROM orders
            GROUP BY restaurant_name, first_name))\
    WHERE row_number = 1;
    """)
res1 = res.fetchall()
restaurant_names, _, _ = zip(*res1)
print(res1)

# Plot
fig, ax = plt.subplots(4, 1, constrained_layout=True)
fig.suptitle("Top 5 customers by visits per restaurant", fontsize=16)
for i, restaurant in enumerate(restaurant_names):
    res = cur.execute(
        "SELECT first_name, COUNT(*) "
        "FROM orders "
        "WHERE restaurant_name = :restaurant "
        "GROUP BY first_name "
        "ORDER BY COUNT(*) DESC "
        "LIMIT 5",
        {"restaurant": restaurant},
    )
    res1 = res.fetchall()
    print(res1)
    first_name, revenue = zip(*res1)
    x = 0.5 + np.arange(len(res1))
    bars = ax[i].bar(x, revenue, width=1, edgecolor="white", linewidth=0.3)
    ax[i].bar_label(bars)
    ax[i].set(
        xlim=(0, 5),
        xticks=0.5 + np.arange(0, 5),
        xticklabels=first_name,
        ylim=(500, 1000),
        yticks=np.arange(500, 1000, 100),
    )
    ax[i].set_xlabel(restaurant)
plt.savefig("plots/plot_5a.png")


# Q5b: Who visited the most stores?
# A5b: Michael, 3462

# Direct answer and plot
res = cur.execute("""
    SELECT first_name, COUNT(*) as visits
    FROM orders
    GROUP BY first_name
    ORDER BY visits DESC
    LIMIT 5
    """)
res1 = res.fetchall()
print(res1)
fig, ax = plt.subplots(constrained_layout=True)
x = 0.5 + np.arange(len(res1))
first_names, visits = zip(*res1)
bars = ax.bar(x, visits, width=1, edgecolor="white", linewidth=0.3)
ax.bar_label(bars)
ax.set(
    xlim=(0, 5),
    xticks=0.5 + np.arange(0, 5),
    xticklabels=first_names,
    ylim=(2000, 4000),
    yticks=np.arange(2000, 4000, 1000),
)
fig.suptitle("Most frequent customers", fontsize=16)
plt.savefig("plots/plot_5b.png")
