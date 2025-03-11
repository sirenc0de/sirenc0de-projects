import mysql.connector
from config import DB_CONFIG

def test_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connected to MySQL successfully!")
            conn.close()
        else:
            print("Connection Failure!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()