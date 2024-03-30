from dotenv import load_dotenv
import os
load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
REDIS_URL = os.getenv('REDIS_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
 