class Config:
    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:/sqlite/conference.db'  # Escape the backslashes in the path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_SECRET_TOKEN = "abcs"
    BASE_URL = "http://127.0.0.1:5000"
