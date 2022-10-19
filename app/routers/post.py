from fastapi import Depends , status , HTTPException , APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models , oauth2
from .. database import get_db
from typing import List , Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)


@router.get("/",response_model=List[schemas.PostwVote])
# @router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    # print(result)
    return posts

@router.get("/{id}",response_model=schemas.PostwVote)
def get_post(id:int, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Go see your own Post.")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found.")
    return post

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Post)
def update_post(id:int , updated_post:schemas.CreatePost,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=("Go Update your own post."))

    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.CreatePost,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    print(f'Welcome {current_user.email}')
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Post with id : {id} not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=("Go Delete your own post."))
    
    db.delete(post)
    db.commit()
    return {"message":f"Post with ID: {id} succesfully removed."}