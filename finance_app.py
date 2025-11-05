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
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
    conn.commit()
    print(f"Deposited ${amount:.2f} to account {account_id}")
    log_user_action(account_id_to_user(account_id), f"Deposited ${amount:.2f} to account {account_id}")


def withdraw(account_id, amount):
    # Check current balance
    cursor.execute("SELECT balance, user_id FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()

    if not result:
        print("Account not found.")
        return

    balance, user_id = result

    if amount > balance:
        print("Withdrawal failed: Insufficient funds.")
        log_user_action(user_id, f"Attempted to withdraw ${amount:.2f} from account {account_id} — insufficient funds")
        return

    # Proceed with withdrawal
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
    conn.commit()
    print(f"Withdrawn ${amount:.2f} from account {account_id}")
    log_user_action(user_id, f"Withdrew ${amount:.2f} from account {account_id}")


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

