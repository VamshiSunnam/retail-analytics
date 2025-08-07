import pandas as pd
import json
from sqlalchemy import create_engine
import os

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
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError(f"Unsupported database driver: {driver}")

def load_csv_to_db(file_path, table_name, engine):
    print(f"Loading {file_path} into table {table_name}...")
    df = pd.read_csv(file_path)
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} rows into {table_name}.")
    except Exception as e:
        print(f"Error loading data into {table_name}: {e}")

if __name__ == "__main__":
    try:
        db_connection_str = get_db_connection_string('development')
        engine = create_engine(db_connection_str)

        # Define paths to your CSV files
        base_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data')
        orders_csv_path = os.path.join(base_data_path, 'orders.csv')
        order_items_csv_path = os.path.join(base_data_path, 'order_items.csv')
        
        # Load data
        load_csv_to_db(orders_csv_path, 'Orders', engine)
        load_csv_to_db(order_items_csv_path, 'Order_Items', engine)

    except Exception as e:
        print(f"An error occurred: {e}")
