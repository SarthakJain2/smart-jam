from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import auth, applications, matcher, users

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="Smart Job Application Manager")

# ✅ CORS MIDDLEWARE — put it here, BEFORE any custom middleware or routers
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Then your custom middleware
@app.middleware("http")
async def log_request(request: Request, call_next):
    if request.method == "POST":
        body = await request.body()
        print("📩 Incoming POST:", request.url.path)
        print("📦 Body:", body.decode())
    response = await call_next(request)
    return response


# ✅ Then include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(applications.router)
app.include_router(matcher.router)


@app.get("/")
async def root():
    return {"ok": True}
