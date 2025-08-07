import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import json

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

class RetailDataGenerator:
    def __init__(self, config_path='config/generation_config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2024, 11, 30)
    
    def generate_customers(self, n=1000):
        """Generate customer data"""
        customers = []
        segments = ['New', 'Regular', 'Premium', 'VIP']
        segment_weights = [0.4, 0.35, 0.2, 0.05]
        
        for i in range(1, n + 1):
            reg_date = fake.date_between(start_date=self.start_date, end_date=self.end_date)
            customers.append({
                'customer_id': i,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'country': 'USA',
                'registration_date': reg_date,
                'customer_segment': np.random.choice(segments, p=segment_weights),
                'is_active': random.choice([True, True, True, False])  # 75% active
            })
        
        return pd.DataFrame(customers)
    
    def generate_orders(self, customers_df, n=5000):
        """Generate order data"""
        orders = []
        customer_ids = customers_df['customer_id'].tolist()
        payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay']
        statuses = ['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Processing', 'Cancelled']
        
        for i in range(1, n + 1):
            customer_id = random.choice(customer_ids)
            customer_reg_date = customers_df[customers_df['customer_id'] == customer_id]['registration_date'].iloc[0]
            
            # Order date should be after customer registration
            order_date = fake.date_time_between(
                start_date=customer_reg_date,
                end_date=self.end_date
            )
            
            status = random.choice(statuses)
            
            # Calculate dates based on status
            if status in ['Delivered', 'Shipped']:
                shipping_date = order_date + timedelta(days=random.randint(1, 3))
                delivery_date = shipping_date + timedelta(days=random.randint(2, 7)) if status == 'Delivered' else None
            else:
                shipping_date = None
                delivery_date = None
            
            subtotal = round(random.uniform(20, 2000), 2)
            shipping_cost = round(random.uniform(0, 25), 2) if subtotal < 100 else 0
            discount = round(subtotal * random.uniform(0, 0.3), 2) if random.random() > 0.7 else 0
            
            orders.append({
                'order_id': i,
                'customer_id': customer_id,
                'order_date': order_date,
                'shipping_date': shipping_date,
                'delivery_date': delivery_date,
                'order_status': status,
                'payment_method': random.choice(payment_methods),
                'shipping_cost': shipping_cost,
                'discount_amount': discount,
                'total_amount': round(subtotal - discount + shipping_cost, 2)
            })
        
        return pd.DataFrame(orders)
    
    def generate_order_items(self, orders_df, products_df):
        """Generate order items data"""
        order_items = []
        item_id = 1
        
        for _, order in orders_df.iterrows():
            # Each order has 1-5 items
            num_items = random.randint(1, 5)
            selected_products = products_df.sample(n=num_items)
            
            for _, product in selected_products.iterrows():
                quantity = random.randint(1, 3)
                unit_price = product['unit_price']
                discount_percent = random.uniform(0, 20) if random.random() > 0.8 else 0
                line_total = round(quantity * unit_price * (1 - discount_percent/100), 2)
                
                order_items.append({
                    'order_item_id': item_id,
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'discount_percent': round(discount_percent, 2),
                    'line_total': line_total
                })
                item_id += 1
        
        return pd.DataFrame(order_items)
    
    def save_all_data(self, output_dir='data/generated/'):
        """Generate and save all datasets"""
        os.makedirs(output_dir, exist_ok=True)
        print("Generating customer data...")
        customers = self.generate_customers(1000)
        customers.to_csv(f'{output_dir}customers.csv', index=False)
        
        print("Generating order data...")
        orders = self.generate_orders(customers, 5000)
        orders.to_csv(f'{output_dir}orders.csv', index=False)
        
        print("Loading product data...")
        products = pd.read_csv('data/sample_data/products.csv')
        
        print("Generating order items data...")
        order_items = self.generate_order_items(orders, products)
        order_items.to_csv(f'{output_dir}order_items.csv', index=False)
        
        print("Data generation complete!")
        return {
            'customers': len(customers),
            'orders': len(orders),
            'order_items': len(order_items)
        }

if __name__ == "__main__":
    generator = RetailDataGenerator()
    stats = generator.save_all_data()
    print(f"Generated: {stats}")