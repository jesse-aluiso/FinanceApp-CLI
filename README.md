# 💰 FinanceApp CLI

A secure, role-aware command-line banking system built in Python. Supports user authentication, account management, deposits, withdrawals, and audit logging.

## 🚀 Features

- 🔐 Secure login with bcrypt password hashing
- 👤 Role-based access: admin vs user
- 🏦 Account types: Checking, Savings, Retirement
- 💸 Deposit and withdrawal with overdraft protection
- 📜 Audit logs for admin and user actions
- 🧾 View account summaries and activity history

## 🛠️ Setup

1. Clone the repo:
   git clone https://github.com/jesse-aluiso/FinanceApp-CLI.git
   cd FinanceApp-CLI
Create a .env file:

env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=finance_app_schema
Install dependencies:

bash
pip install -r requirements.txt
Run the CLI:

bash
python cli.py
🧪 Testing
Use MySQL Workbench or CLI to create the schema and tables. Make sure the database name matches .env.

📂 File Structure
Code
finance_app/
├── .env
├── db.py
├── auth.py
├── finance_app.py
├── cli.py
├── user_log.py
├── README.md
├── requirements.txt
📜 License
MIT License

## 📦 `requirements.txt`

This file lists all Python packages your app depends on:
mysql-connector-python
python-dotenv
bcrypt

mysql-connector-python
python-dotenv
bcrypt

🧠 Data Structures in auth.py
1. Relational Tables (SQL-backed)
These are your core persistent data structures:

Table Name	Purpose
users	Stores user credentials, roles, and metadata
password_history	Tracks last 3 password hashes per user
audit_log	Logs admin actions for accountability
These are implemented as normalized relational tables, ideal for structured, queryable data with referential integrity.

2. Python Dictionaries
Used in authenticate_user() to return user session data:

python
return {
    "user_id": result[0],
    "username": result[1],
    "role": result[3],
    "is_temp_password": result[4] or is_expired
}
✅ Efficient for passing structured user state between functions.

3. Lists
Used to aggregate password hashes for reuse checks:

python
for old in [current_hash[0]] + [r[0] for r in recent_hashes]:
✅ Simple linear structure for iteration and comparison.

⚙️ Algorithms and Logic
1. Password Hashing and Verification
Uses bcrypt for secure one-way hashing

Salted hashes prevent rainbow table attacks

bcrypt.checkpw() ensures constant-time comparison

🔐 Security-first algorithm with built-in resistance to brute-force and timing attacks.

2. Password Reuse Prevention
Fetches last 3 hashes from password_history

Compares new password against each using bcrypt.checkpw()

Deletes older hashes beyond the last 3

🧠 Linear search over a small fixed list — efficient and secure.

3. Password Expiry Enforcement
Compares password_expiry date to date.today()

Forces is_temp_password = True if expired

📅 Simple date comparison — constant time, low overhead.

4. Audit Logging
Every admin action is logged with log_admin_action(admin_id, action)

Ensures traceability and accountability

🧾 Append-only logging — ideal for audit trails and forensic analysis.

5. User Editing Logic
Validates field name against a list

Handles special cases (password, password_expiry)

Uses dynamic SQL for generic updates

🛠️ Field-aware branching with secure update logic.

🧪 Observations and Opportunities
✅ Security: Strong use of bcrypt, password history, and expiry logic

✅ Scalability: SQL-backed design supports growth and indexing

✅ Auditability: Admin actions are traceable

🧩 Opportunity: You could abstract field validation and update logic into a reusable class or service layer for cleaner separation
