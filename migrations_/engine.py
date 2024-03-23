import sqlalchemy as sa
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()
db_url = sa.engine.URL.create(
    drivername=os.getenv('DB_DRIVERNAME', 'postgresql+psycopg2'),
    username=os.getenv('DB_USER', 'postgres'),
    password=quote_plus(os.getenv('DB_PASS', 'postgres')),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', 5657),
    database=os.getenv('DB_NAME', 'postgres')
)
