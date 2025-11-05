import bcrypt  # For password hashing and verification
from db import cursor, conn  # DB connection and cursor

# Hashes a plaintext password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Verifies a password against a stored hash
def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash.encode())

# Authenticates a user by username and password
def authenticate_user(username, password):
    cursor.execute("SELECT user_id, password, role FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and verify_password(password, result[1]):
        return {"user_id": result[0], "role": result[2]}
    return None

# Logs an admin action to the audit_log table
def log_admin_action(admin_id, action):
    cursor.execute("INSERT INTO audit_log (admin_id, action) VALUES (%s, %s)", (admin_id, action))
    conn.commit()

# Creates a new user (admin or regular) and logs the action
def create_user(name, email, username, password, role='user', admin_id=None):
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email, username, password, role) VALUES (%s, %s, %s, %s, %s)",
        (name, email, username, hashed, role)
    )
    conn.commit()

    if admin_id:
        log_admin_action(admin_id, f"Created user '{username}' with role '{role}'")

# Deletes a user by user_id and logs the action
def delete_user(user_id, admin_id=None):
    # Fetch username for logging before deletion
    cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()

    if admin_id and user:
        log_admin_action(admin_id, f"Deleted user '{user[0]}' (ID: {user_id})")
