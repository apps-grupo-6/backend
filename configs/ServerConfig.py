from pathlib import Path
from psycopg2 import pool
import configparser, logging, sib_api_v3_sdk

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

try:
    logger.info("Connecting to email api")

    # Configurar la API key
    API_KEY = config.get("Email", "api_key")
    SENDER_NAME = config.get("Email", "sender_name")
    SENDER_EMAIL = config.get("Email", "sender_email")
    email_configuration = sib_api_v3_sdk.Configuration()
    email_configuration.api_key['api-key'] = API_KEY
except:
    logger.exception("Email api connection failed")

run_check = [
    f"auth={config.get('Auth', 'enabled')}",
    f"users={config.get('Users', 'enabled')}",
    f"otp={config.get('Otp', 'enabled')}"
]
