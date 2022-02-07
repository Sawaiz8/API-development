from fastapi import FastAPI
from .routers import post, user, authentication

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)





                