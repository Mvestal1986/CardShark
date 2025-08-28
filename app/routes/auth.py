from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import get_session
from ..schemas import UserCreate, UserLogin
from ..services.auth import AuthService, AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_session)):
    try:
        created = service.create_user(db, user.email, user.password)
        return {"id": created.id, "email": created.email}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_session)):
    try:
        user = service.authenticate_user(db, credentials.email, credentials.password)
        return {"message": "Login successful", "user_id": user.id}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
