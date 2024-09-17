import psycopg2
from psycopg2 import OperationalError

class PostgresConnection:
    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        # Attempt to connect to PostgreSQL database
        try:
            self.connect = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection to PostgreSQL DB successful")
        
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            self.connection = None

    def disconnect(self):
        # Attempt to disconnect from the PostgreSQL database
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection Closed")
        else:
            print("No active connection to close")

    # TODO: Add functions for building tables and retrieving data





