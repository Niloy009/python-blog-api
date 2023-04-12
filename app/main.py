import time
from fastapi import  FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
 
app = FastAPI()


class Post(BaseModel):
    title: str
    content:str
    published: bool= True
    
# DB Connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi-db', user='postgres', 
                                password='niloy0009', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("Database connected successfully!!!")
        break
    except Exception as error:
        print('Database Connection failed!!')
        print(f"Error is {error}")
        time.sleep(2)
    
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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get('/posts/{id}')
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE post_id = %s""", (str(id)))
    if post := cursor.fetchone():
        return {"data": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found")


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{'data':new_post}

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} is not exist")
    return {"data": updated_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} is not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    