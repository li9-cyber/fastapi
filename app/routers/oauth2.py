from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .. import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from ..config import settings

###
# 假設 request header 是：
# Authorization: Bearer eyJhbGciOiJIUzI1Ni...
# 搭配下面寫法：
# def get_current_user(
#     token: str = Depends(oauth2_scheme),
# ):
#     return token
# FastAPI 會自動：
# 檢查 request 有沒有 Authorization header。
# 檢查格式是不是 Bearer <token>。
# 取出 Bearer 後面的 token。
# 將 token 字串傳給 get_current_user()。
#tokenUrl="login" 的作用是告訴 Swagger UI：
# 要取得 token，應該向 /login endpoint 發送登入 request。

# 它主要用於產生 OpenAPI 文件和 Swagger 的 Authorize 功能，不代表 oauth2_scheme 每次都會自動呼叫 /login
###



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SCRET_KEY
#Algorithm
#Experiation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # the payload variable already verfy the token, if the verfication failed, the payload will throw a JWTError
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        #token_data contains a object, using property to access
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user