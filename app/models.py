from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    def set_password(self, password: str):
        """Сохраняет пароль в поле password."""
        self.password = password

    def verify_password(self, password: str) -> bool:
        """Проверяет, соответствует ли введенный пароль сохраненному паролю."""
        return password == self.password


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))


User.photos = relationship("Photo", back_populates="user")
Photo.user = relationship("User", back_populates="photos")
