from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///./my_database.db")

meta = MetaData()

conn = engine.connect()