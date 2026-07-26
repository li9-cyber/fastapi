from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from . import oauth2
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote {vote.post_id} does not exist")
    
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'user {current_user.id} has already liked the post')
        
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else: 
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
#         synchronize_session=False 的意思是：
# 執行 UPDATE 或 DELETE 時，只修改 database，不要立即同步 SQLAlchemy Session 中已經載入的 Python 物件。
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted the post"}