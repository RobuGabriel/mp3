from sqlalchemy import Column, Integer, String
from database import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(String)
    category = Column(String)
    description = Column(String)
    images = Column(String)