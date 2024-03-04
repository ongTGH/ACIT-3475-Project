from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user



app = Flask(__name__)


def update_categories_budgets(categories, budgets, expenses):
    for category in categories:
        category['total_budget'] = 0
        category['remaining_budget'] = 0
        for budget in budgets:
            if budget['category'] == category['category']:
                category['total_budget'] += int(budget['amount'])
                category['remaining_budget'] += int(budget['amount'])
        for expense in expenses:
            if expense['category'] == category['category']:
                category['remaining_budget'] -= int(expense['amount'])
    return categories

# Check for errors in user input
def validate_amount(amount, total_expense=None, total_budget=None):
    try:
        int(amount)
    except ValueError:
        return False
    if int(amount) < 0 or amount == "":
        return False
    if total_expense and total_budget:
        if (int(total_expense) + int(amount)) > int(total_budget):
            return False
    return True

def check_for_existing(name_input, existing_list, criteria):
    for listing in existing_list:
        if name_input.lower() == listing[criteria].lower():
            return False
    return True

def reset_expenses(existing_expense, budget, current_date):
    new_expense_list = []
    for expense in existing_expense:
        if expense['budget'] != budget['name']:
            new_expense_list.append(expense)
    return new_expense_list

def recalculate_total_expenses(existing_category, budget, existing_expense):
    new_expense_total = 0
    for category in existing_category:
        if category['category'] == budget['category']:
            for expense in existing_expense:
                if expense['category'] == budget['category'] and expense['budget'] != budget['name']:
                    new_expense_total += int(expense['amount'])
    return new_expense_total

