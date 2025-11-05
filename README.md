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
