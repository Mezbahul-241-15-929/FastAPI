from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgressql://postgres:Meraz@localhost:5432/Mezbahul"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)