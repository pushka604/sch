import mysql.connector

# Definiowanie zmiennej z konfiguracją serwera
server_config = {
    "host": "192.168.1.104",  # Use your Windows machine's IP address
    "user": "root",
    "password": "",
    "database": "schronisko"
}

def read_users():
    # Użycie konfiguracji serwera do połączenia z bazą danych
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

def create_new_user(username, password, role, employee_id=None):
    
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = 'INSERT INTO users (username, password, role, employee_id) VALUES (%s, %s, %s, %s)'
    params = (username, password, role, employee_id)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()