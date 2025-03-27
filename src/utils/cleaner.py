
"""Utils Cleaner"""
from datetime import datetime


class DataCleaner:
    """A utility class for cleaning and validating data rows.
    This class provides static methods to validate names and rows,
    parse amounts and dates,replace invalid company IDs and names,
    and clean data rows by applying these operations.
    """
    @staticmethod
    def is_valid_name(name):
        """Validates a given name.
        This method checks if the provided name is not empty or null.
        Args:
            name (str): The name to validate.
        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if not name or name.strip() == "":
            print("Fila omitida: Nombre vacío o nulo ⚠️")
            return False
        return True

    @staticmethod
    def is_valid_row(row):
        """Validates the structure of a data row.
        This method checks if the specified indices in the row are non-empty.
        Args:
            row (list): The data row to validate.
        Returns:
            bool: True if all specified elements in the row are valid,
            False otherwise.
        """
        return all([row[0], row[2], row[3], row[4], row[5]])

    @staticmethod
    def parse_amount(amount):
        """Parses and rounds a monetary amount.
        This method attempts to convert the given amount to a float
        and rounds it to two decimal places.
        Args:
            amount (str): The monetary amount to parse and round.
        Returns:
            float or None: The rounded amount, 0 if the amount is
            excessively large, or None if parsing fails.
        """
        try:
            parsed_amount = round(float(amount), 2)
            if abs(parsed_amount) > 1e14:
                return 0
            return round(parsed_amount, 2)
        except ValueError:
            return None

    @staticmethod
    def parse_date(date_str):
        """Parses a date string into a date object.
        This method attempts to convert the given date string into a
        date object using the format "%Y-%m-%d".
        Args:
            date_str (str): The date string to parse.
        Returns:
            datetime.date or None: The parsed date object,
            or None if parsing fails or the input is empty.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        except ValueError:
            return None

    @staticmethod
    def replace_invalid_company_id(company_id):
        """Replaces an invalid company ID with a default value.
        This method checks if the provided company ID is equal to '*******'.
        Args:
            company_id (str): The company ID to validate and potentially
            replace.
        Returns:
            str: The original company ID if valid, or a default company ID
            if invalid.
        """
        if company_id == '*******':
            return 'cbf1c8b09cd5b549416d49d220a40cbd317f952e'
        return company_id

    @staticmethod
    def replace_invalid_name(name):
        """Replaces invalid names with a default name.
        This method checks if the provided name is in a list of known
        invalid names.
        Args:
            name (str): The name to validate and potentially replace.
        Returns:
            str: The original name if valid, or a default name if invalid.
        """
        if name in ["MiP0xFFFF", "MiPas0xFFFF"]:
            return 'MiPasajefy'
        return name

    @staticmethod
    def clean_row(row):
        """Cleans and validates a data row.
        If any validation or parsing fails, the method returns None.
        Otherwise, it returns a dictionary with the cleaned and
        validated data.
        Args:
            row (list): The data row to clean and validate.
        Returns:
            dict or None: A dictionary containing the cleaned data if
            valid, or None if any validation fails.
        """
        if not DataCleaner.is_valid_row(row):
            return None
        id, name, company_id, amount, status, created_at, paid_at = row
        amount = DataCleaner.parse_amount(amount)
        created_at = DataCleaner.parse_date(created_at)
        paid_at = DataCleaner.parse_date(paid_at)
        company_id = DataCleaner.replace_invalid_company_id(company_id)
        name = DataCleaner.replace_invalid_name(name)
        if not DataCleaner.is_valid_name(name):
            return None
        if amount is None or created_at is None:
            return None
        return {
            "id": id,
            "name": name,
            "company_id": company_id,
            "amount": amount,
            "status": status,
            "created_at": created_at,
            "paid_at": paid_at
        }
