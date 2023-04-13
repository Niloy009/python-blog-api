import time
from fastapi import  Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

 
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()

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


@app.get('/')
def root():
    return{'message': "Hello Fast-Api"}


# @app.get('/db')
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{'data': posts}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get('/posts/{id}')
def get_post(id:int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.post_id == id)
    if post := db.query(models.Post).filter(models.Post.post_id == id).first():
        return {"data": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found")


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{'data':new_post}

@app.put('/posts/{id}')
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.post_id == id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id {id} is not exist")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return {"data": updated_post.first()}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.post_id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id {id} is not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    