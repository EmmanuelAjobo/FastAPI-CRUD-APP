
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, status, Body, HTTPException, Path
from pydantic import BaseModel;
from typing import Annotated, Optional;
import psycopg;
import time;
from psycopg.rows import dict_row;



# Load environment variables from .env file
load_dotenv()

# Read variables from environment
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

app = FastAPI();

class postSchema(BaseModel):
    name: str
    price: int
    issale: bool|None = False
    inventory: int


################## CONNECTION TO DATABASE ##################
while True:
    try:
        conn = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, row_factory=dict_row, port=DB_PORT)
        cursor = conn.cursor();
        print("Database connection was successfull");
        break
    except Exception as error:
        time.sleep(2);
        print("Connecting to database failed")
        print("Error: ", error);







################## DELETE POST ##################

@app.delete("/delete/{id}")
async def deletePost(id: Annotated[int, Path()]):
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id), ))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found");
    return {"data": post}


################## GET POST ##################

@app.get("/posts")
async def getProducts():
    cursor.execute("""SELECT * FROM products """);
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
async def getProduct(id: Annotated[int, Path()]):
    cursor.execute("""SELECT * FROM products WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found");
    return {"data": post}


################## POST UPDATED ##################

@app.put("/update/{id}")
async def updatePost(id: Annotated[int, Path()], post: Annotated[postSchema, Body()]):
    cursor.execute("""UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING * """, (post.name, post.price, id, ));
    updated_post = cursor.fetchone() 
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found");
    return {"data": updated_post}


################## POST CREATED ##################

@app.post("/createPost/", status_code=status.HTTP_201_CREATED)
async def createProduct(product: Annotated[postSchema, Body()] ):
    cursor.execute("""INSERT INTO products (name, price, issale, inventory) VALUES (%s, %s, %s, %s) RETURNING * """, (product.name, product.price, product.issale, product.inventory))
    post = cursor.fetchone();
    conn.commit()
    return {"data": post}

