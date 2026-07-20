from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session 
from ..database import get_db
from .. import schemas, models, utils
from . import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", response_model=schemas.Token)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #{"username": ".....", "password": "...."}
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the user with {userCredentials.email} is not exist")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #create a token
    #return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}




