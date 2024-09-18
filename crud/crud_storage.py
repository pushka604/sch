import mysql.connector

server_config = {
    "host": "192.168.1.104",  
    "user": "root",
    "password": "",
    "database": "schronisko"
}

def read_storage():
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT item_id, item_name, quantity, category FROM storage")
    storage = cursor.fetchall()

    return storage

def create_storage_item(item_name):
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = "INSERT INTO storage (item_name, employee_id, supplier_id) VALUES (%s, %s, %s)"
    params = (item_name, 1, 1)

    try:
        cursor.execute(query, params)
        connection.commit()
        item_id = cursor.lastrowid
        return item_id
    except mysql.connector.Error as err:
        connection.rollback()
    
def delete_storage_item(item_id):
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = "DELETE FROM storage WHERE item_id = %s"
    params = (item_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
        success = True
    except mysql.connector.Error as err:
        connection.rollback()

    return success    

