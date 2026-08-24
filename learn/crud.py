from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


 
class PostSchema(BaseModel):
    title: str
    content: str


# This represent an existing json file
Post_Obj = [{
    "id": 1,
    "title": "Title of content 1",
    "content": "Content of post 1"
}, {
    "id": 2,
    "title": "Title of content 2",
    "content": "Content of post 2"
}]


@app.get("/get_all_posts")
async def get_all_posts():
    print("get")
    return {"data": Post_Obj}






@app.get("/posts/latest")
async def get_latest_post():
    post = Post_Obj[len(Post_Obj)-1]
    return {"detail": post}




async def find_post(id):
    for p in Post_Obj:
        if p["id"] == id:
            return p

async def find_id_index(id): 
    for i, p in enumerate(Post_Obj):
        if p['id'] == id:
            return i

# {id} is the path parameter
# @app.get("/get_post/{id}")
# async def get_post(id: int, response: Response):

#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"error message": f"post with id: {id} was not found"}
#     return {"data of a post": f"Here is post {id}"}





@app.get("/get_post/{id}")
async def get_post(id: int, response: Response):

    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Here is post {id}")
        
    return {"data of a post": f"Here is post {id}"}






@app.post("/post", status_code=status.HTTP_201_CREATED)
async def post(payload: PostSchema):
    # Puting the body req in a variable
    Post_Dict = payload.dict()

    # Overwriting and creating a new obj variable with new variable
    Post_Dict['id'] = randrange(0, 1000000) 

    # Updating the post Obj with new data 
    Post_Obj.append(Post_Dict)

    return {"data": Post_Dict}










@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int):
    #deleting post
    # find the index in the array that has required ID
    # Post_Obj.pop(index)
    index = find_id_index(id)

    #if you did =not find the index
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot delete what is not there")
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot delete what is not there")

    Post_Obj.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)








@app.put("/put")
async def put():
    print("put")

@app.patch("/patch")
async def patch():
    print("patch")
