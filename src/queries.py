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
    "CREATE_TABLE_COMPANIES": """
        CREATE TABLE IF NOT EXISTS companies (
            id VARCHAR(256) PRIMARY KEY,
            name VARCHAR(130) NOT NULL
        );
    """,
    "CREATE_TABLE_CHARGES": """
        CREATE TABLE IF NOT EXISTS charges (
            id VARCHAR(256) PRIMARY KEY,
            company_id VARCHAR(256) REFERENCES companies(id),
            amount DECIMAL(16,2) NOT NULL,
            status VARCHAR(30) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NULL
        );
    """,
    "INSERT_COMPANIES": """
        INSERT INTO companies (id, name)
        SELECT DISTINCT company_id, company_name
        FROM raw_data
        WHERE company_id IS NOT NULL
        ON CONFLICT (id) DO NOTHING;
    """,
    "INSERT_CHARGES": """
        INSERT INTO charges (id, company_id, amount, status, created_at, updated_at)
        SELECT id, company_id, amount, status, created_at, updated_at
        FROM raw_data
        WHERE id IS NOT NULL
        AND company_id IS NOT NULL
        AND amount IS NOT NULL
        AND created_at IS NOT NULL;
    """
}
