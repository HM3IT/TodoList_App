from dataclasses import dataclass

from litestar import Litestar, get, put, post, patch, Controller
from litestar.dto import DataclassDTO, DTOConfig, DTOData

@dataclass
class Character:
    name:str
    skill:str


@dataclass
class User:
    id:int
    name:str
    email:str
    characters:list[Character]
    

class ReadDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"email"})
    
    
class WriteDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"id"})
    
class PatchDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"id"}, partial=True) #This setting allows for partial updates of the resource.


class userController(Controller):
    dto=WriteDTO,
    return_dto=ReadDTO
    
    @get("users/get/{name:str}", sync_to_thread=False)
    def getData(self, name:str) -> User:
    
        cha1 = Character(name = "Diluc", skill = "Big Sword")
        cha2 = Character(name="Neuvillet", skill = "Hyper Beam")
        return  User(name = name, email = f"{name}@gmail.comm", characters  = [cha1, cha2])

    @post("users/add", dto=WriteDTO, sync_to_thread=False)
    def setData(self,data:DTOData[User])-> User:
        id = data.create_instance(id = 1)
        cha1 = Character(name = "Diluc", skill = "Big Sword")
        cha2 = Character(name="Neuvillet", skill = "Hyper Beam")
        return  User(name = name, email = f"{name}@gmail.comm", characters  = [cha1, cha2])

    @patch("user/patch/{user_id:int}", dto=PatchDTO, sync_to_thread=False)    
    def updateUserID(self,user_id:int, data:DTOData[User])-> User:
        cha1 = Character(name = "Diluc", skill = "Big Sword")
        cha2 = Character(name="Neuvillet", skill = "Hyper Beam")
        updated_user =  User(id = user_id, name = name, email = f"{name}@gmail.comm", characters  = [cha1, cha2])
        return data.update_instance(updated_user)


app = Litestar(route_handlers=[userController])
    