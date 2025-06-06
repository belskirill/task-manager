import logging


from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from src.api.dependencies import DBDep
from src.schemas.users import UsersRegistrationDTO
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(
    data: UsersRegistrationDTO,
    db: DBDep,
    response: Response,
):
    try:
        res = await AuthService(db).register(data)
        response.set_cookie("temporary_token_verification", res)
        return {"status": "success"}


    except Exception as e:
        logging.error(e)


@router.post("/register/verification")
async def verification_email(
    code: int
):
    ...