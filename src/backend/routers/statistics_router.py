from collections import defaultdict
import json
from typing import Annotated
from fastapi import APIRouter, Depends, status
from schemas.user_schema import User, UserSchema
from services.user_service import UserService
from schemas.bill_schema import BillSchema
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger


logger.add("statistic_router.log",  level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss.SSS} - {level: <8} - {message}")


router = APIRouter()
user_service= UserService() 


# Itt lehetne a bills_data például egy adatbázisból vagy más forrásból származó adatok listája
bills_data = user_service.get_all_bills()
df = pd.DataFrame(bills_data)


statistics = {
            "total_spending": 0,
            "total_items": 0,
            "total_bills": len(bills_data),
            "user_spending": defaultdict(float),
            "item_frequency": defaultdict(int),
            "user_most_liked_item": defaultdict(str)
    }

for bill in bills_data:
        statistics["total_spending"] += bill["total"]
        for item in bill["items"]:
            statistics["total_items"] += item["quantity"]
            statistics["user_spending"][bill["user_id"]] += item["total_price"]
            statistics["item_frequency"][item["name"]] += item["quantity"]
            if statistics["user_most_liked_item"][bill["user_id"]] == '' or statistics["item_frequency"][item["name"]] > statistics["item_frequency"][statistics["user_most_liked_item"][bill["user_id"]]]:
                statistics["user_most_liked_item"][bill["user_id"]] = item["name"]

for user_id, spending in statistics["user_spending"].items():
     statistics["user_spending"][user_id] = spending / statistics["total_bills"]

def get_total_spending():
        return round(statistics['total_spending'],2)

def get_total_items_purchased():
        return statistics['total_items']

def get_total_bills( ):
        return statistics['total_bills']
    
      # Returns The List Of User Id's with it's spending
def get_all_users_overall_spending( ):
        user_spending_dict = {}
        for user_id, spending in statistics["user_spending"].items():
            user_spending_dict[user_id] = round(spending, 2)
        return user_spending_dict

        # Returns The Must Buyed Item
def get_item_statistics( ):
        most_frequent_item = max(statistics["item_frequency"], key= statistics["item_frequency"].get)
        return most_frequent_item

        # Returns The User's ID
def get_user_with_the_highest_spending( ):
        user_with_highest_spending = max(statistics["user_spending"], key=statistics["user_spending"].get)
        return user_with_highest_spending

def get_comparison_between_users( ):
        user_with_highest_spending = max(statistics["user_spending"], key=statistics["user_spending"].get)
        comparison = [f"User with the highest spending: User {user_with_highest_spending} (€{statistics['user_spending'][user_with_highest_spending]:.2f} on average)"]
        for user_id, most_liked_item in statistics["user_most_liked_item"].items():
            comparison.append(f"User {user_id}'s most liked item: {most_liked_item}")
        return "\n".join(comparison)

def get_comparison_for_user(user_id_to_compare):
        # Returns a percentage (eg. This user spent more then 80% of the user's)
        user_spending_to_compare = statistics["user_spending"][user_id_to_compare]
        if user_spending_to_compare == 0:
          return 0
        users_spent_less = sum(1 for spending in statistics["user_spending"].values() if spending < user_spending_to_compare)
        total_users = len(statistics["user_spending"])
        percentage_spent_more = abs((users_spent_less / total_users)) * 100
        if percentage_spent_more == 0:
            percentage_spent_more = 100
        return round(percentage_spent_more,2)

def get_user_expenses_by_month(user_id):
        expenses_by_month = defaultdict(float)
        for bill in bills_data:
            if bill['user_id'] == user_id:
                month_number = bill['date'].month
                expenses_by_month[month_number] += bill['total']
        return expenses_by_month


# FastAPI végpontok a statisztikák lekérdezésére
@router.get('/total_spending')
def total_spending():
    return {'total_spending': get_total_spending()}

@router.get('/total_items_purchased')
def total_items_purchased():
    return {'total_items_purchased': get_total_items_purchased()}

@router.get('/total_bills')
def total_bills():
    return {'total_bills': get_total_bills()}

@router.get('/all_users_overall_spending')
def all_users_overall_spending():
    return get_all_users_overall_spending()

@router.get('/item_statistics')
def item_statistics():
    return {'most_frequent_item': get_item_statistics()}

@router.get('/user_with_highest_spending')
def user_with_highest_spending():
    return {'user_with_highest_spending': get_user_with_the_highest_spending()}

@router.get('/comparison_between_users')
def comparison_between_users():
    return {'comparison_between_users': get_comparison_between_users()}

@router.get('/comparison_for_user/{user_id}')
def comparison_for_user(user_id: int):
    return {'comparison_for_user': get_comparison_for_user(user_id)}

@router.get("/user_expenses_by_month/{user_id}")
def get_expenses_by_month(user_id: int):
    expenses_by_month = get_user_expenses_by_month(user_id)
    return expenses_by_month
