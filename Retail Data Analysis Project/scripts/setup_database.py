import os
import json
import mysql.connector
from mysql.connector import Error
import psycopg2
from pathlib import Path
import sys

class DatabaseSetup:
    def __init__(self, env='development'):
        self.env = env
        self.config = self.load_config()
        self.connection = None
        self.cursor = None
    
    def load_config(self):
        """Load database configuration"""
        config_path = Path('config/database_config.json')
        with open(config_path, 'r') as f:
            configs = json.load(f)
        return configs[self.env]
    
    def connect(self):
        """Establish database connection"""
        try:
            if self.config['driver'] == 'mysql':
                self.connection = mysql.connector.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    user=self.config['user'],
                    password=self.config['password']
                )
            elif self.config['driver'] == 'postgresql':
                self.connection = psycopg2.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    user=self.config['user'],
                    password=self.config['password']
                )
            
            self.cursor = self.connection.cursor()
            print(f"Connected to {self.config['driver']} database")
            return True
            
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def execute_sql_file(self, filepath):
        """Execute SQL commands from file"""
        with open(filepath, 'r') as f:
            sql_commands = f.read()
        
        # Split by semicolon and execute each command
        commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
        
        for command in commands:
            try:
                self.cursor.execute(command)
                self.connection.commit()
                print(f"Executed: {command[:50]}...")
            except Error as e:
                print(f"Error executing command: {e}")
                self.connection.rollback()
    
    def setup_database(self):
        """Run all setup scripts"""
        if not self.connect():
            return False
        
        # Get all SQL files in order
        sql_files = sorted(Path('database').glob('*.sql'))
        
        for sql_file in sql_files:
            print(f"\nExecuting {sql_file.name}...")
            self.execute_sql_file(sql_file)
        
        print("\nDatabase setup complete!")
        return True
    
    def verify_setup(self):
        """Verify database setup"""
        try:
            # Check if database exists
            self.cursor.execute(f"USE {self.config['database']}")
            
            # Check tables
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            
            print("\nDatabase verification:")
            print(f"Tables created: {len(tables)}")
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = self.cursor.fetchone()[0]
                print(f"  - {table[0]}: {count} records")
            
            return True
            
        except Error as e:
            print(f"Verification failed: {e}")
            return False
    
    def cleanup(self):
        """Close database connections"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connections closed")

def main():
    # Parse command line arguments
    env = sys.argv[1] if len(sys.argv) > 1 else 'development'
    
    # Setup database
    setup = DatabaseSetup(env)
    
    try:
        if setup.setup_database():
            setup.verify_setup()
    finally:
        setup.cleanup()

if __name__ == "__main__":
    main()