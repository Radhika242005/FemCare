import mysql.connector


def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Radhika@2005",
        database="femcare"
    )

    return connection