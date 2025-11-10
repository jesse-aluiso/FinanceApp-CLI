💰 FinanceApp CLI
A secure, role-aware command-line banking system built in Python. Supports user authentication, account management, deposits, withdrawals, audit logging — and now spending forecasts with charting and Excel export.

🚀 Features
🔐 Secure login with bcrypt password hashing

👤 Role-based access: admin vs user

🏦 Account types: Checking, Savings, Retirement

💸 Deposit and withdrawal with overdraft protection

📜 Audit logs for admin and user actions

📊 Spending forecast with chart visualization

📁 Excel export with timestamped reports

🧾 View account summaries and activity history

📈 New Forecasting Capabilities
🧠 Predict next month’s spending using Linear Regression

📅 Group transactions by month for trend analysis

📊 Visualize actual vs predicted spending with matplotlib

📁 Export forecast and historical data to Excel with timestamped filenames

🧪 Simulate multi-month transactions for testing

🛠️ Setup
bash
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
Use MySQL Workbench or CLI to create the schema and tables. Make sure the database name matches .env. You can simulate past transactions by specifying how many days ago they occurred.

📂 File Structure
Code
finance_app/
├── .env
├── db.py
├── auth.py
├── finance_app.py
├── forecast_module.py
├── cli.py
├── user_log.py
├── README.md
├── requirements.txt
📦 requirements.txt
text
mysql-connector-python  
python-dotenv  
bcrypt  
pandas  
scikit-learn  
matplotlib  
openpyxl
🧠 Data Structures & Logic
Relational Tables (SQL-backed)
Table Name	Purpose
users	Stores user credentials, roles, and metadata
password_history	Tracks last 3 password hashes per user
audit_log	Logs admin actions for accountability
transactions	Logs deposits/withdrawals with category/date
categories	User-defined spending categories
Python Structures
Dictionaries: Used to pass user session data

Lists: Used for password reuse checks

DataFrames: Used for forecasting and Excel export

⚙️ Algorithms and Security
bcrypt for password hashing and verification

Password reuse prevention via history tracking

Password expiry enforcement

Audit logging for all admin actions

Forecasting using LinearRegression from scikit-learn

Excel export using pandas and openpyxl

🧩 Opportunities
✅ Security: Strong use of bcrypt, password history, and expiry logic ✅ Scalability: SQL-backed design supports growth and indexing ✅ Auditability: Admin actions are traceable ✅ Analytics: Forecasting and export features mirror enterprise-grade workflows 🧩 Future: Embed charts in Excel, auto-archive reports, add monthly summaries
