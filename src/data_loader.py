import csv
from repository import DataRepository


class DataLoader:
    def __init__(self, file_path, batch_size=100):
        self.file_path = file_path
        self.batch_size = batch_size
        self.repository = DataRepository(batch_size=batch_size)

    def _read_csv(self):
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            couter = 0
            next(reader)
            for row in reader:
                if row:
                    couter += 1
                    print(f"Fila procesado {couter}")
                    yield row
                else:
                    pass

    def load_data(self):
        print("🚀 Iniciando carga de datos...")
        self.repository.create_table()
        batch = []
        for row in self._read_csv():
            batch.append(row)
            if len(batch) >= self.batch_size:
                self.repository.insert_data(batch)
                batch = []
        if batch:
            self.repository.insert_data(batch)
        print("✅ Carga de datos completada.")


if __name__ == "__main__":
    DATASET_PATH = "src/data_prueba_técnica.csv"
    loader = DataLoader(DATASET_PATH, batch_size=100)
    loader.load_data()
