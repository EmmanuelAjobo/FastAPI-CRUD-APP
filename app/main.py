from fastapi import FastAPI, Depends ,status, Body, HTTPException, Path
from typing import Annotated;
from .engine import engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from .models import Product, ProductUpdate, ProductCreate

################## CONNECTION TO DATABASE ##################

#SESSION 
async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan);

################## DELETE POST ##################

@app.delete("/posts/{id}")
async def deletePost(session: Annotated[AsyncSession, Depends(get_db)], id: Annotated[int, Path()]):
    post = await session.get(Product, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return {"data": post}


################## GET POST ##################


@app.get("/posts")
async def getProducts(session: Annotated[AsyncSession, Depends(get_db)]):
    statement = select(Product)
    result = await session.exec(statement)
    products = result.all()
    return {"data": products}

@app.get('/posts/{id}')
async def getproduct(id: Annotated[int, Path()], session: Annotated[AsyncSession, Depends(get_db)]):
    product = await session.get(Product, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id could not be found")
    return {"data": product}


# ################## POST UPDATED ##################

@app.put("/posts/{id}")
async def updateProduct(id: Annotated[int, Path()], payload: Annotated[ProductUpdate, Body()] , session: Annotated[AsyncSession, Depends(get_db)]):
    #Fetch an existing Item
    product = await session.get(Product, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id could not be found")

    #Extract Incoming data (excluding unset field if using partial updates)
    #This is responsible for partial updates, meaning only the fields provided in the request will be updated, while the rest will remain unchanged.
    update_product = payload.model_dump(exclude_unset=True)

    #Update the existing database object attributes 
    for key, val in update_product.items():
        setattr(product, key, val)

    session.add(product)
    await session.commit()
    await session.refresh(product)

    return {"data": product}

# ################## POST CREATED ##################

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createPost(payload: Annotated[ProductCreate, Body()], session: Annotated[AsyncSession, Depends(get_db)]):
    product = Product.model_validate(payload)

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return {"data": product}