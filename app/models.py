from .database import Base
from sqlalchemy import TIMESTAMP, text, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id= Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "TRUE")
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

#     查詢後：
# post = db.query(models.Post).first()
# 可以取得 ID：
# post.owner_id
# # 12
# 加入 relationship() 後，還可以直接取得使用者物件：
# post.owner
# # User(id=12, email="abc@example.com", ...)
# 因此可以寫：
# post.owner.email
# 而不需要手動查詢：
# db.query(models.User).filter(
#     models.User.id == post.owner_id
# ).first()
# owner = relationship("User")
# 只改變 SQLAlchemy ORM 的 Python 層，不會修改 database table，所以不需要 migration，也不需要重新建立 table。
#relationship把foreign key的關係存進去了
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))


    
