from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER=os.getenv("MYSQL_USER",)
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
MYSQL_DB=os.getenv("MYSQL_DB")
MYSQL_HOST=os.getenv("MYSQL_HOST","sigorgas-databasesigorgas-3n89yi")
MYSQL_PORT=int(os.getenv("MYSQL_PORT",3306))

DATABASE_URL= f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()    

