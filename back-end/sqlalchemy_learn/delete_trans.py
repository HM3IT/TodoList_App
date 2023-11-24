from main import Session
from models import User, TodoTask

with Session() as session:
    task = session.query(TodoTask).filter_by(task = "Do exercise").first()
    session.delete(task)
    session.commit()