@app.route('/', methods=['GET', 'POST'])
# #@login_required
def index():
    with open("expense.json", "r") as f:
        existing_expense = json.load(f)
    with open("category.json", "r") as f:
        existing_category = json.load(f)    
    with open("budget.json", "r") as f:
        existing_budget = json.load(f)
    with open("history.json", "r") as file:
        history = json.load(file)

    # Initialize the variables with default values
    descr = ''
    amount = 0
    category = ''
    name = ''
    budget = ''
    current_date = datetime.now().strftime("%d %b %Y")

    # Append the new data to the existing data
    if request.method == 'POST':
        if 'descr' in request.form and 'amount' in request.form and 'category' in request.form and 'budget' in request.form:
            descr = request.form['descr']
            amount = request.form['amount']
            category = request.form['category']
            budget = request.form['budget']

            total_expenses = 0
            total_budget = 0
            for expense_item in existing_expense:
                if expense_item["budget"] == budget:
                    total_expenses += int(expense_item["amount"])
            for budget_item in existing_budget:
                if budget_item["name"] == budget:
                    total_budget = int(budget_item["amount"])

            if validate_amount(amount, total_expenses, total_budget) == True:
                budget_exists = any(budget_item['name'] == budget for budget_item in existing_budget)
            
                new_expense = {
                    "descr": descr,
                    "amount": amount,
                    "category": category,
                    "budget": budget,
                    "date": current_date
                }

                existing_expense.append(new_expense)
                for category in existing_category:
                    if category['category'] == new_expense['category']:
                        category['total expenses'] += int(new_expense['amount'])

                new_action = {
                    "action": "Created Expense",
                    "name": new_expense["budget"],
                    "amount": amount,
                    "description": descr,
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)

        elif 'name' in request.form and 'amount' in request.form and 'category' in request.form:
            name = request.form['name']
            amount = request.form['amount']
            category = request.form['category']
            recurring = request.form['recurring budget']

            if validate_amount(amount) == True and name != "" and check_for_existing(name, existing_budget, 'name') == True:
            
                new_budget = {
                    'name': name,
                    'amount': amount,
                    'category': category,
                    'recurring': recurring,
                    'date': current_date
                }
                existing_budget.append(new_budget)

        elif 'category' in request.form:
            category = request.form['category']
            
            if category != "" and check_for_existing(category, existing_category, "category"):
            
                new_category = {
                    'category': category,
                    'total budget': 0,
                    'total expenses': 0,
                    'date': current_date
                }
                existing_category.append(new_category)

        # Write the entire data object back to the file
        with open("expense.json", "w") as f:
            json.dump(existing_expense, f, indent=4)
        with open("category.json", "w") as f:
            json.dump(existing_category, f, indent=4)
        with open("budget.json", "w") as f:
            json.dump(existing_budget, f, indent=4)
        with open("history.json", "w") as file:
            json.dump(history, file, indent=4)
            return redirect(url_for("index"))
        
     # check for recurring budget 
    for budget in existing_budget:
        if budget['recurring'] == "None":
            continue
        elif budget['recurring'] == "Daily":
            if (datetime.strptime(current_date, "%d %b %Y") - datetime.strptime(budget['date'], "%d %b %Y")).days == 1:
                new_expense_list = []
                for expense in existing_expense:
                    if expense['budget'] != budget['name']:
                        new_expense_list.append(expense)
                existing_expense = new_expense_list
                budget['date'] = current_date

                budget_expense_total = 0
                for expense in existing_expense:
                    if expense['budget'] == budget['name']:
                        budget_expense_total += expense['amount']

                for category in existing_category:
                    if category['category'] == budget['category']:
                        category['total expenses'] = recalculate_total_expenses(existing_category, budget, existing_expense)

                new_action = {
                    "action": "Reset Recurring Budget",
                    "name": budget['name'],
                    "amount": budget_expense_total,
                    "description": budget['recurring'] + " budget",
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)


        elif budget['recurring'] == "Weekly":
             if (datetime.strptime(current_date, "%d %b %Y") - datetime.strptime(budget['date'], "%d %b %Y")).days == 7:
                new_expense_list = []
                for expense in existing_expense:
                    if expense['budget'] != budget['name']:
                        new_expense_list.append(expense)
                existing_expense = new_expense_list
                budget['date'] = current_date

                budget_expense_total = 0
                for expense in existing_expense:
                    if expense['budget'] == budget['name']:
                        budget_expense_total += expense['amount']

                new_action = {
                    "action": "Reset Recurring Budget",
                    "name": budget['name'],
                    "amount": budget_expense_total,
                    "description": budget['recurring'] + " budget",
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)

        elif budget['recurring'] == "Bi-Weekly":
             if (datetime.strptime(current_date, "%d %b %Y") - datetime.strptime(budget['date'], "%d %b %Y")).days == 14:
                new_expense_list = []
                for expense in existing_expense:
                    if expense['budget'] != budget['name']:
                        new_expense_list.append(expense)
                existing_expense = new_expense_list
                budget['date'] = current_date

                budget_expense_total = 0
                for expense in existing_expense:
                    if expense['budget'] == budget['name']:
                        budget_expense_total += expense['amount']

                new_action = {
                    "action": "Reset Recurring Budget",
                    "name": budget['name'],
                    "amount": budget_expense_total,
                    "description": budget['recurring'] + " budget",
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)

        elif budget['recurring'] == "Monthly":
            if (datetime.strptime(current_date, "%d %b %Y") - datetime.strptime(budget['date'], "%d %b %Y")).days == 31:
                new_expense_list = []
                for expense in existing_expense:
                    if expense['budget'] != budget['name']:
                        new_expense_list.append(expense)
                existing_expense = new_expense_list
                budget['date'] = current_date

                budget_expense_total = 0
                for expense in existing_expense:
                    if expense['budget'] == budget['name']:
                        budget_expense_total += expense['amount']

                new_action = {
                    "action": "Reset Recurring Budget",
                    "name": budget['name'],
                    "amount": budget_expense_total,
                    "description": budget['recurring'] + " budget",
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)


        elif budget['recurring'] == "Yearly":
             if (datetime.strptime(current_date, "%d %b %Y") - datetime.strptime(budget['date'], "%d %b %Y")).days == 365:
                new_expense_list = []
                for expense in existing_expense:
                    if expense['budget'] != budget['name']:
                        new_expense_list.append(expense)
                existing_expense = new_expense_list
                budget['date'] = current_date

                budget_expense_total = 0
                for expense in existing_expense:
                    if expense['budget'] == budget['name']:
                        budget_expense_total += expense['amount']

                new_action = {
                    "action": "Reset Recurring Budget",
                    "name": budget['name'],
                    "amount": budget_expense_total,
                    "description": budget['recurring'] + " budget",
                    "date": current_date
                }

                history.insert(0, new_action)
                if len(history) > 10:
                    history.pop(10)

        with open("expense.json", "w") as f:
            json.dump(existing_expense, f, indent=4)
        with open("budget.json", "w") as f:
            json.dump(existing_budget, f, indent=4)
        with open("category.json", "w") as f:
            json.dump(existing_category, f, indent=4)
        with open("history.json", "w") as f:
            json.dump(history, f, indent=4)
        # with open("history.json", "w") as file:
        #     json.dump(history, file, indent=4)

    expenses = existing_expense
    categories = existing_category
    budgets = existing_budget

    # get total budget 
    total_budget = 0
    with open("category.json", "r") as file:
        categories = json.load(file)
    
    for category in categories:
        total_budget += category['total budget']

    # get total expenses
    total_expenses = 0

    for category in categories:
        total_expenses += category['total expenses']

    categories = update_categories_budgets(categories, budgets, expenses)
    return render_template('index.html', 
        expenses=expenses, 
        categories=categories, 
        budgets=budgets, 
        total_budget=total_budget, 
        total_expenses=total_expenses,
        history=history
        )


