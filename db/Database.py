<<<<<<< HEAD
import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'kluv'
        self.user = 'root'
        self.password = 'alee'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()

    def fetch_data(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener los datos: {e}")
            return []
=======
import mysql.connector
from mysql.connector import Error

class DBConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'kluv'
        self.user = 'root'
        self.password = 'alee'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()

    def fetch_data(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener los datos: {e}")
            return []
>>>>>>> 43cf25c888ac1565fa18378ddcf8c2381e2dbc89
