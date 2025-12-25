#backend\auth.py
# backend/auth.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt
from fastapi import HTTPException, status
import os

# Security
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fix for bcrypt issues - use specific configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",  # Explicitly set bcrypt version
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Handles bcrypt's 72-byte limit and fallback if needed.
    """
    try:
        # Encode to bytes for bcrypt
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Try direct bcrypt first (more reliable)
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        try:
            # Fallback to passlib if bcrypt fails
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            print(f"Password verification error: {e}")
            return False

def get_password_hash(password: str) -> str:
    """
    Generate password hash with bcrypt.
    Automatically handles 72-byte limit.
    """
    # Truncate to 72 bytes if password is too long
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes, then decode back to string
        truncated_bytes = password_bytes[:72]
        # Try to decode, ignoring errors if truncated in middle of character
        password = truncated_bytes.decode('utf-8', 'ignore')
        # If empty after decode, use raw bytes
        if not password:
            password = truncated_bytes.decode('utf-8', 'replace')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role", "student")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"email": email, "role": role}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )