from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import get_session, User
from ..schemas import UserCreate, UserOut, Token
from ..services.auth import AuthService, AuthenticationError
from ..services.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_session)) -> UserOut:
    try:
        created = service.create_user(db, user.email, user.password)
        return {"id": created.id, "email": created.email}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)) -> Token:
    try:
        # OAuth2PasswordRequestForm sends 'username', we treat it as email
        user = service.authenticate_user(db, form_data.username, form_data.password)
        token = service.create_access_token(subject=user.id)
        return Token(access_token=token)
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)) -> UserOut:
    return {"id": current_user.id, "email": current_user.email}
