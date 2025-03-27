queries = {
    "CREATE_TABLE_RAW_DATA": """
    CREATE TABLE IF NOT EXISTS raw_data (
        id VARCHAR(256),
        company_name VARCHAR(130),
        company_id VARCHAR(256),
        amount DECIMAL(16,2),
        status VARCHAR(30),
        created_at TIMESTAMP,
        updated_at TIMESTAMP NULL
    );
    """,

    "INSERT_RAW_DATA": """
    INSERT INTO raw_data (id, company_name, company_id, amount, status, created_at, updated_at)
    VALUES %s
    """,

    "SELECT_RAW_DATA": """
    SELECT * FROM raw_data LIMIT %s;
    """
}
