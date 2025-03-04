from utils.notifications import notify_user, notify_admin

def check_budget(user_id, category_id, amount):
    budgets = get_budgets(user_id)
    for budget in budgets:
        if budget["category_id"] == category_id and amount > budget["amount"]:
            notify_user(f"You have exceeded your budget for {budget['category_id']}!")