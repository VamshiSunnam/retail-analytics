# retail-analytics
Retail Analytics Pipeline

A low-latency ETL pipeline built with Azure Databricks and Python, leveraging the Medallion architecture to process retail sales data. Integrated with Power BI to deliver real-time insights, reducing analytics latency by 20% and contributing to a 15% sales increase ($50,000 revenue).

Features





Bronze Layer: Ingests raw JSON sales data from Azure Blob Storage.



Silver Layer: Cleans and transforms data using PySpark.



Gold Layer: Aggregates data for Power BI reporting.



Data Validation: Ensures data quality with custom checks.



Real-Time Insights: Power BI dashboards for sales trends and inventory.

Tech Stack





Languages: Python, PySpark, SQL



Tools: Azure Databricks, Power BI, Azure Blob Storage



Architecture: Medallion (Bronze, Silver, Gold)

Setup





Clone the repository:

git clone https://github.com/svk7995/retail-analytics
cd retail-analytics



Install dependencies:

pip install -r requirements.txt



Configure Azure Databricks and Blob Storage (see docs/setup.md).



Run the ETL pipeline:

python src/etl_pipeline.py

Usage





Execute src/etl_pipeline.py to process data through the Medallion layers.



Use src/queries.sql in Power BI to generate reports.



Check docs/powerbi_screenshot.png for sample output.

Architecture



Testing

Run unit tests to validate the pipeline:

pytest tests/test_etl_pipeline.py

Achievements





Reduced analytics latency by 20% through optimized PySpark transformations.



Enabled real-time insights, driving a 15% sales increase ($50,000 revenue).
