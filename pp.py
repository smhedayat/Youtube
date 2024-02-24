import mysql.connector

try:
    connection=mysql.connector.connect(host='localhost', user='root', password='researchwork15', database='youtube_db')
    if connection.is_connected():
            print(f"Connected to MySQL database")

        # Your database operations go here

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the connection in the finally block to ensure it's always closed
    if connection.is_connected():
        connection.close()
        print("Connection closed")
