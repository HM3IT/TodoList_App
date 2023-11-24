from sqlalchemy import select
from models import User, TodoTask
from main import Session


#simple_select
with Session() as session:
#     select_stmt = select(User).where(User.first_name.in_(["Hein Min"]))
#     results = session.scalars(select_stmt)

#     for user in results:
#         print(user)


#condition select
    # results = session.query(User).filter_by(last_name="Min Maw").first()
    # print(results)
    
    select_stmt = select(TodoTask).join(TodoTask.user).where(User.first_name =="Hein Min")
    results = session.scalars(select_stmt)
    for result in results:
        print(result)