from faker import Faker
from faker.providers import DynamicProvider
from faker.providers import person
import csv

fake = Faker()

restaurant_names_provider = DynamicProvider(
    provider_name="restaurant_names",
    elements=["the-restaurant-at-the-end-of-the-universe", "johnnys-cashew-stand", "bean-juice-stand",
              "the-ice-cream-parlor"],
)

food_names_provider = DynamicProvider(
    provider_name="food_names",
    elements=["beans", "cashews", "chips", "chocolate", "coffee", "cookies", "corn", "candy", "cereal", "chicken",
              "cheese", "eggs", "fish", "fruit", "grains", "honey", "ice cream", "juice", "milk", "meat", "nuts", "oil",
              "pasta", "rice", "salad", "sandwiches", "soup", "spices", "sugar", "tea", "vegetables", "water", "wine",
              "yogurt"],
)

food_cost_provider = DynamicProvider(
    provider_name="food_cost",
    elements=[1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.00, 8.50, 9.00],
)

fake.add_provider(restaurant_names_provider)
fake.add_provider(food_names_provider)
fake.add_provider(person)
fake.add_provider(food_cost_provider)

print(fake.restaurant_names())
print(fake.food_names())
print(fake.first_name_nonbinary())
print(fake.food_cost())

with open('data.csv', 'w', newline='') as csvfile:
    field_names = ['restaurant_names', 'food_names', 'first_name', 'food_cost']
    restaurant_data = csv.DictWriter(
        csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL,
        fieldnames=field_names
    )
    restaurant_data.writeheader()
    for _ in range(150000):
        restaurant_data.writerow({
            'restaurant_names': fake.restaurant_names(),
            'food_names': fake.food_names(),
            'first_name': fake.first_name_nonbinary(),
            'food_cost': fake.food_cost()
        })
