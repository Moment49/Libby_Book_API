from fastapi import FastAPI
from routers import user_authentication
from database.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the auth router
app.include_router(user_authentication.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LIBBY_BOOK_API app"}