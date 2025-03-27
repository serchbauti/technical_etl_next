"""Handler DB"""
import psycopg2


class Database:
    """A class to manage database connections using psycopg2."""
    def __init__(
            self,
            dbname="test_db",
            user="admin",
            password="adminpass",
            host="db",
            port=5432
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_connection(self):
        """Establishes and returns a connection to the
        PostgreSQL database using the instance's configuration parameters.
        Returns:
            psycopg2.extensions.connection: A connection object to
            interact with the database.
        """
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
