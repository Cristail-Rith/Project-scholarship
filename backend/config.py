import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ---- Database ----
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_HOST = 'localhost'
    DB_NAME = 'restaurant_db'
    DB_PORT = '3306'

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---- Uploads ----
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'menu')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    # Multipart uploads include file data plus form fields. Allow menu images up to 16 MiB.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024