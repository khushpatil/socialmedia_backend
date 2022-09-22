from fastapi import FastAPI, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


try:
    conn = psycopg2.connect(host= 'localhost', database= 'social_media_backend', user= 'postgres', password= 'KhushP@TIL70', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as err:
    print(err)

#Testing SqlAlchemy
# @app.get("/sqlalchemy")
# def testing(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return{"data": post}

@app.get("/posts")
def get_posts(db : Session = Depends(get_db)):

    #The following commands are without the use of an ORM
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=201)
def create_post(post: schemas.Post, db : Session = Depends(get_db)):

    # cursor.execute(""" INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db : Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)),)
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="The requested resource could not be found")
    return {"post detail": post}

@app.delete("/posts/{id}",status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=404, detail="The resouce could not be found")

    post.delete(synchronize_session=False)
    db.commit()

    return {"message": "The resource has been deleted successfullyy"}

@app.put("/posts/{id}", status_code=200)
def update_post(id: int, updated_post: schemas.Post, db : Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id))) 
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail="The resource could not be found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return{"data": post_query.first()}
