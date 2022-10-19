from fastapi import Depends , status , HTTPException , APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models , utils
from .. database import get_db
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserBase,db:Session=Depends(get_db)):

    
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} not found.")
    return user

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.UserOut])
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