@app.route('/categories', methods=['GET', 'POST'])
#@login_required
def categories():

    # Get information from category and budget json files
    with open("category.json", "r") as file:
        category_list = json.load(file)
    categories = category_list

    with open("budget.json", "r") as file:
        budget_list = json.load(file)

    with open("expense.json", "r") as file:
        expenses = json.load(file)

    # delete category

    category_to_delete = ""
    if request.method == "POST":
        if "rename category" in list(request.form)[0]:
            category_name = list(request.form)[0][16:]
            new_category_name = request.form[list(request.form)[0]]

            for category in categories:
                if category_name == category['category']:
                    category['category'] = new_category_name
            
            for budget in budget_list:
                if category_name == budget['category']:
                    budget['category'] = new_category_name
            
            for expense in expenses:
                if category_name == expense['category']:
                    expense['category'] = new_category_name
            with open("category.json", "w") as file:
                json.dump(categories, file, indent=4)
            with open("budget.json", "w") as file:
                json.dump(budget_list, file, indent=4)
            with open("expense.json", "w") as file:
                json.dump(expenses, file, indent=4)

        elif "rename budget" in list(request.form)[0]:
            budget_name = list(request.form)[0][14:]
            new_budget_name = request.form[list(request.form)[0]]
            for budget in budget_list:
                if budget_name == budget['name']:
                    budget['name'] = new_budget_name
            with open("budget.json", "w") as file:
                json.dump(budget_list, file, indent=4)

        elif "edit budget" in list(request.form)[0]:
            budget_name = list(request.form)[0][12:]
            new_budget_amount = int(request.form[list(request.form)[0]])
            for budget in budget_list:
                if budget_name == budget['name']:
                    total_expense = 0
                    for expense in expenses:
                        if expense["budget"] == budget["name"]:
                            total_expense += int(expense["amount"])
                    if total_expense <= new_budget_amount:
                        budget['amount'] = new_budget_amount
            with open("budget.json", "w") as file:
                json.dump(budget_list, file, indent=4)

        elif "delete budget" in list(request.form)[0]:
            budget_to_delete = list(request.form)[0][14:]
            new_budget_list = []
            new_expense_list = []
            for budget in budget_list:
                if budget_to_delete != budget["name"]:
                    new_budget_list.append(budget)
                elif budget_to_delete == budget["name"]:
                    for category in categories:
                        if category["category"] == budget["category"]:
                            category["total budget"] -= int(budget["amount"])
                            for expense in expenses:
                                if expense["budget"] == budget["name"]:
                                    category["total expenses"] -= int(expense["amount"])
                                else:
                                    new_expense_list.append(expense)

            with open("budget.json", "w") as file:
                json.dump(new_budget_list, file, indent=4)
            budget_list = new_budget_list
            with open("category.json", "w") as file:
                json.dump(categories, file, indent=4)
            with open("expense.json", "w") as file:
                json.dump(new_expense_list, file, indent=4)

        elif "delete category" in list(request.form)[0]:
            category_list = categories
            for category in category_list:
                if category['category'] == list(request.form)[0][16:]:
                    new_budget_list = []
                    for budget in budget_list:
                        if budget["category"] != category["category"]:
                            new_budget_list.append(budget)
                    budget_list = new_budget_list
                    category_to_delete = category
                    categories.remove(category_to_delete)
                    with open("category.json", "w") as file:
                        json.dump(categories, file, indent=4)
                    with open("budget.json", "w") as file:
                        json.dump(new_budget_list, file, indent=4)
                    break

    total_budget_list = categories
    # add budgets to category files
    for category in total_budget_list:
        category["total budget"] = 0
        for budget in budget_list:
            if budget["category"] == category["category"]:
                category["total budget"] += int(budget["amount"])
    
    with open("category.json", "w") as file:
        json.dump(total_budget_list, file, indent=4)

    with open("budget.json", "r") as file:
        budgets = json.load(file)

    return render_template("categories.html", categories=categories, total_budgets=total_budget_list, budgets=budgets)

