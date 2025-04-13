from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging
from urllib.parse import urlparse, parse_qs
import ssl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
parsed_url = urlparse(db_url)
query_params = parse_qs(parsed_url.query)

base_url = db_url.split('?')[0]
SQLALCHEMY_DATABASE_URL = base_url.replace("postgresql://", "postgresql+asyncpg://")
logger.info(f"Base database URL: {SQLALCHEMY_DATABASE_URL}")

connect_args = {}
if 'sslmode' in query_params and query_params['sslmode'][0] == 'require':
    logger.info("Setting up SSL for database connection with certificate validation disabled")
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connect_args['ssl'] = ssl_context

try:
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args
    )
    
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    Base = declarative_base()
    
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Error initializing database connection: {e}")
    raise 

def import_models():
    from app.models.user import User
    from app.models.location import Location