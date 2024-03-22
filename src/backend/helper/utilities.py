import os
import random
import re
from typing import List
import requests
import sys
import dotenv
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
    for _ in range(nr):
        quantity=random.randint(1, 10),
        unique_price = random.uniform(1.0, 100.0),
        total_price = quantity[0] * unique_price[0] 
        print(quantity[0])
        print(unique_price[0])

        item = ItemSchema(
            name=f"Item {_ + 1}",
            quantity=quantity[0],
            unique_price=unique_price[0],
            total_price = total_price
        )

        items.append(item.model_dump())
        
    return items