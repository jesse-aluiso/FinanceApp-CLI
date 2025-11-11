from auth import *
from finance_app import *
from forecast_module import forecast_spending
from datetime import datetime
from datetime import datetime, timedelta

def main():
    while True:
        print("Welcome to FinanceApp CLI")
        username = input("Username: ")
        password = input("Password: ")

        user = authenticate_user(username, password)
        if not user:
            print("Invalid credentials.")
            continue
    
        if user["is_temp_password"]:
            print("You are using a temporary password. Please update it now.")
            new_password = input("Enter new password: ")
            update_password(user["user_id"], new_password)
        

        if user["role"] == "admin":
            signed_out = admin_menu(user["user_id"])
        else:
            signed_out = user_menu(user["user_id"])

        if not signed_out:
            break #Exit the app
#Delted history bank(Log) for admin -> For better tracking of what was deleted/created,etc. by admin from admin_log maybe - this feature is only accessible by admin role ? 
#Give this user a temporary password and then have them create their password in their creation(idk how to do this yet but basically (ex. adding a feature for the user to update password and this is then salted into the database))
def admin_menu(admin_id):
    while True:
        print("\n Admin Menu")
        print("1. Create User")
        print("2. Delete User")
        print("3. View User Logs")
        print("4. View All Users")
        print("5. View a User")
        print("6. View Admin History Log")
        print("7. Update My Password")
        print("8. Edit a User")
        print("9. Sign out")
        print("0. Exit")
        choice = input("Select: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/user): ").lower()
            create_user(name, email, username, password, role, admin_id=admin_id)
            print(f"Successfully created- User:{username} with Role:{role} and temporary password")
        elif choice == "2":
            user_id = input("User ID to delete: ")
            user = get_user_by_id(user_id)
            if user:
                delete_user(user_id, admin_id=admin_id)
                print(f"User ID: {user_id} has been successfully deleted") #I want to display the username of the user_id that is being deleted
            else:
                print("No user found with that ID. Please try again.")
        elif choice == "3":
            user_id = input("Enter User ID to view logs: ")
            view_user_logs(user_id)
        elif choice == "4":
            users = list_all_users()
            for uid, name, email, uname, role in users:
                print(f"User ID: {uid} | Name: {name} | Email: {email} | Username: {uname} | Role: {role}")
        elif choice == "5":
            user_id = input("Enter User ID to view: ")
            user = get_user_by_id(user_id)
            if user:
                print(f"\n User Details:")
                print(f"User ID: {user[0]}")
                print(f"Name: {user[1]}")
                print(f"Email: {user[2]}")
                print(f"Username: {user[3]}")
                print(f"Role: {user[4]}")
            else:    
                print("No user found with that ID. Please try again.")
        elif choice == "6":
            view_admin_log()
        elif choice == "7":
            current_password = input("Enter current password: ")
            cursor.execute("SELECT password FROM users WHERE user_id = %s", (admin_id,))
            stored_hash = cursor.fetchone()

            if stored_hash and bcrypt.checkpw(current_password.encode(), stored_hash[0].encode()):
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm new password: ")
                if new_password == confirm_password:
                    update_password(admin_id, new_password)
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Incorrect current password. Please try again.")

        elif choice == "8":
            user_id = input("Enter User ID to edit: ")
            print("Which field would you like to edit?")
            print("Options: name, email, username, role, password, is_temp_password, password_expiry")
            field = input("Field: ").strip().lower()

            if field == "password_expiry":
                confirm = input("Set password to expire in 90 days? (yes/no): ").lower()
                if confirm == "yes":
                    edit_user(user_id, field, None, admin_id=admin_id)
                else:
                    print("Cancelled.")
            else:
                new_value = input(f"Enter new value for {field}: ")
                edit_user(user_id, field, new_value, admin_id=admin_id)  
        elif choice == "9":
            return True  # Sign out  
        elif choice == "0":
            return False  # Exit app
#also lets add a feature to sign out so that we dont have to run application all the time - for example i can sign out of the admin account and then sign into my user account.
def user_menu(user_id):
    while True:
        print("\n User Menu")
        print("1. Open Account")
        print("2. Deposit Funds") 
        print("3. Withdraw Funds")
        print("4. Close Account")
        print("5. View My Accounts")
        print("6. View My Activity Log")
        print("7. Update My Password")
        print("8. View Account Balance")
        print("9. Forecast Spending")
        print("10. Create Spending Category")
        print("11. Sign Out")
        print("0. Exit")
        choice = input("Select: ")

        if choice == "1":
            account_type = input("Account Type (Checking/Savings/Retirement): ")
            open_account(user_id, account_type)
        elif choice == "2":
            category_name = input("ENTER category for this transaction (e.g., Groceries): ")
            cursor.execute("SELECT category_id FROM categories WHERE user_id = %s AND name = %s", (user_id, category_name))
            result = cursor.fetchone()
            if not result:
                print("Category not found. Please create it first.")
                continue
            category_id = result[0]

            account_type = input("Account Type (Checking/Savings/Retirement): ") # Ask for account_type
            cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
            result = cursor.fetchone()

            if not result:
                print(f"No {account_type} account found.")
                continue
            account_id = result[0]
            try:
                amount = float(input("Amount to deposit: "))
                deposit(account_id, amount)
                

                # For testing only — simulate last month
                direction = input("Simulate transaction in the past or future? (Enter 'past' or 'future'): ").strip().lower()
                days = int(input("How many days from today? (e.g., 30,60, etc.): "))
                if direction == "future":
                    data_override = datetime.now().date() + timedelta(days=days)
                    print(f"Transaction will be logged with date: {data_override}")
                else:
                    data_override = datetime.now().date() - timedelta(days=days)
                           
                #days_offset = int(input("Enter number of days offset from today (negative for future, postive for past) (e.g., 30, 60): "))
                #date_override = datetime.now().date() - timedelta(days=days_offset)
                log_transaction(user_id, account_id, amount, category_id, "deposit", data_override)
                print(f"Deposited ${amount:.2f} into {account_type} account under category '{category_name}'.")
            except ValueError:
                print("Invalid amount. Please enter a number value.")
        elif choice == "3":
            category_name = input("ENTER category for this transaction (e.g., Groceries): ")
            cursor.execute("SELECT category_id FROM categories WHERE user_id = %s AND name = %s", (user_id, category_name))
            result = cursor.fetchone()
            if not result:
                print("Category not found. Please create it first.")
                continue
            category_id = result[0]
             

            account_type = input("Account type (Checking/Savings/Retirement): ")
            cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
            result = cursor.fetchone()

            if not result:
                print(f"No {account_type} account found. Please try again.")
                continue
            account_id = result[0]
            
            try:
                amount = float(input("Amount to withdraw: "))
                direction = input("Simulate withdrawal in the past or future? (Enter 'past' or 'future'): ").strip().lower()
                days = int(input("How many days from today? (e.g., 30, 60, etc.): "))
                if direction == "future":
                    date_override = datetime.now().date() + timedelta(days=days)
                else:
                    date_override = datetime.now().date() - timedelta(days=days)
                print(f"Withdrawal will be logged with date: {date_override}") 
                withdraw(account_id, amount)
                log_transaction(user_id, account_id, amount, category_id, "withdraw", date_override)
                print(f"Withdrew ${amount:.2f} from {account_type} account under category '{category_name}'.")

            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
        elif choice == "4":
            account_type = input("Account Type to close(Checking/Savings/Retirement): ")
            close_account(user_id, account_type)
        elif choice == "5":
            accounts = get_user_accounts(user_id)
            for acc in accounts:
                print(f"ID: {acc[0]}, Type: {acc[1]}, Balance: ${acc[2]:.2f}")
        elif choice == "6":
            view_user_logs(user_id)
        elif choice == "7":
            current_password = input("Enter current password: ")
            cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
            stored_hash = cursor.fetchone()

            if stored_hash and bcrypt.checkpw(current_password.encode(), stored_hash[0].encode()):
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm new password: ")
                if new_password == confirm_password:
                    update_password(user_id, new_password)
                    
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Incorrect current password. Please try again.")
        elif choice == "8":
            account_type = input("Account Type (Checking/Savings/Retirement): ")
            cursor.execute("SELECT balance FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
            result = cursor.fetchone()

            if result:
                balance = result[0]
                print(f"Balance in {account_type}: ${balance:.2f}")
            else: 
                print(f"No {account_type} account found. Please try again.")
        elif choice == "9":
            category = input("Enter category to forecast (e.g., Groceries): ")
            forecast_spending(user_id, category)
        elif choice == "10":
            category_name = input("Enter new category name: ")
            create_category(user_id, category_name)
        elif choice == "11":
            return True  # Sign out
        elif choice == "0":
            return False  # Exit app

if __name__ == "__main__":
    main()
