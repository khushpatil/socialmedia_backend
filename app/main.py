from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post,user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)

try:
    conn = psycopg2.connect(host= 'localhost', database= 'social_media_backend', user= 'postgres', password= 'KhushP@TIL70', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as err:
    print(err)



