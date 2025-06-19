from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    String,
    ForeignKey,
)
from src.common.databases.postgres import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    short_description = Column(String(20), nullable=True)
    is_active = Column(Boolean)

    categories = relationship("ProductCategory", back_populates="product")
    # images = relationship()
    # discounts = relationship()
    # stock_records = relationship()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    products = relationship("ProductCategory", back_populates="category")
    parent = relationship("Category", back_populates="subcategories", remote_side="categories.c.id")
    subcategories = relationship("Category", back_populates="parent")

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    category = relationship("Category", back_populates="products")
    product = relationship("Product", back_populates="categories")




