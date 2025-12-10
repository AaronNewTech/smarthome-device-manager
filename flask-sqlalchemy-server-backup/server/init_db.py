#!/usr/bin/env python3
"""
Database initialization script for Smart Home Device Manager
"""

from app import create_app, init_sample_data
from models import db

def init_database():
    """Initialize the database and add sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created!")
        
        print("Adding sample data...")
        init_sample_data()
        print("Sample data added!")
        
        print("Database initialization complete!")

if __name__ == '__main__':
    init_database()