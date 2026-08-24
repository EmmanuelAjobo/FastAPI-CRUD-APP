from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional



#If the product table is not available it is going to create it.
class Product(SQLModel, table=True):
    __tablename__ = "products"
    name: str = Field(nullable= False)
    price: int = Field(nullable=False)
    id: int | None = Field(primary_key=True, nullable=False, default=None)
    issale: bool | None = Field(default=False, nullable=False)
    inventory: int | None = Field(default=0, nullable=False)
    createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[int] = None
    issale: Optional[bool] = None
    inventory: Optional[int] = None

class ProductCreate(SQLModel):
    name: str
    price: int
    issale: bool = False
    inventory: int = 0