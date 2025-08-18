# import libraries
import os
import psycopg2
from dotenv import load_dotenv

# import libraries
import psycopg2

class Database:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection to the database established successfully.")
            return self.connection
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None
    def create_table(self, create_table_sql):
        if self.connection is None:
            print("No connection to the database. Please connect first.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            print("Table created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to the database closed.")
