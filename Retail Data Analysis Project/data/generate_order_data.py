
import csv
import random
from datetime import datetime, timedelta

def generate_orders_data(num_orders, customer_ids_range=(1, 100)):
    """Generates sample data for the Orders table."""
    orders_data = []
    for i in range(1, num_orders + 1):
        order_id = i
        customer_id = random.randint(customer_ids_range[0], customer_ids_range[1])
        order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        total_amount = round(random.uniform(10.0, 1000.0), 2)
        order_status = random.choice(['Pending', 'Completed', 'Cancelled'])
        shipping_address = f"Address {random.randint(1, 100)}"
        shipping_city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
        shipping_state = random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])
        shipping_zip_code = f"{random.randint(10000, 99999)}"
        orders_data.append([order_id, customer_id, order_date, total_amount, order_status,
                            shipping_address, shipping_city, shipping_state, shipping_zip_code])
    return orders_data

def generate_order_items_data(num_order_items, order_ids_range, product_ids_range=(1, 50)):
    """Generates sample data for the Order_Items table."""
    order_items_data = []
    for i in range(1, num_order_items + 1):
        order_item_id = i
        order_id = random.randint(order_ids_range[0], order_ids_range[1])
        product_id = random.randint(product_ids_range[0], product_ids_range[1])
        quantity = random.randint(1, 5)
        price_per_unit = round(random.uniform(5.0, 500.0), 2)
        order_items_data.append([order_item_id, order_id, product_id, quantity, price_per_unit])
    return order_items_data

# Configuration
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1000
CUSTOMER_IDS_RANGE = (1, 100) # Assuming customer_ids exist from 1 to 100
PRODUCT_IDS_RANGE = (1, 50)   # Assuming product_ids exist from 1 to 50

# Generate data
orders_data = generate_orders_data(NUM_ORDERS, CUSTOMER_IDS_RANGE)
order_ids_range = (1, NUM_ORDERS) # Order IDs will be from 1 to NUM_ORDERS
order_items_data = generate_order_items_data(NUM_ORDER_ITEMS, order_ids_range, PRODUCT_IDS_RANGE)

# Define file paths
orders_csv_path = r"C:\Users\vamsh\OneDrive\Desktop\Project SQL\Retail Data Analysis Project\data\sample_data\orders.csv"
order_items_csv_path = r"C:\Users\vamsh\OneDrive\Desktop\Project SQL\Retail Data Analysis Project\data\sample_data\order_items.csv"

# Write to CSV files
with open(orders_csv_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['order_id', 'customer_id', 'order_date', 'total_amount', 'order_status',
                         'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code'])
    csv_writer.writerows(orders_data)
print(f"Generated {NUM_ORDERS} records and saved to {orders_csv_path}")

with open(order_items_csv_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['order_item_id', 'order_id', 'product_id', 'quantity', 'price_per_unit'])
    csv_writer.writerows(order_items_data)
print(f"Generated {NUM_ORDER_ITEMS} records and saved to {order_items_csv_path}")
