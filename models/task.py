from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class Task(Base):
    """Task database model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship: Many tasks belong to one user
    user = relationship("User", back_populates="tasks")


@router.post("/api/users/") 
def create_user_bad(user_data: UserCreate, db: Session = Depends(get_db)):
    # HTTP + Logika biznesowa + dostęp do danych = MESS
    if not user_data.username:  # Logika biznesowa pośród routingu
        raise HTTPException(400, "Username required")
    user = User(username=user_data.username, email=user_data.email)
    db.add(user)  # Bezpośrednie połączenie do DB w routingu
    db.commit()
    return user