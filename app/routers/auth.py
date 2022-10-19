from fastapi import APIRouter , status , Depends , HTTPException
from sqlalchemy.orm import Session

from app import schemas
from .. import models , utils , oauth2
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags = ["Login"]
)

@router.post("/login",response_model=schemas.Token)
def login(userCredentials : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
            

    if not utils.verify(userCredentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {
        "token" : access_token,
        "type" : "Bearer"
    
    }