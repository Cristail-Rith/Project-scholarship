import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads",
        "products",
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
        mysql_host = os.getenv("MYSQL_HOST", "localhost")
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        mysql_database = os.getenv("MYSQL_DATABASE", "restaurant_db")
        database_url = (
            f"mysql+pymysql://{mysql_user}:{mysql_password}"
            f"@{mysql_host}:{mysql_port}/{mysql_database}"
        )
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
