import bcrypt  # For password hashing and verification
from db import cursor, conn  # DB connection and cursor
from finance_app import (log_user_action)

# Hashes a plaintext password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verifies a password against a stored hash
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash.encode())

# Authenticates a user by username and password
def authenticate_user(username, password):
    cursor.execute("SELECT user_id, username, password, role, is_temp_password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode(), result[2].encode()):
        return {
            "user_id": result[0],
            "username": result[1],
            "role": result[3],
            "is_temp_password": result[4]
        }
    return None

# Logs an admin action to the audit_log table
def log_admin_action(admin_id, action):
    cursor.execute("INSERT INTO audit_log (admin_id, action) VALUES (%s, %s)", (admin_id, action))
    conn.commit()

# Creates a new user (admin or regular) and logs the action
def create_user(name, email, username, temp_password, role='user', admin_id=None):
    hashed = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "INSERT INTO users (name, email, username, password, role, is_temp_password) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, username, hashed, role, True)
    )
    conn.commit()

    if admin_id:
        log_admin_action(admin_id, f"Created user '{username}' with role '{role}' and temporary password")

# Deletes a user by user_id and logs the action
def delete_user(user_id, admin_id=None):
    # Fetch username for logging before deletion
    cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()

    if admin_id and user:
        log_admin_action(admin_id, f"Deleted user '{user[0]}' (ID: {user_id})")

def update_password(user_id, new_password):
    cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
    current_hash = cursor.fetchone()

    cursor.execute("SELECT password_hash FROM password_history WHERE user_id = %s ORDER BY changed_at DESC LIMIT 3", (user_id,))
    recent_hashes = cursor.fetchall()

    for old in [current_hash[0]] +[r[0] for r in recent_hashes]:
        if bcrypt.checkpw(new_password.encode(), old.encode()):
            print("New password cannot match any of your last 3 password.")
            return

    if current_hash and bcrypt.checkpw(new_password.encode(), current_hash[0].encode()):
        print("New password cannot be the same as the current password. Please try again.")
        return
    
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("UPDATE users SET password = %s, is_temp_password = FALSE WHERE user_id = %s", (hashed, user_id))
    conn.commit()

    cursor.execute("INSERT INTO password_history (user_id, password_hash) VALUES (%s, %s)", (user_id, hashed))
    conn.commit()

    cursor.execute("DELETE FROM password_history WHERE user_id = %s AND history_id NOT IN (SELECT history_id FROM(SELECT history_id FROM password_history WHERE user_id = %s ORDER BY changed_at DESC LIMIT 3) AS recent)", (user_id, user_id))
    conn.commit()

    log_user_action(user_id, "Updated password")
    print("Password updated successfully.")
    