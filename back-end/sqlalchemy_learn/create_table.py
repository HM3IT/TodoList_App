from models import *
# from sqlalchemy import create_engine

engine = create_engine("sqlite:///todo_app.db", echo = True)

# with engine.connect() as connection:
Base.metadata.create_all(bind = engine) 
    