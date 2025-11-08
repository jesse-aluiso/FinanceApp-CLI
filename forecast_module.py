import pandas as pd
import mysql.connector
from sklearn.linear_model import LinearRegression
import os
from dotenv import load_dotenv

load_dotenv()

def forecast_spending(user_id, category):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="finance_app_schema"
    )

    query = """
    SELECT amout, DATE_FORMAT(timestamp, '%%Y-%%m) AS month
    FROM transactions
    WHERE category = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (category,))
    rows = cursor.fetchall()

    if not rows:
        print("No transactions for category: {category}")
        return
    
    df = pd.DataFrame(rows, columns=["amount", "month"])
    df = df.groupby("month")["amount"].sum().reset_index()
    df["month_num"] = range(len(df))

    X = df[["month_num"]]
    y = df["amount"]
    model = LinearRegression()
    model.fit(X, y)

    next_month = [[df["month_num"].max() + 1]]
    forecast = model.predict(next_month)[0]

    print(f"Forecast: You are predicted to spend ~${forecast:.2f} on {category} next month.")
