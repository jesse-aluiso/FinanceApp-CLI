import mysql.connector # Import the MySQL connector library to interact with MySQL databases
import os # Import the os module to access environment variables
from dotenv import load_dotenv # Import the dotenv loader to read variables from a .env file

# Load environment variables from the .env file into the system environment
load_dotenv()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"), # Securely fetch password from .env
    database="finance_app_shcema"
)
# Create a cursor object to execute SQL queries
# 'buffered=True' allows multiple queries without needing to fetch results immediately
cursor = conn.cursor(buffered=True)
