import os

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "juan1104")
DB_HOST = os.getenv("DB_HOST", "mydb1.crum4qey00uo.us-east-1.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "mydb1")
DB_PORT = os.getenv("DB_PORT", "3306")  # Default MySQL port

#DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#DATABASE_URL = "mysql+pymysql://admin:juan1104@mydb1.crum4qey00uo.us-east-1.rds.amazonaws.com/mydb"
