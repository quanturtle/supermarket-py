from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from models import get_session


router = APIRouter(prefix="", tags=["health"])
health_router = router


@router.get('/health', status_code=status.HTTP_200_OK)
async def health_check(session: Session = Depends(get_session)):
    return {'status': 'ok'}