# Expense Page
@app.route('/categories/<budget_name>', methods=['GET', 'POST'])
#@login_required
def budget_detail(budget_name):
    with open('expense.json') as f:
        expenses = json.load(f)
    with open('budget.json') as f:
        budgets = json.load(f)
    
    budget = next((budget for budget in budgets if budget['name'] == budget_name), None)
    if budget is None:
        abort(404)
    
    budget_expenses = [expense for expense in expenses if expense['budget'] == budget['name']]

    total_expense = sum([int(expense['amount']) for expense in budget_expenses])
    remaining = int(budget['amount']) - total_expense

    return render_template('expenses.html', budget=budget, budget_expenses=budget_expenses, total_expense=total_expense, remaining=remaining)

@app.route('/clear_expenses/<budget_name>', methods=['DELETE'])
#@login_required
def clear_expenses(budget_name):
    with open('expense.json', 'r') as f:
        expenses = json.load(f)
        
    filtered_expenses = [expense for expense in expenses if expense['budget'] != budget_name]
    
    with open('expense.json', 'w') as f:
        json.dump(filtered_expenses, f, indent=4)
    
    return jsonify({'status': 'success'}), 200


## Transfer Page
@app.route('/transfer', methods=['GET', 'POST'])
#@login_required
def transfer():
    with open("expense.json", "r") as f:
        existing_expense = json.load(f)
    with open("category.json", "r") as f:
        existing_category = json.load(f)    

    with open("budget.json", "r") as f:
        existing_budget = json.load(f)
    expenses = existing_expense
    categories = existing_category
    budgets = existing_budget

    current_date = datetime.now().strftime("%d %b %Y")

    if request.method == 'POST':

        # Get user input
        budget_from_str = request.form["budget-from"]
        budget_to_str = request.form["budget-to"]
        transfer_amount = request.form['transfer-amount']

        # Fix syntax issue replacing single to double quote
        budget_from_str_fixed = budget_from_str.replace("'", "\"")
        budget_to_str_fixed = budget_to_str.replace("'", "\"")

        # Convert string to dictionary
        budget_from_dict = json.loads(budget_from_str_fixed)
        budget_to_dict = json.loads(budget_to_str_fixed)

        if int(budget_from_dict["amount"]) - int(transfer_amount) >= 0:

            # Change budget
            budget_from_dict["amount"] = int(budget_from_dict["amount"]) - int(transfer_amount)
            budget_to_dict["amount"] = int(budget_to_dict["amount"]) + int(transfer_amount)

            # Update budgets
            for budget in budgets:
                if budget["name"] == budget_from_dict["name"] and budget["category"] == budget_from_dict["category"]:
                    budget["amount"] = budget_from_dict["amount"]
                if budget["name"] == budget_to_dict["name"] and budget["category"] == budget_to_dict["category"]:
                    budget["amount"] = budget_to_dict["amount"]
            
        # Write to history.json
        with open("history.json", "r") as file:
            latest_transaction = json.load(file)
        
        new_transaction = {
            "action": "Transfer",
            "name": budget_from_dict["name"] + " to " + budget_to_dict["name"],
            "amount": int(transfer_amount),
            "description": "",
            "date": current_date
        }

        latest_transaction.insert(0, new_transaction)
        if len(latest_transaction) > 10:
            latest_transaction.pop(10)

        with open("history.json", "w") as file:
            json.dump(latest_transaction, file, indent=4)
    
        # Update budgets.json
        with open("budget.json", "w") as f:
            json.dump(budgets, f, indent=4)
    return render_template('transfer.html', expenses=expenses, categories=categories, budgets=budgets)
