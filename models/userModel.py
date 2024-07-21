from pydantic import BaseModel, constr

class User(BaseModel):
    fullName: constr(min_length=1, max_length=50)
    sucursal: constr(min_length=1, max_length=50)
    marca: constr(min_length=1, max_length=50)
