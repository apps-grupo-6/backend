from logging.handlers import RotatingFileHandler
from pathlib import Path
from psycopg2 import pool
import configparser, logging, sib_api_v3_sdk

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "properties" / ".env"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# logs config
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[94m",   # Azul
    "INFO": "\033[92m",    # Verde
    "WARNING": "\033[93m", # Amarillo
    "ERROR": "\033[91m",   # Rojo
    "CRITICAL": "\033[95m" # Magenta
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, RESET)
        message = super().format(record)
        return f"{color}{message}{RESET}"

logger = logging.getLogger(__name__)
if not logger.handlers:  # it's like a singleton, just for not creating unnecessary handlers
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_structure = "[%(asctime)s] [%(filename)s] [%(lineno)d] [%(levelname)s] %(message)s"
    formatter = ColorFormatter(log_structure)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)
    LOG_FILE = LOG_DIR / "app.log"

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=100 * 1024 * 1024,  # 100 MB
        backupCount=100,               # saves max 100 files
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(log_structure)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
try:
    logger.info("Connecting to database")
    connection_pool = pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        host=config.get("database", "DB_HOST"),
        user=config.get("database", "DB_USER"),
        password=config.get("database", "DB_PASSWORD"),
        database=config.get("database", "DB_NAME"),
        port=config.get("database", "DB_PORT"),
        options='-c search_path=public'
    )
    logger.info("Database connection established")

except:
    logger.exception("Database connection failed")
    connection_pool = None

try:
    logger.info("Connecting to email api")

    API_KEY = config.get("email", "api_key")
    SENDER_NAME = config.get("email", "sender_name")
    SENDER_EMAIL = config.get("email", "sender_email")
    email_configuration = sib_api_v3_sdk.Configuration()
    email_configuration.api_key['api-key'] = API_KEY
    logger.info("Email api connection established")
except:
    logger.exception("Email api connection failed")

LOCALHOST_ORIGINS_REGEX = r"^http://(localhost|127\.0\.0\.1)(:\d+)?$"

config_keys = config.keys()

enabled = [
    f"{section}={config.get(section, 'enabled')}"
    for section in config_keys
    if config.has_option(section, 'enabled')
]

# -1 = database error when trying to check if user exists in our database
# 9998 = user is banned
# 9999 = security breach
special_errors_code_map = ("-1", "9998", "9999")