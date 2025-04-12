from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


class Auth0:
    def __init__(self, domain=settings.AUTH0_DOMAIN, audience=settings.AUTH0_API_AUDIENCE):
        self.domain = domain
        self.audience = audience
        self.jwks_url = f"https://{domain}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(self.jwks_url)
        self.algorithm = "RS256"  
        self.issuer = f"https://{domain}/"
        self.auth0_token = settings.AUTH0_TOKEN

    async def verify_token(self, token: str):
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token
            ).key
        except jwt.exceptions.PyJWKClientError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication error: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.exceptions.DecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication error: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self.algorithm,
                audience=self.audience,
                issuer=self.issuer,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication error: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload



auth0 = Auth0()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    try:
        token = credentials.credentials
        payload = await auth0.verify_token(token)
        auth0_user_id = payload.get("sub")
        if not auth0_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not found in token",
            )
        
        logger.info(f"Authenticating user with email: {email}")
        
        stmt = select(User).where(User.id == auth0_user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if user:
            logger.info(f"Found user by Auth0 ID: {auth0_user_id}")
            return user
        
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if user:
            logger.info(f"Found user by email: {email}")
            if user.id != auth0_user_id:
                user.id = auth0_user_id
                await db.commit()
                await db.refresh(user)
                logger.info(f"Updated Auth0 ID for user: {email}")
            return user
        
        logger.info(f"Creating new user with email: {email}")
        user = User(id=auth0_user_id, email=email, full_name=payload.get("name"))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise
