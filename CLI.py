from auth import authenticate_user, create_user, delete_user
from finance_app import (
    open_account, deposit, withdraw, close_account,
    get_user_accounts, view_user_logs, list_all_users, get_user_by_id
)

def main():
    print("Welcome to FinanceApp CLI")
    username = input("Username: ")
    password = input("Password: ")

    user = authenticate_user(username, password)
    if not user:
        print("Invalid credentials.")
        return

    if user["role"] == "admin":
        admin_menu(user["user_id"])
    else:
        user_menu(user["user_id"])

def admin_menu(admin_id):
    while True:
        print("\n Admin Menu")
        print("1. Create User")
        print("2. Delete User")
        print("3. View User Logs")
        print("4. View All Users")
        print("5. View a User")
        print("0. Exit")
        choice = input("Select: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/user): ").lower()
            create_user(name, email, username, password, role, admin_id=admin_id)
            print(f"Successfully created: User:{username} with Role:{role}")
        elif choice == "2":
            user_id = input("User ID to delete: ")
            username = input("Username to delte: ")
            delete_user(user_id, username, admin_id=admin_id)
            print(f"User ID: {user_id} has been successfully deleted") #I want to display the username of the user_id that is being delted
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
                print(f"Email:  {user[2]}")
                print(f"Username: {user[3]}")
                print(f"Role: {user[4]}")
            else:    
                print("No user found with that ID. Please try again.")
        elif choice == "0":
            break

def user_menu(user_id):
    while True:
        print("\n User Menu")
        print("1. Open Account")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Close Account")
        print("5. View My Accounts")
        print("6. View My Activity Log")
        print("0. Exit")
        choice = input("Select: ")

        if choice == "1":
            account_type = input("Account Type (Checking/Savings/Retirement): ")
            open_account(user_id, account_type)
        elif choice == "2":
            account_id = input("Account ID: ")
            amount = float(input("Amount to deposit: "))
            deposit(account_id, amount)
        elif choice == "3":
            account_id = input("Account ID: ")
            amount = float(input("Amount to withdraw: "))
            withdraw(account_id, amount)
        elif choice == "4":
            account_type = input("Account Type to close: ")
            close_account(user_id, account_type)
        elif choice == "5":
            accounts = get_user_accounts(user_id)
            for acc in accounts:
                print(f"ID: {acc[0]}, Type: {acc[1]}, Balance: ${acc[2]:.2f}")
        elif choice == "6":
            view_user_logs(user_id)
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
