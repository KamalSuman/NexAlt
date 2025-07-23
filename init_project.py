#!/usr/bin/env python
"""
Script to initialize the project by creating necessary directories and files.
"""
import os
import shutil
import sys

def init_project():
    """Initialize the project by creating necessary directories and files."""
    try:
        # Create directories for Excel files if they don't exist
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
        
        # Create a sample Excel file if it doesn't exist
        scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
        excel_source = os.path.join(scripts_dir, "top20_indian_instruments.xlsx")
        excel_dest = os.path.join(data_dir, "top20_indian_instruments.xlsx")
        
        if os.path.exists(excel_source) and not os.path.exists(excel_dest):
            shutil.copy(excel_source, excel_dest)
            print(f"Copied sample Excel file to: {excel_dest}")
        
        print("\nProject initialized successfully!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run migrations: python manage.py migrate")
        print("3. Start the server: python manage.py runserver")
        
        return True
    
    except Exception as e:
        print(f"Error initializing project: {e}")
        return False

if __name__ == "__main__":
    init_project()