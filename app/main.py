from fastapi import FastAPI
from .routers import post, user, authentication #import files

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)





                