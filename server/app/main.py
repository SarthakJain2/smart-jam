from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import auth, applications, matcher

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Job Application Manager")

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(matcher.router)

@app.get("/")
async def root():
    return {"ok": True}