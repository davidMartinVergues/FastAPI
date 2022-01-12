from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True # by default it will b True
    rating: Optional[int] = None



# path operation - 1
@app.get("/", tags=["ROOT"])
async def root():
    return {"message":"welcome to my API"}

# path operation - 2
@app.get("/posts", tags=["POSTS"])
async def get_posts():
    return {"data":"this is your post"}

# path operation - 3 POST request
@app.post("/createposts", tags=["POSTS"])
async def create_posts(post:Post):
    return {"new_post":f'titel: {post.title} content: {post.content}'}
