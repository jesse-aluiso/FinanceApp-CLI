import pandas as pd
import mysql.connector
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from datetime import datetime

load_dotenv()

def forecast_spending(user_id, category_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="finance_app_shcema"
    )
    cursor = conn.cursor()

    #Get category_id
    cursor.execute("SELECT category_id FROM categories WHERE user_id = %s AND name = %s", (user_id, category_name))
    result = cursor.fetchone()
    if not result:
        print("Category '{category_name}' not found.")
        conn.close()
        return
    category_id = result[0]

    #Query transactions
    query = """
    SELECT amount, DATE_FORMAT(date, '%Y-%m') AS month
    FROM transactions
    WHERE user_id = %s AND category_id = %s
    """

    cursor.execute(query, (user_id, category_id))
    rows = cursor.fetchall()

    if not rows:
        print("No transactions for category '{category_name}'.")
        conn.close()
        return
    
    #Build DataFrame - Forecast logic
    df = pd.DataFrame(rows, columns=["amount", "month"])
    df = df.groupby("month")["amount"].sum().reset_index()
    df["month_num"] = range(len(df))
    if df.empty:
        print("DataFrame is empty. Check query and transaction dates.")
        print("Raw rows:", rows)
        return
    print("DataFrame preview:")
    print(df)

    if len(df) < 2:
        print("Not enough data to forecast. Add more transactions.")
        conn.close()
        return

    train_df = df.iloc[:-1]
    test_df = df.iloc[-1:]

    X_train = train_df[["month_num"]]
    y_train = train_df["amount"]
    X_test = test_df[["month_num"]]
    y_test = test_df["amount"]

    #Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    #Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"Model trained: Last month actual: ${y_test.values[0]:.2f}, predicted: ${y_pred[0]:.2f}")
    print(f"MSE: {mse:.2f}, MAE: {mae:.2f}")

    #Forecast next month
    next_month = [[df["month_num"].max() + 1]]
    forecast = model.predict(next_month)[0]
    #X = df[["month_num"]]
    #y = df["amount"]
    #model.fit(X, y)

    print(f"Forecast: You are predicted to spend ~${forecast:.2f} on {category_name} next month.")

    #Visualization
    forecast_month_label = f"{df['month'].iloc[-1]} + 1"
    df_forecast = pd.DataFrame({
        "month": list(df["month"]) + [forecast_month_label],
        "amount": list(df["amount"]) + [forecast]
    })

    plt.figure(figsize=(10,5))
    plt.plot(df_forecast["month"], df_forecast["amount"], marker='*', label="Spending")
    plt.axvline(x=df["month"].iloc[-1], color='gray', linestyle='--', label="Forecast Start")
    plt.title(f"Spending Forecast for '{category_name}'")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("spending_forecast.png")
    plt.show()

    #Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Spending_analysis_{timestamp}.xlsx"
    #Export to excel
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="Actual Spending", index=False)
        df_forecast.to_excel(writer, sheet_name="Forecast", index=False)

    conn.close()
