from datetime import date

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, text, Boolean, func
from sqlalchemy.orm import relationship

from models import Base
from tasks.models import TaskStatus, TaskPriority


class Roles(Base):
    __tablename__ = "role"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String, nullable=False, index=True)
    permission = Column("permission", JSON)

    users = relationship("Users", back_populates="roles")


class Users(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True, index=True)
    email = Column("email", String, unique=True, nullable=False, index=True)
    username = Column("username", String, nullable=False, index=True)
    hashed_password = Column("hashed_password", String, nullable=False)
    registered_at = Column("registered_at", TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    role_id = Column("role_id", Integer, ForeignKey("role.id"))

    is_active = Column("is_active", Boolean, default=True, nullable=False)
    is_superuser = Column("is_superuser", Boolean, default=False, nullable=False)
    is_verified = Column("is_verified", Boolean, default=False, nullable=False)

    roles = relationship("Roles", back_populates="users")