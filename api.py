from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

user_data = {
    1: {
        "name": "igor",
        "age": 23,
        "country": "Brazil",
    }
}

class User(BaseModel):
    name: str
    age: int
    country: str

class UpdateUser(BaseModel):
    name: Optional[str]
    age: Optional[int]
    country: Optional[str]

@app.get("/")
def index():
    data = {"mock": "data", "name": "igor"}
    return data


# path parameters


@app.get("/get_user/{user_id}")
def get_user(user_id: int = Path(description="The user id intended", gt=0)): # fastapi type checks
    return user_data[user_id]

# /? query=parameters


@app.get("/get_user_by_name/{user_id}")
def get_user_by_name(user_id, user_name: Optional[str] = None):
    """
    call:  /get_user_by_name?user_name=igor
    """
    print(user_id) # just to use it
    for user in user_data:
        if user_data[user]["name"] == user_name:
            return user_data[user]

    return {"Data": "Not Found"}

# request body and post 

@app.post("/create_user/{user_id}")
def create_user(user_id: int, user: User):
    # checks if user already exists
    if user_id in user_data:
        return {"Error": "User exists"}
    
    # create the actually user
    user_data[user_id] = user
    return user_data[user_id]

# put

@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in user_data:
        return {"Error": "User does not exists"}
    
    if user.name != None:
        user_data[user_id].name = user.name

    if user.age != None:
        user_data[user_id].age = user.age

    if user.country != None:
        user_data[user_id].country = user.country

    user_data[user_id] = user
    return user_data[user_id] 



# delete 

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    if user_id not in user_data:
        return {"Error": "User does not exists"}
    
    del user_data[user_id]
    return {"Message": "User Deleted successfully"}

