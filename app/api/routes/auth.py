from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.config import settings
from app.services.user import authenticate_user
from app.core import security
from app.db.session import SessionLocal
from app.schemas.user import AccessToken, LoginForm, ValidateToken, RefreshToken, LoginToken
from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.dependecies import get_db
from app.api.dependencies import get_current_user, get_user_from_refresh_token, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter()

"""
Authentication Plan:

HTTP Only Cookies: It's considered a better practice to store tokens in HTTP Only cookies instead of Local Storage. 
Local Storage is accessible through JavaScript, and therefore vulnerable to cross-site scripting (XSS) attacks. 
HTTP Only cookies are not accessible via JavaScript and are automatically sent with every request to the server, 
making them a better choice for storing sensitive information like tokens.

Secure Flag on Cookies: If you are using cookies, make sure you set the secure flag on the cookies to ensure they 
are only sent over HTTPS.

SameSite Attribute on Cookies: Setting the SameSite attribute on your cookies can help to prevent cross-site request 
forgery (CSRF) attacks.

Implement CSRF Protection: Although it's less of an issue with token-based authentication, it's still a good idea to 
implement CSRF protection.

Content Security Policy (CSP): A Content Security Policy can help to prevent various types of attacks, including XSS 
and data injection attacks.

Check token validity: When you get the token from local storage, it's good practice to check its validity before 
using it. This can prevent issues where an expired or otherwise invalid token is used, leading to unnecessary 
requests to the server.

Error Handling: It's important to handle errors properly. In the catch block, instead of just logging a message, 
you should handle the error more gracefully. This might mean redirecting the user to a login page, showing an 
error message, or some other appropriate response. Make sure not to expose any sensitive information in error messages.

Use HTTPS: Always use HTTPS for any communication that involves sensitive data. HTTPS encrypts the data between 
the client and the server, protecting it from eavesdroppers.

"""

@router.post("/token", response_model=AccessToken)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": security.create_access_token(user.id),
    }

@router.post("/login", response_model=LoginToken)
def login(form_data: LoginForm, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.email, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        return {
            "access_token": security.create_access_token(user.id),
            "refresh_token": security.create_refresh_token(user.id),
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh", response_model=RefreshToken)
def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_user_from_refresh_token(db, refresh_token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer"
    }

@router.get("/validate")
def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")

    if not user:
        raise HTTPException(status_code=400, detail="Invalid access token")
    return {"detail": "Access token is valid"}