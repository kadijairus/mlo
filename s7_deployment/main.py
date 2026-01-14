import re
from fastapi import FastAPI
from http import HTTPStatus
from enum import Enum
from fastapi import UploadFile, File
from typing import Optional
from fastapi.responses import FileResponse
import cv2

class ItemEnum(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()
@app.get("/")
def root():
    """ Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/restric_items/{item_id}")
def read_item(item_id: ItemEnum):
    return {"item_id": item_id}

# Query parameters
# Example: /query_items?item_id=5
@app.get("/query_items")
def read_item(item_id: int):
    return {"item_id": item_id}

database = {'username': [ ], 'password': [ ]}

# /login?username=yourname&password=yourpass
@app.post("/login")
def login(username: str, password: str):
    print("Someone is trying to login with", username, password)
    username_db = database['username']
    password_db = database['password']
    if username not in username_db and password not in password_db:
        with open('database.csv', "a") as file:
            file.write(f"{username}, {password} \n")
        username_db.append(username)
        password_db.append(password)
    return "login saved"

# Text processing endpoint
# http://localhost:8000/text_model/?data=kj.ee
@app.get("/text_model/")
def contains_email(data: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    response = {
        "input": data,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "is_email": re.fullmatch(regex, data) is not None
    }
    return response

# Computer Vision endpoint
#  curl -X POST "http://localhost:8000/cv_model/" -F "data=@exercise_files/my_cat.jpg"
@app.post("/cv_model/")
async def cv_model(data: UploadFile = File(...), h: None | int = 28, w: None | int = 28):
    with open('image.jpg', 'wb') as image:
        content = await data.read()
        image.write(content)
        image.close()

    img = cv2.imread('image.jpg')
    res = cv2.resize(img, (h, w))
    cv2.imwrite("image_resize.jpg", res)

    response = {
        "input": data,
        "output": "image_resize.jpg",
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response