from fastapi import FastAPI , status
from app.database import engine
import app.models
from app.routers import user , post , auth , vote
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

# app.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/', status_code=status.HTTP_200_OK)
def get_check() -> Dict:
    return dict(status='OK!!')

