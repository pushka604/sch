import mysql.connector


def read_employees():
# Replace with your Windows IP address, MySQL username, password, and database
    connection = mysql.connector.connect(
        host="192.168.1.104",  # Use your Windows machine's IP address
        user="root",
        password="",
        database="schronisko"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees


