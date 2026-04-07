from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True)
    employee_id = Column(String(50), unique=True)
    avatar = Column(String(255))
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role = relationship("Role", back_populates="users")
    operations = relationship("Operation", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="category")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    capacity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="zone")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    article = Column(String(100), unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="SET NULL"))
    quantity = Column(Integer, default=0)
    unit = Column(String(20), default="шт")
    price = Column(DECIMAL(10, 2), default=0.00)
    barcode = Column(String(100))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    zone = relationship("Zone", back_populates="products")
    operation_items = relationship("OperationItem", back_populates="product")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String(50), nullable=False, index=True)
    operation_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(30), default="pending", index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    supplier_customer = Column(String(255))
    total_amount = Column(DECIMAL(12, 2), default=0.00)
    notes = Column(Text)
    operation_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="operations")
    items = relationship("OperationItem", back_populates="operation", cascade="all, delete-orphan")


class OperationItem(Base):
    __tablename__ = "operation_items"

    id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(Integer, ForeignKey("operations.id", ondelete="CASCADE"), index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), default=0.00)
    from_zone_id = Column(Integer, ForeignKey("zones.id", ondelete="SET NULL"))
    to_zone_id = Column(Integer, ForeignKey("zones.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    operation = relationship("Operation", back_populates="items")
    product = relationship("Product", back_populates="operation_items")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())