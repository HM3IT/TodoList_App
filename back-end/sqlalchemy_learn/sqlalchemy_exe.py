from sqlalchemy import create_engine,text

engine = create_engine("sqlite:///test.db", echo = True)

with engine.connect() as connection:
    result = connection.execute(text("Select 'Hello world'"))
    print(result.all())