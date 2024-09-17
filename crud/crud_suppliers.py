import mysql.connector

# Definiowanie zmiennej z konfiguracją serwera
server_config = {
    "host": "192.168.1.104",  # Use your Windows machine's IP address
    "user": "root",
    "password": "",
    "database": "schronisko"
}

def read_suppliers():
    # Użycie konfiguracji serwera do połączenia z bazą danych
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return suppliers

def read_supplier(supplier_id):
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM suppliers WHERE id = %s', (supplier_id,))
    supplier = cursor.fetchone()

    cursor.close()
    connection.close()

    return supplier

def create_supplier(name, city):

    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = 'INSERT INTO supplier (name, city) VALUES (%s, %s)'
    params = (name, city)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
    
def update_supplier(supplier_id, name=None, city=None):

    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = 'UPDATE supplier SET'
    params = []

    if name is not None:
        query += ' name = %s,'
        params.append(name)
    
    if city is not None:
        query += ' city = %s,'
        params.append(city)
    
    query = query.rstrip(',') + ' WHERE supplier_id = %s'
    params.append(supplier_id)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def delete_supplier(supplier_id):

    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = 'DELETE FROM supplier WHERE supplier_id = %s'
    params = (supplier_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

