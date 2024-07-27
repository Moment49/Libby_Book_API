from fastapi import FastAPI,Depends,APIRouter,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from repository import user
from models import user_model
from database import database
from database.database import  Base,engine
from schemas import user_schemas
from config.hashing import Hash
from config import token

get_db = database.get_db
Base.metadata.create_all(bind=engine)
app = FastAPI()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup",response_model=user_schemas.UserCreateResponse,status_code=status.HTTP_201_CREATED)
def create_user(request:user_schemas.CreateAccount,db: Session = Depends(get_db)):
    new_user = user.createUser(request,db)
    return {"message": "Account successfully created", "user": new_user}
    

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}