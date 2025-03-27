"""Repository"""
from psycopg2.extras import execute_values

from db import Database
from queries import queries
from utils.cleaner import DataCleaner


class DataRepository:
    """A class to manage data operations in the database."""

    def __init__(self, batch_size=100):
        self.db = Database()
        self.batch_size = batch_size
        self.conn = self.db.get_connection()
        self.cursor = self.conn.cursor()

    @staticmethod
    def dict_to_tuple(row):
        """Convert a dictionary values to a tuple.
        Args:
            row (dict): The dictionary to convert.
        Returns:
            tuple: A tuple containing the dictionary values.
        """
        return tuple(row.values())

    def create_raw_table(self):
        """Create the raw_data table in the database"""
        self.cursor.execute(queries["CREATE_TABLE_RAW_DATA"])
        self.conn.commit()
        print("Tabla raw_data creada correctamente ✅")

    def create_companies_table(self):
        """Create the companies table in the database"""
        self.cursor.execute(queries["CREATE_TABLE_COMPANIES"])
        print("Tabla companies creada correctamente ✅")

    def create_charges_table(self):
        """Create the cahrge table in the database"""
        self.cursor.execute(queries["CREATE_TABLE_CHARGES"])
        print("Tabla charges creada correctamente ✅")

    def _batch_generator(self, data):
        for i in range(0, len(data), self.batch_size):
            yield data[i:i + self.batch_size]

    def clean_data(self, data):
        """Clean data with utils cleaner"""
        cleaned_data = [DataCleaner.clean_row(row) for row in data]
        return [row for row in cleaned_data if row]

    def insert_data(self, data):
        """Insert cleaned data into the raw_data table in batches"""
        query = queries["INSERT_RAW_DATA"]
        cleaned_data = self.clean_data(data)
        print("Datos limpios preparados para inserción 💾")
        for batch in self._batch_generator(cleaned_data):
            batch_tuples = [self.dict_to_tuple(row) for row in batch]
            execute_values(self.cursor, query, batch_tuples)
            self.conn.commit()
            print(f"Lote de {len(batch)} registros insertados 💾")

    def insert_companies(self):
        """Insert company data into the companies table"""
        self.cursor.execute(queries["INSERT_COMPANIES"])
        print("Empresas insertadas correctamente ✅")

    def insert_charges(self):
        """Insert charges data into the companies table"""
        self.cursor.execute(queries["INSERT_CHARGES"])
        print("Cargos insertados correctamente ✅")

    def create_daily_transaction_summary_view(self):
        """Create view daily_transaction_summary in database"""
        self.cursor.execute(queries["CREATE_VIEW_DAILY_TRANSACTION_REPORT"])
        print("Vista 'daily_transaction_summary_v2' creada correctamente ✅")

    def drop_raw_data_table(self):
        """Drop raw_data"""
        self.cursor.execute(queries["DROP_TABLE_RAW_DATA"])
        print("Tabla raw_data eliminada correctamente ✅")

    def disperse_data_from_raw(self):
        """Process and disperse data from the raw_data table to other tables.
        This method orchestrates the creation of necessary tables, insertion
        of data into the companies and charges tables, creation of a summary
        view, and removal of the raw_data table.
        Prints:
            A success message upon completion or an error message if an
            exception occurs.
        Raises:
            Exception: If any operation within the transaction fails.
        Finally:
            Closes the database connection and cursor to release resources.
        """
        try:
            self.create_companies_table()
            self.create_charges_table()
            self.insert_companies()
            self.insert_charges()
            self.create_daily_transaction_summary_view()
            self.drop_raw_data_table()
            self.conn.commit()
            print("Dispersión de datos completada con éxito ✅")
        except Exception as e:
            self.conn.rollback()
            print(f"Error en la dispersión de datos: {e} 🛑")
        finally:
            self.close()

    def close(self):
        """Close the database cursor and connection"""
        self.cursor.close()
        self.conn.close()
        print("Conexión cerrada correctamente ✅")
