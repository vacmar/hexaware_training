from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)  # ✅ Capital C
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # ✅ Capital C

    customer = relationship("Customer", back_populates="orders")  # ✅ Capital C
    product = relationship("Product", back_populates="orders")  # ✅ Capital C