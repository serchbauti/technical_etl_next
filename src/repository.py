from queries import queries
from psycopg2.extras import execute_values
from utils.cleaner import DataCleaner
from db import Database


class DataRepository:

    def __init__(self, batch_size=100):
        self.db = Database()
        self.batch_size = batch_size

    @staticmethod
    def dict_to_tuple(row):
        return tuple(row.values())

    def create_table(self):
        query = queries["CREATE_TABLE_RAW_DATA"]
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        print("Tabla raw_data creada correctamente.")

    def _batch_generator(self, data):
        for i in range(0, len(data), self.batch_size):
            yield data[i:i + self.batch_size]

    def clean_data(self, data):
        """Limpia los datos antes de la inserción."""
        cleaned_data = [DataCleaner.clean_row(row) for row in data]
        return [row for row in cleaned_data if row]

    def insert_data(self, data):
        query = queries["INSERT_RAW_DATA"]
        cleaned_data = self.clean_data(data)
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                for batch in self._batch_generator(cleaned_data):
                    batch_tuples = [self.dict_to_tuple(row) for row in batch]
                    execute_values(cursor, query, batch_tuples)
                    conn.commit()
                    print(f"✅ Lote de {len(batch)} registros insertados.")
