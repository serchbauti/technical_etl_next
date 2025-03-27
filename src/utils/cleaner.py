import uuid
from datetime import datetime


class DataCleaner:

    @staticmethod
    def is_valid_name(name):
        if not name or name.strip() == "":
            print("Fila omitida: Nombre vacío o nulo.")
            return False
        return True

    @staticmethod
    def is_valid_row(row):
        return all([row[0], row[2], row[3], row[4], row[5]])

    @staticmethod
    def parse_amount(amount):
        try:
            parsed_amount = round(float(amount), 2)
            if abs(parsed_amount) > 1e14:
                return 0
            return round(parsed_amount, 2)
        except ValueError:
            return None

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        except ValueError:
            return None

    @staticmethod
    def convert_id_to_uuid(id_value):
        try:
            return str(uuid.UUID(id_value))
        except ValueError:
            print(f"Error: ID '{id_value}' no es un UUID válido.")
            return uuid.uuid5(uuid.NAMESPACE_DNS, id_value)

    @staticmethod
    def replace_invalid_company_id(company_id):
        """Reemplaza el company_id '*******' con el UUID específico"""
        if company_id == '*******':
            return 'cbf1c8b09cd5b549416d49d220a40cbd317f952e'
        return company_id

    @staticmethod
    def replace_invalid_name(name):
        if name in ["MiP0xFFFF", "MiPas0xFFFF"]:
            return 'MiPasajefy'
        return name

    @staticmethod
    def clean_row(row):
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
