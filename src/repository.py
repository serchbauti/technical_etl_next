from queries import queries
from psycopg2.extras import execute_values
from utils.cleaner import DataCleaner
from db import Database


class DataRepository:

    def __init__(self, batch_size=100):
        self.db = Database()
        self.batch_size = batch_size
        self.conn = self.db.get_connection()
        self.cursor = self.conn.cursor()

    @staticmethod
    def dict_to_tuple(row):
        return tuple(row.values())

    def create_raw_table(self):
        self.cursor.execute(queries["CREATE_TABLE_RAW_DATA"])
        self.conn.commit()
        print("Tabla raw_data creada correctamente.")

    def create_companies_table(self):
        self.cursor.execute(queries["CREATE_TABLE_COMPANIES"])
        print("Tabla 'companies' creada correctamente.")

    def create_charges_table(self):
        self.cursor.execute(queries["CREATE_TABLE_CHARGES"])
        print("Tabla 'charges' creada correctamente.")

    def _batch_generator(self, data):
        for i in range(0, len(data), self.batch_size):
            yield data[i:i + self.batch_size]

    def clean_data(self, data):
        cleaned_data = [DataCleaner.clean_row(row) for row in data]
        return [row for row in cleaned_data if row]

    def insert_data(self, data):
        query = queries["INSERT_RAW_DATA"]
        cleaned_data = self.clean_data(data)
        print("Datos limpios preparados para inserción.")
        for batch in self._batch_generator(cleaned_data):
            batch_tuples = [self.dict_to_tuple(row) for row in batch]
            execute_values(self.cursor, query, batch_tuples)
            self.conn.commit()
            print(f"Lote de {len(batch)} registros insertados.")

    def insert_companies(self):
        self.cursor.execute(queries["INSERT_COMPANIES"])
        print("Empresas insertadas correctamente.")

    def insert_charges(self):
        self.cursor.execute(queries["INSERT_CHARGES"])
        print("Cargos insertados correctamente.")

    def disperse_data_from_raw(self):
        try:
            self.create_companies_table()
            self.create_charges_table()
            self.insert_companies()
            self.insert_charges()
            self.conn.commit()
            print("Dispersión de datos completada con éxito.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error en la dispersión de datos: {e}")
        finally:
            self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Conexión cerrada correctamente.")
