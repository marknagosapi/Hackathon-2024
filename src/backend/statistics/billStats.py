# Make Statistics 
from collections import defaultdict

class BillStatistics:
    def __init__(self, bills_data):
        self.statistics = {
            "total_spending": 0,
            "total_items": 0,
            "total_bills": len(bills_data),
            "user_spending": defaultdict(float),
            "item_frequency": defaultdict(int),
            "user_most_liked_item": defaultdict(str)
        }

    def calculateStatistics(self):
        for bill in bills_data:
            self.statistics["total_spending"] += bill["total"]
            for item in bill["items"]:
                self.statistics["total_items"] += item["quantity"]
                self.statistics["user_spending"][bill["user_id"]] += item["total_price"]
                self.statistics["item_frequency"][item["name"]] += item["quantity"]
                if self.statistics["user_most_liked_item"][bill["user_id"]] == '' or self.statistics["item_frequency"][item["name"]] > self.statistics["item_frequency"][self.statistics["user_most_liked_item"][bill["user_id"]]]:
                    self.statistics["user_most_liked_item"][bill["user_id"]] = item["name"]

        # Calculate average spending per user
        for user_id, spending in self.statistics["user_spending"].items():
            self.statistics["user_spending"][user_id] = spending / self.statistics["total_bills"]

    def get_total_spending(self):
        return self.statistics['total_spending']

    def get_total_items_purchased(self):
        return self.statistics['total_items']

    def get_total_bills(self):
        return self.statistics['total_bills']
    

    def get_user_statistics(self):
        user_stats = []
        for user_id, spending in self.statistics["user_spending"].items():
            user_stats.append(f"Average spending for User {user_id}: €{spending:.2f}")
        return "\n".join(user_stats)

    def get_item_statistics(self):
        most_frequent_item = max(self.statistics["item_frequency"], key=self.statistics["item_frequency"].get)
        return f"Most frequently purchased item: {most_frequent_item} ({self.statistics['item_frequency'][most_frequent_item]} times)"

    def get_comparison_between_users(self):
        user_with_highest_spending = max(self.statistics["user_spending"], key=self.statistics["user_spending"].get)
        comparison = [f"User with the highest spending: User {user_with_highest_spending} (€{self.statistics['user_spending'][user_with_highest_spending]:.2f} on average)"]
        for user_id, most_liked_item in self.statistics["user_most_liked_item"].items():
            comparison.append(f"User {user_id}'s most liked item: {most_liked_item}")
        return "\n".join(comparison)

    def get_comparison_for_user(self, user_id_to_compare):
        user_spending_to_compare = self.statistics["user_spending"][user_id_to_compare]
        users_spent_less = sum(1 for spending in self.statistics["user_spending"].values() if spending < user_spending_to_compare)
        total_users = len(self.statistics["user_spending"])
        percentage_spent_more = abs((users_spent_less / total_users)) * 100
        if percentage_spent_more == 0:
            percentage_spent_more = 100
        return f"Comparison for User {user_id_to_compare}:\nSpending: €{user_spending_to_compare:.2f}\nPercentage of people spent more than user {user_id_to_compare}: {percentage_spent_more:.2f}%"

# Example usage:
bills_data = [...]  # Your bills data here
billStatManager = BillStatistics(bills_data)
billStatManager.calculateStatistics()
billStatManager.get_basic_statistics()