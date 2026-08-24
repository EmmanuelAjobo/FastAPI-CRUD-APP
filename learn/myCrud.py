from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


############################ SCHEMAS ############################
# publihed default value if false.
# Making use of Rating, we are not putting any value
class postSchema(BaseModel):
    name: str
    email: str
    published: bool = False
    rating: Optional[int] = None



############################ VARIABLES ############################
# this represents where the post created will be stored
myPosts = []


############################ FUNCTIONS ############################

def find_post(id): 
    for p in myPosts:
        if p["id"] == id:
            return p;

def findIndexPost(id):
    for i, p in enumerate(myPosts):
        if p['id'] == id:
            return i


############################ POST ############################


# Body retrieves body json and convert to python dictionary
#schema tells us what kind of data the user returns to us
@app.post("/post", status_code=status.HTTP_201_CREATED)
async def createPost(payload: postSchema):
    post_dict = payload.dict();
    # this can create a field ID
    post_dict["id"] = randrange(0, 10000)
    myPosts.append(post_dict);
    return {"body": post_dict}




############################ Delete Post ############################
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(id: int):
    postToDelete = findIndexPost(id)
    if postToDelete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does not exist")
    myPosts.pop(postToDelete);
    return Response(status_code=status.HTTP_204_NO_CONTENT)

############################ Update ############################

@app.put('/post/{id}')
async def updatePost(id: int, body: postSchema):
    index = findIndexPost(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does not exist")
    postDict = index.dict();
    postDict["id"] = id
    myPosts[index] = postDict
    return Response(status_code=status.HTTP_200_OK)


############################ GET ############################

@app.get("/getPost/{id}")
async def getSinglePost(id: int):
    p = find_post(id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} is not found")
    return {"body": p}




@app.get("/getAllPost")
async def getPost():
    return {
        "data": myPosts
    }


############################ Learn ############################

# @app.get("/files/")
# async def readFiles(path: str | None = None):
