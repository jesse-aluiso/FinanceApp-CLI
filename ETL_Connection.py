import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"), # Securely fetch password from .env
    database="finance_app_shcema"
)


query = "SELECT account_id, user_id, account_type, balance FROM accounts"
df_accounts = pd.read_sql(query, conn)

df_accounts['account_type'] = df_accounts['account_type'].str.title()

summary = df_accounts.groupby('account_type')['balance'].agg(['count', 'sum', 'mean']).reset_index()
print("Account Summary:\n", summary)

with pd.ExcelWriter("finance_report.xlsx") as writer:
    df_accounts.to_excel(writer, sheet_name="Accounts", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)

sns.barplot(data=summary, x='account_type', y='sum')
plt.title("Total Balance by Account Type")
plt.ylabel("Total Balance($)")
plt.xlabel("Account Type")
plt.show()

query_log = """
SELECT a.account_type, l.action, COUNT(*) as count
FROM activity_log l
JOIN accounts a ON l.user_id = a.user_id
GROUP BY a.account_type, l.action
"""
df_log_summary = pd.read_sql(query, conn)
print("Activity Log Summary:\n", df_log_summary)
