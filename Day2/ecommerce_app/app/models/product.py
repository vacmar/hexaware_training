from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)   # ✅ Capital C
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)   # ✅ Capital C
    category_id = Column(Integer, ForeignKey("categories.id"))  # ✅ Capital C
    
    category = relationship("Category", back_populates="products")  # ✅ Capital C
    orders = relationship("Order", back_populates="product")