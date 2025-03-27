import psycopg2


class Database:

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
        """Retorna una conexión a la base de datos."""
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
