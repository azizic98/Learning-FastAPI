from fastapi import Depends , status , HTTPException , APIRouter
from requests import Session
from ..  import schemas , database , models , oauth2

router = APIRouter(
    prefix = "/vote",
    tags= ['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db : Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Abe oye Andhe , Aisi koi post nahi hai yaha.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1): 
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Kitna Vote Karega re Baba? Ho gaya tera , tu jaa!")
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message":f"Voted : +{vote.dir}"}

    elif (vote.dir==0):
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pehle vote to karle , bada aaya vote hatane wala.")
        vote_query.delete(synchronize_session =False)
        db.commit()

        return {"Message":"Haa , Hat Gaya Vote."}
    
    

        