from pathlib import Path
from psycopg2 import pool
import configparser, logging

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "properties" / ".env"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# logs config
logger = logging.getLogger(__name__)
if not logger.handlers:  # it's like a singleton, just for not creating unnecessary handlers
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [%(lineno)d] [%(levelname)s] %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

try:
    logger.info("Connecting to database")
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=config.get("Database", "DB_HOST"),
        user=config.get("Database", "DB_USER"),
        password=config.get("Database", "DB_PASSWORD"),
        database=config.get("Database", "DB_NAME"),
        port=config.get("Database", "DB_PORT"),
        options='-c search_path=public'
    )
    logger.info("Database connection established")

except:
    logger.exception("Database connection failed")
    connection_pool = None

run_check = [
    f"auth={config.get('Auth', 'enabled')}",
    f"users={config.get('Users', 'enabled')}",
    f"otp={config.get('Otp', 'enabled')}"
]
