from typing import Optional, Annotated
from dataclasses import dataclass
from collections.abc import AsyncGenerator
from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler

from litestar import Litestar, get, post, put, delete
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from litestar.exceptions import ClientException, NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT
from litestar.dto import DataclassDTO, DTOConfig, DTOData, dto_field

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.config.cors import CORSConfig
from sqlalchemy import select, delete as delete_row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

cors_config = CORSConfig(allow_origins=["http://localhost:5173","http://localahost:5173/"])
					

class Base(DeclarativeBase):
    pass

class TodoItem(Base):

    __tablename__ = "todo_items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] 
    done: Mapped[bool]

TodoDTO = SQLAlchemyDTO[TodoItem]
    
writeConfig = DTOConfig( exclude={"id"})

# ReadTodoDTO = SQLAlchemyDTO[Annotated[TodoItem, readConfig]]
WriteTodoDTO = SQLAlchemyDTO[Annotated[TodoItem, writeConfig]]


@get("/todos/get/")
async def get_todos(transaction: AsyncSession, done: Optional[bool] = None) -> list[TodoItem]:
    return await get_todo_list(done, transaction)


@post("/todos/add/", dto = WriteTodoDTO)
async def add_todo(data: TodoItem, transaction: AsyncSession) -> TodoItem:
    transaction.add(data)
    await transaction.flush()
    return data
 
@put("/todos/update/{todo_id:int}", dto = WriteTodoDTO )
async def update_todo(todo_id: int, data:TodoItem, transaction: AsyncSession) -> TodoItem:
    todo = await get_todo_by_id(todo_id, transaction)
    todo.title = data.title
    todo.done = data.done

    return todo

@delete("/todos/delete/{todo_id:int}")
async def remove_todo(todo_id: int, transaction: AsyncSession) -> None:
    stmt = delete_row(TodoItem).where(TodoItem.id == todo_id)
    await transaction.execute(stmt)
  
   
async def get_todo_list(done: Optional[bool], session: AsyncSession) -> list[TodoItem]:
    query = select(TodoItem)
    
    if done is not None:
        query = query.where(TodoItem.done.is_(done))

    result = await session.execute(query)
    return result.scalars().all()


async def get_todo_by_id(todo_id, session: AsyncSession) -> TodoItem:

    query = select(TodoItem).where(TodoItem.id == todo_id)
    result = await session.execute(query)

    try:
        return result.scalar_one()

    except NoResultFound as e:
        raise NotFoundException(detail=f"TODO {todo_name!r} not found") from e
    
    
async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:

    try:
        async with db_session.begin():
            yield db_session

    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


db_config = SQLAlchemyAsyncConfig(

    connection_string="sqlite+aiosqlite:///todoList.sqlite",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,

)

fullapp = Litestar(
    route_handlers=[get_todos, add_todo, update_todo, remove_todo],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    cors_config=cors_config
)
