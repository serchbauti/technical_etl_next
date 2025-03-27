import unittest
from unittest.mock import patch, MagicMock
from src.etl import DataLoader


class TestDataLoader(unittest.TestCase):

    @patch('src.etl.DataRepository')
    def test_run_etl(self, MockDataRepository):
        mock_repo = MagicMock()
        MockDataRepository.return_value = mock_repo
        loader = DataLoader("src/data_prueba_técnica.csv")
        
        loader.run_etl()

        mock_repo.create_raw_table.assert_called_once()
        mock_repo.disperse_data_from_raw.assert_called_once()
        print("ETL ejecutado correctamente.")

    @patch('src.etl.DataLoader._read_csv')
    @patch('src.etl.DataRepository')
    def test_load_data(self, MockDataRepository, mock_read_csv):
        mock_repo = MagicMock()
        MockDataRepository.return_value = mock_repo
        mock_read_csv.return_value = [["1", "Company ABC", "cbf1c8b09cd5b549416d49d220a40cbd317f952e", "100", "active", "2025-03-26", "2025-03-27"]]
        loader = DataLoader("src/data_prueba_técnica.csv")
        loader._load_data()
        mock_repo.insert_data.assert_called_once()
        print("Carga de datos ejecutada correctamente.")