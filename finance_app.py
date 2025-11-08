from db import cursor, conn # Import the database cursor and connection from db.py

def open_account(user_id, account_type):
    # Check if the user already has this account type
    cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
    existing = cursor.fetchone()

    if existing:
        print(f"{account_type} account already exists for this user.")
        log_user_action(user_id, f"Attempted to open duplicate {account_type} account")
        return

    # Insert new account if not already present
    cursor.execute("INSERT INTO accounts (user_id, account_type) VALUES (%s, %s)", (user_id, account_type))
    conn.commit()
    print(f"{account_type} account opened.")
    log_user_action(user_id, f"Opened {account_type} account")

def deposit(account_id, amount):
    # Add deposit to account balance
    cursor.execute("SELECT account_type FROM accounts WHERE account_id = %s", (account_id, ))
    result = cursor.fetchone()
    account_type = result[0] if result else "unknown"
    
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
    conn.commit()
    print(f"Deposited: ${amount:.2f} to account type: {account_type}") #Change so it shows the "to account "Account_Type" (for example Deposited amount to account Checking)
    log_user_action(account_id_to_user(account_id), f"Deposited: ${amount:.2f} to account type: {account_type}")


def withdraw(account_id, amount):
    # Check current balance
    cursor.execute("SELECT balance, user_id FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()

    if not result:
        print("Account not found.")
        return

    balance, user_id = result

    cursor.execute("SELECT account_type FROM accounts WHERE account_id = %s", (account_id,))
    type_result = cursor.fetchone()
    account_type = type_result[0] if type_result else "Unknown"

    if amount > balance:
        print("Withdrawal failed: Insufficient funds.")
        log_user_action(user_id, f"Attempted to withdraw ${amount:.2f} from {account_type} — insufficient funds")
        return

    # Proceed with withdrawal
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
    conn.commit()
    print(f"Withdrew: ${amount:.2f} from {account_type} account")
    log_user_action(user_id, f"Withdrew: ${amount:.2f} from account {account_type} account")


def get_user_accounts(user_id):
    cursor.execute("SELECT account_id, account_type, balance FROM accounts WHERE user_id = %s", (user_id,))
    accounts = cursor.fetchall()
    log_user_action(user_id, "Viewed account summary")
    return accounts

def close_account(user_id, account_type):
    # Check if the account exists - Ensures the log only fires after a successful deletion. Keeps your audit trail clean and accurate. Makes it easy to trace user-driven actions separately from admin actions
    cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
    account = cursor.fetchone()

    if account:
        # Delete the account
        cursor.execute("DELETE FROM accounts WHERE user_id = %s AND account_type = %s", (user_id, account_type))
        conn.commit()
        print(f"{account_type} account closed.")
        # Log the user action here
        log_user_action(user_id, f"Closed {account_type} account")
    else:
        print(f"No {account_type} account found for this user.")
        log_user_action(user_id, f"Attempted to close non-existent {account_type} account")

def log_user_action(user_id, action):
    cursor.execute("INSERT INTO user_activity_log (user_id, action) VALUES (%s, %s)", (user_id, action))
    conn.commit()

def account_id_to_user(account_id):
    cursor.execute("SELECT user_id FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def view_user_logs(user_id):
    # Fetch all user actions from the log
    cursor.execute("SELECT action, timestamp FROM user_activity_log WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
    logs = cursor.fetchall()

    if logs:
        print("\nUser Activity Log:")
        for action, timestamp in logs:
            print(f"[{timestamp}] {action}")
    else:
        print("No activity found for this user.")

def list_all_users():
    cursor.execute("SELECT user_id, name, email, username, role FROM users ORDER BY user_id")
    return cursor.fetchall()

def get_user_by_id(user_id):
    cursor.execute("SELECT user_id, name, email, username, role FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

def view_admin_log():
    cursor.execute("SELECT log_id, admin_id, action, timestamp FROM audit_log ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    print("\nAdmin History Log:")
    for log in logs:
        print(f"[{log[3]}] Admin ID: {log[1]} | Action: {log[2]}")


