from datetime import datetime, timedelta, timezone
from fastapi import  Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'c2d2038673429b481c138975aa7820adcb2754d38b2c5cf23e56a3b31a4d3617'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data:dict) -> str:
    """Create JWT token for authentication

    Args:
        data (dict): data to show on jwt

    Returns:
        str: jwt token
    """
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire_time

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token:str, credential_exception):
    # sourcery skip: raise-from-previous-error
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credential_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credential_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not vallidate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token=token, credential_exception=credential_exception)
    return (
        db.query(models.User)
        .filter(models.User.user_id == token.user_id)
        .first()
    )
