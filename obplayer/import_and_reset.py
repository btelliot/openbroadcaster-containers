#!/usr/bin/python3
import os
import sys
import sqlite3

# Initialize the application context
import obplayer
from obplayer.data import ObConfigData
from obplayer.log import ObLog

# Set up logging and configuration
obplayer.Log = ObLog()
obplayer.Config = ObConfigData()

# Get the data directory
data_dir = obplayer.ObData.get_datadir()

# Paths to database files
settings_db_path = os.path.join(data_dir, 'settings.db')

# Function to reset database
def reset_database(db_path):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Drop all existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        
        # Recreate settings table
        cursor.execute("""
            CREATE TABLE settings (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                value TEXT, 
                type TEXT
            )
        """)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        print(f"Database {db_path} reset successfully")
    except Exception as e:
        print(f"Error resetting database {db_path}: {e}")

# Reset the settings database
reset_database(settings_db_path)

# Read settings from file
settings = {}
with open('/app/obsettings.txt', 'r') as f:
    for line in f:
        name, value = line.strip().split(':', 1)
        settings[name] = value

# Save the settings
obplayer.Config.save_settings(settings)

print("Settings imported successfully")