import unittest
from src.utils.cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):

    def test_is_valid_name_valid(self):
        valid_name = "Company ABC"
        self.assertTrue(DataCleaner.is_valid_name(valid_name))

    def test_is_valid_name_invalid(self):
        invalid_name = ""
        self.assertFalse(DataCleaner.is_valid_name(invalid_name))

    def test_parse_amount_valid(self):
        valid_amount = "123.45"
        self.assertEqual(DataCleaner.parse_amount(valid_amount), 123.45)

    def test_parse_amount_invalid(self):
        invalid_amount = "invalid"
        self.assertIsNone(DataCleaner.parse_amount(invalid_amount))

    def test_parse_date_invalid(self):
        invalid_date = "invalid"
        self.assertIsNone(DataCleaner.parse_date(invalid_date))

    def test_replace_invalid_company_id(self):
        invalid_company_id = "*******"
        self.assertEqual(DataCleaner.replace_invalid_company_id(invalid_company_id),
                         'cbf1c8b09cd5b549416d49d220a40cbd317f952e')

    def test_replace_invalid_name(self):
        invalid_name = "MiP0xFFFF"
        self.assertEqual(DataCleaner.replace_invalid_name(invalid_name), 'MiPasajefy')

    def test_clean_row_valid(self):
        valid_row = ["1", "Company ABC", "cbf1c8b09cd5b549416d49d220a40cbd317f952e", "100", "active", "2025-03-26", "2025-03-27"]
        cleaned_row = DataCleaner.clean_row(valid_row)
        self.assertIsNotNone(cleaned_row)

    def test_clean_row_invalid(self):
        invalid_row = ["1", "", "cbf1c8b09cd5b549416d49d220a40cbd317f952e", "100", "active", "2025-03-26", "2025-03-27"]
        cleaned_row = DataCleaner.clean_row(invalid_row)
        self.assertIsNone(cleaned_row)