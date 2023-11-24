from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.types import String  # Import String type for todo_task column
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(nullable=False)
    todo_task: Mapped[List["TodoTask"]] = relationship(back_populates='user')

    # def __init__(self, id, first_name, last_name):
    #     self.id = id
    #     self.first_name = first_name
    #     self.last_name = last_name

    def __repr__(self):
        return f"Person({self.id}, {self.first_name} {self.last_name})"

class TodoTask(Base):
    __tablename__ = "todo_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task: Mapped[str] = mapped_column(String(100))  # Added String type here
    done: Mapped[bool]
    user: Mapped["User"] = relationship(back_populates='todo_task')
    
    
    def __repr__(self):
        return f"Person({self.user_id}, {self.task} {self.done})"


engine = create_engine("sqlite:///todo_app.db", echo=True)

Base.metadata.create_all(bind=engine)
