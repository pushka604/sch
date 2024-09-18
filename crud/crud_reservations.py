import mysql.connector

server_config = {
    "host": "192.168.1.104",  
    "user": "root",
    "password": "",
    "database": "schronisko"
}

def create_reservation(user_id, dog_id, date_and_hours):
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)

    query = "INSERT INTO dog_walking (user_id, dog_id, date_and_hours) VALUES (%s, %s, %s)"
    params = (user_id, dog_id, date_and_hours)
    
    try:
        cursor.execute(query, params)
        connection.commit()
        reservation_id = cursor.lastrowid
        return reservation_id
    except mysql.connector.Error as err:
        connection.rollback()
    

def read_reservations(dog_id):
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT date_and_hours FROM dog_walking WHERE dog_id = %s", (dog_id,))
    reservations = cursor.fetchall()

    return reservations

