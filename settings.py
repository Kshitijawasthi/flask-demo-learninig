import os
from dotenv import load_dotenv

load_dotenv()
class Config:  
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG =False