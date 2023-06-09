import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return{'message': "Hello Fast-Api"}

