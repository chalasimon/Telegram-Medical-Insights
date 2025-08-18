# import libraries
import os
import psycopg2
from dotenv import load_dotenv
import psycopg2.extras


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


    def insert_dataframe(self, df, table_name):
        """
        Bulk insert a pandas DataFrame into Postgres using execute_values
        """
        if self.connection is None:
            print("No connection. Please connect first.")
            return
        if df.empty:
            print("⚠️ DataFrame is empty, skipping insert.")
            return

        cols = list(df.columns)
        values = [tuple(x) for x in df.to_numpy()]
        insert_sql = f"INSERT INTO {table_name} ({','.join(cols)}) VALUES %s ON CONFLICT DO NOTHING;"

        try:
            cursor = self.connection.cursor()
            psycopg2.extras.execute_values(cursor, insert_sql, values)
            self.connection.commit()
            cursor.close()
            print(f"✅ Inserted {len(df)} records into {table_name}.")
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            self.connection.rollback()
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to the database closed.")
