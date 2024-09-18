import mysql.connector

server_config = {
    "host": "192.168.1.104",  
    "user": "root",
    "password": "",
    "database": "schronisko"
}

def read_dogs():
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT dog_id, name, dog_history, year_of_birth FROM dogs")
    dogs = cursor.fetchall()

    for dog in dogs:
        dog_id = dog["dog_id"]
        cursor.execute("SELECT * FROM dog_treatments WHERE dog_id = %s", (dog_id,))
        treatments = cursor.fetchall()

        if treatments:
            dog["health_history"] = treatments[-1]["description"]
        else:
            dog["health_history"] = ""
        
        cursor.execute("SELECT * FROM adoption WHERE dog_id = %s", (dog_id,))
        adoptions = cursor.fetchall()

        if adoptions:
            dog["adoption"] = "adoptowany"
        else:
            dog["adoption"] = "wolny"


    cursor.close()
    connection.close()

    return dogs

def create_dog(name, dog_history, year_of_birth, treatment_description):
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = "INSERT INTO dogs (name, dog_history, year_of_birth) VALUES (%s, %s, %s)"
    params = (name, dog_history, year_of_birth)

    try:
        cursor.execute(query, params)
        connection.commit()
        dog_id = cursor.lastrowid
    except mysql.connector.Error as err:
        connection.rollback()
    
    query = "INSERT INTO dog_treatments(dog_id, description) VALUES (%s, %s)"
    params = (dog_id, treatment_description)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
    
    return dog_id

def delete_dog(dog_id):
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()
    
    query = "DELETE FROM dog_treatments WHERE dog_id = %s"
    params = (dog_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    
    query = "DELETE FROM adoption WHERE dog_id = %s"
    params = (dog_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
    
    query = "DELETE FROM dog_walking WHERE dog_id = %s"
    params = (dog_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()

    query = "DELETE FROM dogs WHERE dog_id = %s"
    params = (dog_id,)

    try:
        cursor.execute(query, params)
        connection.commit()
        success = True
    except mysql.connector.Error as err:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
    
    return success
    
def update_dog(dog_id, name=None, dog_history=None, year_of_birth=None, adopted=None):
    connection = mysql.connector.connect(**server_config)
    cursor = connection.cursor()

    query = "UPDATE dogs SET"
    params = []

    if name is not None:
        query += ' name = %s,'
        params.append(name)
    
    if dog_history is not None:
        query += ' dog_history = %s,'
        params.append(dog_history)
    
    if year_of_birth is not None:
        query += ' year_of_birth = %s,'
        params.append(year_of_birth)

    query = query.rstrip(',') + ' WHERE dog_id = %s'
    params.append(dog_id)

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()

    if adopted == "adoptowany":
        cursor.execute("SELECT * FROM adoption WHERE dog_id = %s", (dog_id,))
        adoptions = cursor.fetchall()
        if not adoptions:
            query = "INSERT INTO adoption (dog_id, user_id) VALUES (%s, %s)"
            params = (dog_id, 5)
            try:
                cursor.execute(query, params)
                connection.commit()
            except mysql.connector.Error as err:
                connection.rollback()
    if adopted == "wolny":
        query = "DELETE FROM adoption WHERE dog_id = %s"
        params = (dog_id,)
        try:
            cursor.execute(query, params)
            connection.commit()
        except mysql.connector.Error as err:
            connection.rollback()
    
    updated = read_dog(dog_id)

    cursor.close()
    connection.close()

    return updated

def read_dog(dog_id):
    connection = mysql.connector.connect(**server_config)

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM dogs WHERE dog_id = %s", (dog_id,))
    dogs = cursor.fetchone()

    cursor.execute("SELECT * FROM dog_treatments WHERE dog_id = %s", (dog_id,))
    treatments = cursor.fetchall()

    if treatments:
        dogs["health_history"] = treatments[-1]["description"]
    else:
        dogs["health_history"] = ""
    
    cursor.execute("SELECT * FROM adoption WHERE dog_id = %s", (dog_id,))
    adoptions = cursor.fetchall()

    if adoptions:
        dogs["adoption"] = "adoptowany"
    else:
        dogs["adoption"] = "wolny"
    
    cursor.close()
    connection.close()

    return dogs
