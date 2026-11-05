from pathlib import Path

import duckdb


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SQL_DIR = BASE_DIR / "sql"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


RAW_TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


SQL_OUTPUTS = [
    ("01_order_master.sql", "order_master", "order_master.csv"),
    ("02_customer_summary.sql", "customer_summary", "customer_summary.csv"),
    ("03_category_summary.sql", "category_summary", "category_summary.csv"),
    ("04_monthly_summary.sql", "monthly_summary", "monthly_summary.csv"),
]


def validate_raw_files() -> None:
    missing_files = []

    for file_name in RAW_TABLES.values():
        file_path = RAW_DIR / file_name
        if not file_path.exists():
            missing_files.append(file_name)

    if missing_files:
        raise FileNotFoundError(
            "Missing raw files in data/raw/: " + ", ".join(missing_files)
        )


def register_raw_tables(connection) -> None:
    for table_name, file_name in RAW_TABLES.items():
        file_path = RAW_DIR / file_name

        connection.execute(
            f"""
            CREATE OR REPLACE VIEW {table_name} AS
            SELECT *
            FROM read_csv_auto('{file_path.as_posix()}', header = TRUE)
            """
        )

        row_count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(f"Registered {table_name}: {row_count:,} rows")


def run_sql_to_csv(
    connection,
    sql_file: str,
    table_name: str,
    output_file: str,
) -> None:
    query_path = SQL_DIR / sql_file
    output_path = PROCESSED_DIR / output_file

    query = query_path.read_text(encoding="utf-8")
    connection.execute(query)

    result_df = connection.execute(f"SELECT * FROM {table_name}").df()
    result_df.to_csv(output_path, index=False)

    print(
        f"Saved {output_file}: "
        f"{result_df.shape[0]:,} rows, {result_df.shape[1]} columns"
    )


def main() -> None:
    validate_raw_files()

    connection = duckdb.connect(database=":memory:")

    try:
        register_raw_tables(connection)

        for sql_file, table_name, output_file in SQL_OUTPUTS:
            run_sql_to_csv(connection, sql_file, table_name, output_file)

    finally:
        connection.close()


if __name__ == "__main__":
    main()