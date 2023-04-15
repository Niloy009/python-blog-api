from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password:str) -> str:
    """Hashed the Password

    Args:
        password (str): Password from the user

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify(plain_password:str, password:str) -> bool:
    """Verify the password

    Args:
        plain_password (str): password from user
        password (str): password from db

    Returns:
        bool: True or False
    """
    return pwd_context.verify(secret=plain_password, hash=password)