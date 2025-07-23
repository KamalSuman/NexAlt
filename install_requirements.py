#!/usr/bin/env python
"""
Script to install required packages for the hackathon project.
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt."""
    try:
        # Get the absolute path to requirements.txt
        requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
        
        # Check if requirements.txt exists
        if not os.path.exists(requirements_path):
            print(f"Error: requirements.txt not found at {requirements_path}")
            return False
        
        # Install requirements
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        
        print("\nAll packages installed successfully!")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    install_requirements()