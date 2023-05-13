from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.user import TokenData

"""
Security Plan:

HTTPS: Use HTTPS for all API requests to ensure the data is encrypted during transit. This will protect against 
man-in-the-middle attacks and eavesdropping.

CORS: Configure Cross-Origin Resource Sharing (CORS) policies on your server. CORS is a security feature that allows 
or denies scripts on a web page to request data from your API on a different domain.

Rate Limiting: Implement rate limiting to prevent abuse and protect your API from denial-of-service attacks. It can 
limit the number of requests a client can make in a specific time period.

Input Validation: Validate all inputs on the server-side even if you've validated them on the client-side. Never trust 
data coming from the client as it can be tampered with.

Content Security Policy (CSP): Implement CSP on your front end. It reduces the risk of cross-site scripting (XSS) 
attacks by allowing you to specify the domains that the browser should consider as valid sources of executable scripts.

X-XSS-Protection and X-Content-Type-Options: These HTTP headers add an extra layer of protection against XSS and MIME 
type attacks, respectively.

Regularly Update Dependencies: Keep all the libraries and dependencies of your project up-to-date as they might contain 
important security patches.

Security Scanners and Penetration Testing: Use automated security scanners to find vulnerabilities. Consider hiring 
professionals for penetration testing as well.
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(subject: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRE_TIMEDELTA

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRE_TIMEDELTA

    to_encode = {"exp": expires_delta, "sub": str(subject),
        "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt