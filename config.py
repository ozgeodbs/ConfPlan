import os

class Config:
    # Absolute path to the SQLite database
    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:/sqlite/conference.db'  # Escape the backslashes in the path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
