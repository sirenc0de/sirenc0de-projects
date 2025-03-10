from db_utils import get_db_connection

conn = get_db_connection()
if conn:
    print("Connected to MySQL successfully!")
    conn.close()
else:
    print("Failed to connect to MySQL.")
