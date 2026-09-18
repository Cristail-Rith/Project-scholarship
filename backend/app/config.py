import os
from datetime import timedelta
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

# Resolve relative SQLite paths from this config file's location to avoid
# CWD/Unicode normalization issues (e.g. OneDrive paths with spaces)
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_instance_dir = os.path.join(_backend_dir, "instance")
os.makedirs(_instance_dir, exist_ok=True)


class Config:
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads",
        "products",
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("sqlite:///"):
        rel_path = database_url.replace("sqlite:///", "")
        if not os.path.isabs(rel_path):
            rel_path = os.path.join(_backend_dir, rel_path)
        database_url = "sqlite:///" + rel_path
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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
