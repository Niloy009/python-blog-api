from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
 
app = FastAPI()


class Post(BaseModel):
    title: str
    content:str
    published: bool= True
    rating: Optional[int] = None
    
my_posts = [{"title":"title 1", "content":"content 1", "id":1},{"title":"title 2","content":"content 2","id":2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for index, i in enumerate(my_posts):
        if i["id"] == id:
            return index


@app.get('/')
def root():
    return{'message': "Hello Fast-Api"}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def createpost(posts: Post):
    post_dict = posts.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{'data':my_posts}

@app.get('/posts/{id}')
def get_post(id:int):
    if post := find_post(id):
        return {"data":post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found")


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} is not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} is not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    