## End of Transfer


## LOGIN & REGISTER CODE
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_email):
    return User.get(user_email)

class User:
    def __init__(self, email):
        self.email = email

    @staticmethod
    def get(user_email):
        with open('login.json', 'r') as file:
            users = json.load(file)
            for user in users:
                if user['email'] == user_email:
                    return User(user['email'])
        return None
    
    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        loginEmail = request.form.get("login-email")
        passwordInput = request.form.get("login-pwd")
        with open("login.json", "r") as f:
            users = json.load(f)
        for user in users:
            if user["email"] == loginEmail and check_password_hash(user["password"], passwordInput):
                return True
        return False
    
    def get_id(self):
        return self.email

@app.route('/login', methods=['GET', 'POST'])
def login():
    with open("login.json", "r") as f:
        existing_user = json.load(f)

    users = existing_user
    newUser = {}
        
    if request.method == 'POST':
        loginEmail = request.form.get("login-email")
        loginPwd = request.form.get("login-pwd")
        regName = request.form.get("reg-name")
        regEmail = request.form.get("reg-email")
        regPwd1 = request.form.get("reg-pwd1")
        regSecurityQ = request.form.get("reg-security-q")
        regSecurityA = request.form.get("reg-security-a")
        fgtEmail = request.form.get("fgt-email")
        fgtPwd1 = request.form.get("fgt-pwd1")           
        
        if loginEmail:
            userEmail = User.get(loginEmail)
            for user in users:
                if userEmail:
                    if check_password_hash(user["password"], loginPwd):
                        login_user(userEmail)
                        return redirect(url_for("index"))
            flash('Incorrect email or password')
            return redirect(url_for('login'))
        elif fgtEmail:
            for user in users:
                print(user)
                if user['email'] == fgtEmail:
                    user['password'] = generate_password_hash(fgtPwd1, method="sha256")
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
            return redirect(url_for('login'))
        elif regEmail:
            hashPwd = generate_password_hash(regPwd1, method="sha256")
            newUser['name'] = regName
            newUser['password'] = hashPwd
            newUser['email'] = regEmail
            newUser['question'] = regSecurityQ
            newUser['answer'] = regSecurityA
            users.append(newUser)
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
            userEmail = User.get(regEmail)
            login_user(userEmail)
            return redirect(url_for('index'))
        

    return render_template("login.html")
## End of Login & Register Code

@app.route('/cost')
def cost():
    return render_template('cost.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/statistic')
def statistic():
    return render_template('statistic.html')

@app.route('/login.json')
def get_json():
    with open("login.json", "r") as f:
        existing_user = json.load(f)

    # Return the JSON data as a response
    return jsonify(existing_user)

@app.route('/account-page')
#@login_required
def account():
    return render_template('account-page.html')

@app.route('/logout', methods=['GET'])
#@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)