from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from . import oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Depends() 只負責先執行 dependency，然後取得它的回傳值。它不會判斷「這是不是 JWTError」。
# 不同 exception 的處理結果是：
# HTTPException：FastAPI 轉成對應的 HTTP response，例如 401。
# JWTError：你的 except JWTError 負責捕捉，再轉成 HTTPException。
# 沒有被捕捉的 TypeError、AttributeError、ValidationError：通常變成 500 Internal Server Error。
# 只要 dependency 拋出 exception，正常的 endpoint 都不會繼續執行。


@router.get("/sqlalchemy") 
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/", response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #cursor.execute('SELECT * FROM posts;')
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all()
    
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute('''
    #                 INSERT INTO posts 
    #                (title, content, published)
    #                VALUES (%s, %s, %s)
    #                RETURNING * 
    #                ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''
    #                 SELECT * FROM posts
    #                WHERE id = %s
    #                 ''', (id, ))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"Not authorized ot perform requested action")
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''
    #                 DELETE FROM posts
    #                WHERE id = %s
    #                RETURNING *;
    #                 ''', (id, ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"Not authorized ot perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Response)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''
    #                 UPDATE posts
    #                SET title = %s,
    #                     content = %s,
    #                     published = %s
    #                WHERE id = %s
    #                 RETURNING *;
    #                 ''', (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_get = updated_post.first()
    if post_get is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    
    if post_get.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"Not authorized ot perform requested action")

    updated_post.update(post.model_dump())
    db.commit()
    db.refresh(post_get)
    return post_get

