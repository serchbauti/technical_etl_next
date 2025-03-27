"""Main ETL"""
import csv
from repository import DataRepository


class DataLoader:
    """DataLoader class for handling ETL processes."""
    def __init__(self, file_path, batch_size=100):
        self.file_path = file_path
        self.batch_size = batch_size
        self.repository = DataRepository(batch_size=batch_size)

    def _read_csv(self):
        """Reads data from a CSV file."""
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            couter = 0
            next(reader)
            for row in reader:
                if row:
                    couter += 1
                    print(f"Fila procesada {couter} ✅")
                    yield row
                else:
                    pass

    def _load_data(self):
        """Loads data from a CSV file into the database."""
        print("Iniciando carga de datos 🚀")
        self.repository.create_raw_table()
        batch = []
        for row in self._read_csv():
            batch.append(row)
            if len(batch) >= self.batch_size:
                self.repository.insert_data(batch)
                batch = []
        if batch:
            self.repository.insert_data(batch)
        print("Carga de datos completada ✅")

    def _disperse_data(self):
        """Handles the dispersion of data from raw tables into
        structured tables within the database.
        """
        print("Iniciando dispersión de datos 🚀")
        self.repository.disperse_data_from_raw()
        print("Dispersión de datos completada ✅")

    def run_etl(self):
        """Executes the ETL process by loading and dispersing data.
        This method orchestrates the ETL process.
        """
        try:
            self._load_data()
            self._disperse_data()
            print("ETL finalizado con éxito ✅")
        except Exception as e:
            print(f"Error en el proceso ETL: {e} 🛑")
        finally:
            self.repository.close()


if __name__ == "__main__":
    DATASET_PATH = "src/data_prueba_técnica.csv"
    loader = DataLoader(DATASET_PATH, batch_size=100)
    loader.run_etl()
