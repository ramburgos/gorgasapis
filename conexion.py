from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

#url = URL.create(
#    drivername="mysql", 
#    username="masternet", 
#    password="G0r94s_Nm4db", 
#    host="172.31.1.112", 
#    database="db_gorgas_crm", 
#    port=3036
#    )

url = URL.create(
    drivername="mysql", 
    username="root", 
    password="87351910", 
    host="localhost", 
    database="db_gorgas_crm", 
    port=3306
    )

engine = create_engine(url)
Sessionlocal = sessionmaker(bind=engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()    

