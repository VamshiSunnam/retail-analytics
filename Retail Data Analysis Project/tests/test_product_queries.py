import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os
import json

# Helper function to get DB connection string (copied from scripts/run_analysis.py for self-containment)
def get_db_connection_string(env='development'):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'database_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    db_config = config.get(env)
    if not db_config:
        raise ValueError(f"Environment '{env}' not found in database_config.json")

    driver = db_config['driver']
    host = db_config['host']
    port = db_config['port']
    database = db_config['database']
    user = db_config['user']
    password = db_config['password']

    if driver == 'mysql':
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    elif driver == 'postgresql':
        raise ValueError("PostgreSQL not yet implemented for this test.")
    else:
        raise ValueError(f"Unsupported database driver: {driver}")

@pytest.fixture(scope='module')
def db_engine():
    try:
        db_connection_str = get_db_connection_string('development')
        engine = create_engine(db_connection_str)
        # Attempt to connect to verify credentials and server status
        with engine.connect() as connection:
            connection.execute(pd.text("SELECT 1"))
        return engine
    except OperationalError as e:
        pytest.skip(f"Database connection failed: {e}. Skipping database tests.")
    except Exception as e:
        pytest.fail(f"Failed to set up database engine: {e}")

def load_sql_query(query_file_path):
    with open(query_file_path, 'r') as f:
        return f.read()

def test_top_products_query_schema(db_engine):
    query_file_path = os.path.join(os.path.dirname(__file__), '..', 'queries', 'product_analysis', 'top_products.sql')
    sql_query = load_sql_query(query_file_path)

    df = pd.read_sql(sql_query, db_engine)

    # 1. Verify expected columns exist
    expected_columns = ['product_name', 'total_quantity_sold', 'total_revenue_generated']
    assert all(col in df.columns for col in expected_columns), \
        f"Missing expected columns. Expected: {expected_columns}, Got: {df.columns.tolist()}"

    # 2. Verify data types of numerical columns
    # Note: Pandas might infer int for quantity if all values are integers, or float if there are NaNs or decimals.
    # For sum of quantity, int is generally expected. For sum of decimal, float is expected.
    assert pd.api.types.is_string_dtype(df['product_name']), "product_name should be string type"
    assert pd.api.types.is_integer_dtype(df['total_quantity_sold']), "total_quantity_sold should be integer type"
    assert pd.api.types.is_float_dtype(df['total_revenue_generated']), "total_revenue_generated should be float type"

    # 3. Verify data is returned (assuming there's data in the database)
    assert not df.empty, "Query returned an empty DataFrame. Ensure there is data in the database."
