from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2

db_string = "postgres://postgres:admin@localhost:5432/ISSP"

db = create_engine(db_string)
base = declarative_base()


class Firma(base):
    _tablename_ = 'firma'

    firma_id = Column(Integer, primary_key=True)
    nume = Column(String)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# Create
spitalu_dorle = Firma(firma_id=2, nume="cel_amiidwfe")
session.add(spitalu_dorle)
session.commit()