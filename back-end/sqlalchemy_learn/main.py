from models import engine
from sqlalchemy.orm import Session, sessionmaker

Session = sessionmaker(engine)