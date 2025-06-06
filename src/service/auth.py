from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import logging
import secrets
import jwt

from src.config import settings
from src.init import redis_manager
from src.schemas.users import UsersRegistrationDTO
from src.service.base import BaseService
from src.tasks.tasks import validation_email


class AuthService(BaseService):

    pwd_context = CryptContext(
        schemes=["argon2", "bcrypt"], deprecated="auto", bcrypt__ident="2b"
    )

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)


    async def register(self, data):
        password = data.password.strip()
        if password:
            hashed_password = AuthService().hash_password(data.password)
            _data = UsersRegistrationDTO(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                login=data.login,
                number_phone=data.number_phone,
                password=hashed_password
            )
            try:
                await self.db.users.add_data(_data)
                await self.db.commit()
                code = f"{secrets.randbelow(10 ** 4):04d}"
                await redis_manager.set(_data.email, code, expire=600)
                code_val = await redis_manager.get(_data.email)
                logging.error(code_val)
                validation_email.delay(_data.email, code)
                verification_token = AuthService().create_access_token({"email": _data.email})
                logging.error(verification_token)
                return verification_token

            except Exception as e:
                logging.error(e)

