from main import Session
from models import User, TodoTask

with Session() as session:
    task = session.query(TodoTask).filter_by(id = 1).first()
    task.task = "Updated task"
    session.commit()