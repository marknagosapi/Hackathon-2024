import datetime
import os
import random
from typing import List
import requests
from schemas.bill_schema import BillSchema
from schemas.item_schema import ItemSchema


BE_SERVICE_URL=os.getenv("BE_SERVICE_URL")


def send_post_request(bill:BillSchema) -> bool:
    url = BE_SERVICE_URL+"/user/add_bill/"
    data = bill.model_dump()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("POST request was successful")
        return True
    else:
        print("POST request failed")
        return False
    
def generate_random_items(nr)->List[ItemSchema]:
    items = []
    item_names = ['Cheeseburger', 'Pizza', 'Salad', 'Sandwich', 'Pasta', 'Sushi', 'Steak', 'Soup Potato','Bread With Ketchup', 'Soup', 'Taco', 'Burger','Samsung Galaxy 10','iPhone','Water','Jump Rope','Nike Air Jordan','Running Shoe']

    for _ in range(nr):
        quantity=random.randint(1, 10),
        unique_price = random.uniform(1.0, 10.0),
        total_price = quantity[0] * unique_price[0] 

        item_name = random.choice(item_names)
        item = ItemSchema(
            name=item_name,
            quantity=quantity[0],
            unique_price=round(unique_price[0], 2),
            total_price =round( total_price, 2 )
        )
        items.append(item.model_dump())

    return items

# Function to generate random bills data
def generate_bills_data(num_bills):
    bills = []
    bill_ids = set()  # To ensure unique bill IDs
    item_ids = set()  # To ensure unique item IDs
    current_date = datetime.now().date()

    for _ in range(num_bills):
        bill_id = random.randint(1, 1000)
        while bill_id in bill_ids:
            bill_id = random.randint(1, 1000)
        bill_ids.add(bill_id)

        user_id = random.randint(1, 5)
        admin_id = random.randint(1, 10)
        date = current_date - datetime.timedelta(days=random.randint(1, 30))
        item_number = random.randint(1, 5)
        total = 0
        items = []

        for i in range(item_number):
            item_id = random.randint(1, 1000)
            while item_id in item_ids:
                item_id = random.randint(1, 1000)
            item_ids.add(item_id)

            # Random item name
            item_names = ['Cheeseburger', 'Pizza', 'Salad', 'Sandwich', 'Pasta', 'Sushi', 'Steak', 'Soup Potato','Bread With Ketchup', 'Soup', 'Taco', 'Burger','Samsung Galaxy 10','iPhone','Water','Jump Rope','Nike Air Jordan','Running Shoe']
            item_name = random.choice(item_names)

            # Random item price
            item_price = round(random.uniform(10, 50), 2)

            # Random item quantity
            item_quantity = random.randint(1, 5)

            # Calculate total price for the item
            item_total_price = item_price * item_quantity
            total += item_total_price

            item = ItemSchema(
            name=f"Item {_ + 1}",
            quantity=item_quantity[0],
            unique_price=item_price,
            total_price = item_total_price
            )

        items.append(item.model_dump())


        
        # Create bill dictionary
        bill = {
            "id": bill_id,
            "user_id": user_id,
            "admin_id": admin_id,
            "date": date.strftime("%Y-%m-%d"),
            "item_number": len(items),
            "items": items,
            "total": total
        }
        bills.append(bill)

    return bills
