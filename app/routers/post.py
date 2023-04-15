from typing import List
from fastapi import  Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2




router = APIRouter(
    prefix= '/posts',
    tags=['Posts']
)




@router.get('/', response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(database.get_db), 
              current_user:schemas.ResponseUser = Depends(oauth2.get_current_user)):
    return db.query(models.Post).all()


@router.get('/{id}', response_model=schemas.ResponsePost)
def get_post(id:int, db: Session = Depends(database.get_db), 
             current_user:schemas.ResponseUser = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.post_id == id)
    if post := db.query(models.Post).filter(models.Post.post_id == id).first():
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found")


@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), 
                current_user:schemas.ResponseUser = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/{id}', response_model=schemas.ResponsePost)
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(database.get_db),
                current_user:schemas.ResponseUser = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.post_id == id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id {id} is not exist")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return updated_post.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(database.get_db),
                current_user:schemas.ResponseUser = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.post_id == id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id {id} is not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)