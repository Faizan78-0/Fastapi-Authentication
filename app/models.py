from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String, nullable=True)
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)

    posts = relationship("Post", back_populates="owner", cascade="all,delete")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")

