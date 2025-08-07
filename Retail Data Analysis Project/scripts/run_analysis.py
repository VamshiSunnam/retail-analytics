import pandas as pd
import json
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
from jinja2 import Environment, FileSystemLoader
import io
import base64
import seaborn as sns

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
        raise ValueError("PostgreSQL not yet implemented for this script.")
    else:
        raise ValueError(f"Unsupported database driver: {driver}")

def load_sql_query(query_file_path):
    with open(query_file_path, 'r') as f:
        return f.read()

def run_query_and_get_dataframe(engine, query):
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

def dataframe_to_html_table(df):
    return df.to_html(index=False, classes='table table-striped')

def plot_to_base64(plt_obj):
    img_buffer = io.BytesIO()
    plt_obj.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt_obj.close()
    return img_base64

def visualize_top_products(df):
    plt.figure(figsize=(12, 6))
    plt.bar(df['product_name'], df['total_quantity_sold'], color='skyblue')
    plt.xlabel('Product Name')
    plt.ylabel('Total Quantity Sold')
    plt.title('Top 10 Selling Products by Quantity')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return plot_to_base64(plt)

def visualize_monthly_sales_trends(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['sales_month'], df['monthly_sales_amount'], marker='o', linestyle='-', color='green')
    plt.xlabel('Month')
    plt.ylabel('Monthly Sales Amount')
    plt.title('Monthly Sales Trends')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    return plot_to_base64(plt)

def visualize_customer_ltv(df):
    plt.figure(figsize=(12, 6))
    plt.bar(df['customer_id'].astype(str), df['customer_lifetime_value'], color='lightcoral')
    plt.xlabel('Customer ID')
    plt.ylabel('Customer Lifetime Value')
    plt.title('Customer Lifetime Value (Top Customers)')
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()
    return plot_to_base64(plt)

def visualize_rfm_segments(df):
    # Assign RFM scores (example: using quantiles)
    df['R_Score'] = pd.qcut(df['Recency'], 5, labels=[5, 4, 3, 2, 1]) # Lower recency is better (higher score)
    df['F_Score'] = pd.qcut(df['Frequency'], 5, labels=[1, 2, 3, 4, 5])
    df['M_Score'] = pd.qcut(df['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    df['RFM_Score'] = df['R_Score'].astype(str) + df['F_Score'].astype(str) + df['M_Score'].astype(str)

    # Simple segmentation based on RFM scores
    # You can define more complex segmentation logic here
    def rfm_segment(row):
        if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
            return 'Champions'
        elif row['R_Score'] >= 4 and row['F_Score'] >= 3:
            return 'Loyal Customers'
        elif row['R_Score'] >= 3 and row['M_Score'] >= 3:
            return 'Potential Loyalists'
        elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
            return 'At Risk'
        else:
            return 'Others'

    df['Segment'] = df.apply(rfm_segment, axis=1)

    # Visualize segment distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Segment', palette='viridis')
    plt.title('RFM Customer Segments Distribution')
    plt.xlabel('Customer Segment')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return plot_to_base64(plt), df # Return df with segments for table

if __name__ == "__main__":
    try:
        db_connection_str = get_db_connection_string('development')
        engine = create_engine(db_connection_str)

        # Define query file paths
        queries_path = os.path.join(os.path.dirname(__file__), '..', 'queries')
        top_products_query_path = os.path.join(queries_path, 'product_analysis', 'top_products.sql')
        monthly_sales_query_path = os.path.join(queries_path, 'sales_analysis', 'sales_trends.sql')
        customer_ltv_query_path = os.path.join(queries_path, 'customer_analysis', 'customer_ltv.sql')
        rfm_analysis_query_path = os.path.join(queries_path, 'customer_analysis', 'rfm_analysis.sql')

        # --- Top Selling Products ---
        top_products_query = load_sql_query(top_products_query_path)
        top_products_df = run_query_and_get_dataframe(engine, top_products_query)
        top_products_chart_base64 = ""
        top_products_table_html = ""
        if not top_products_df.empty:
            top_products_chart_base64 = visualize_top_products(top_products_df)
            top_products_table_html = dataframe_to_html_table(top_products_df)
        else:
            print("No data for Top Selling Products.")

        # --- Monthly Sales Trends ---
        monthly_sales_query = load_sql_query(monthly_sales_query_path)
        monthly_sales_df = run_query_and_get_dataframe(engine, monthly_sales_query)
        monthly_sales_chart_base64 = ""
        monthly_sales_table_html = ""
        if not monthly_sales_df.empty:
            monthly_sales_chart_base64 = visualize_monthly_sales_trends(monthly_sales_df)
            monthly_sales_table_html = dataframe_to_html_table(monthly_sales_df)
        else:
            print("No data for Monthly Sales Trends.")

        # --- Customer LTV ---
        customer_ltv_query = load_sql_query(customer_ltv_query_path)
        customer_ltv_df = run_query_and_get_dataframe(engine, customer_ltv_query)
        customer_ltv_chart_base64 = ""
        customer_ltv_table_html = ""
        if not customer_ltv_df.empty:
            # For LTV, let's visualize top 20 customers for better readability
            customer_ltv_chart_base64 = visualize_customer_ltv(customer_ltv_df.head(20))
            customer_ltv_table_html = dataframe_to_html_table(customer_ltv_df.head(20))
        else:
            print("No data for Customer LTV.")

        # --- RFM Analysis ---
        rfm_analysis_query = load_sql_query(rfm_analysis_query_path)
        rfm_df = run_query_and_get_dataframe(engine, rfm_analysis_query)
        rfm_chart_base64 = ""
        rfm_table_html = ""
        if not rfm_df.empty:
            rfm_chart_base64, rfm_df_segmented = visualize_rfm_segments(rfm_df.copy())
            rfm_table_html = dataframe_to_html_table(rfm_df_segmented.head(20)) # Show top 20 for table
        else:
            print("No data for RFM Analysis.")

        # --- Generate HTML Report ---
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'templates')
        file_loader = FileSystemLoader(template_dir)
        env = Environment(loader=file_loader)
        template = env.get_template('dashboard.html')

        output_html = template.render(
            title="Retail Data Analysis Report",
            monthly_sales_chart=monthly_sales_chart_base64,
            monthly_sales_table=monthly_sales_table_html,
            top_products_chart=top_products_chart_base64,
            top_products_table=top_products_table_html,
            customer_ltv_chart=customer_ltv_chart_base64,
            customer_ltv_table=customer_ltv_table_html,
            rfm_chart=rfm_chart_base64,
            rfm_table=rfm_table_html
        )

        report_output_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'dashboard.html')
        with open(report_output_path, 'w') as f:
            f.write(output_html)
        print(f"HTML report generated at {report_output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
