"""Service configuration"""
import os

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///accounts.db")
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
