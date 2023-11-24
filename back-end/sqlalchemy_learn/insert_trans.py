from models import User, TodoTask
from main import Session
from create_table import engine
 
user1 = User(
    first_name="Hein Min",
    last_name="Min Maw",
    todo_task = [
        TodoTask(task="Learn Litestar", done = False),
        TodoTask(task = "Learn SQLAlchemy", done = True)
    ]
)

user2 = User(
    first_name="John",
    last_name="Smith",
    todo_task = [
        TodoTask(task="Watch News", done = True),
        TodoTask(task = "Do exercise", done = False)
    ]
)
 
with Session() as session:
    session.add_all([user1, user2])
    session.commit()