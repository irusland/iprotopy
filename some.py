from pydantic import BaseModel

class PersonModel(BaseModel):
    name: str
    age: int

class PersonResponseModel(BaseModel):
    message: str
