import mysql.connector


def connetDB():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="alee",
        database="dbtaller"
    )
