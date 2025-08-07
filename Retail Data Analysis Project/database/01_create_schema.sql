-- Create database and schema
DROP DATABASE IF EXISTS retail_analytics;
CREATE DATABASE retail_analytics;
USE retail_analytics;

-- Set configuration for optimal performance
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 2147483648; -- 2GB
SET GLOBAL innodb_log_file_size = 536870912; -- 512MB