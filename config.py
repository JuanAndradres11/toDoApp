import os

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "juan9811and")
DB_HOST = os.getenv("DB_HOST", "mydb.crum4qey00uo.us-east-1.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "mydb")

#DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_URL = "mysql+pymysql://admin:juan9811and@mydb.crum4qey00uo.us-east-1.rds.amazonaws.com/mydb"
