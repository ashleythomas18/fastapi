from fastapi import FastAPI, Depends, status, Response, HTTPException
import models
import schemas
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
from typing import Optional
from typing import List
import uvicorn
from pydantic import BaseModel
from passlib.context import CryptContext


models.Base.metadata.create_all(bind=engine) #the reason tableplus pr tables shpw horhi hai


app= FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# @app.post('/blog')
# def create(request: schemas.Blog, db: Session= Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog



'''@app.get("/blog")
def index(limit=10, published:bool=True,sort: Optional[str]= None):
    

    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}'''

    #only get 10 published blogs
    #return {'data':f'{limit} blogs from the db'}

# @app.get('/blog/unpublished')

# def unpublished():
#     return {'data': 'all unpublished blogs'}


@app.get("/blog/{id}")
def show(id: int):

    #fetch blog woth id=id
    return{'data':id}


# @app.get('/blog/{id}/comments')
# def comments(id,limit=10):
    
#     return{'data':{1,2}}



@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session= Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy (id,db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id of{id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED)
def update(id,request: schemas.Blog, db: Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).update(request)
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with id of{id} not found")
    blog.update(request)
    db.commit()
    return 'updated'


@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db:Session=Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response: Response, db:Session=Depends(get_db)):         #this db:session is for connection to database
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return{'detail': f"Blog with the id {id} is not available"}
    return blog

@app.post('/blog')

def create_blog(request: schemas.Blog):
    
    return {'data': f'Blog is created with title  {request.title}'}
    
#if __name__== "__main__":
#    uvicorn.run(app,host="127.0.0.1", port=8000)

pwd_cxt= CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', response_model=schemas.User)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashedPassword= pwd_cxt.hash(request.password)
    new_user=models.User(name= request.name, email=request.email, password= hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

 
