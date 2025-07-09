from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://dbuser25:dbslave_sigorgas@172.31.1.71:3030/db_gorgas_crm")
#DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://dbuser25:dbslave_sigorgas@sigorgas-databasesigorgas-3n89yi:3306/db_gorgas_crm")
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()    

