from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix= '/users',
    tags=['User']
)

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Hash user password
    hashed_password = utils.hashed_password(user.password)
    user.password = hashed_password 
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ResponseUser)
def get_post(id:int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.post_id == id)
    if user := db.query(models.User).filter(models.User.user_id == id).first():
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"User with id {id} is not found")
