from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta
from src.model import SentenceInput, OutputModel, TokenData, User, Token
from typing import List, Dict, Annotated
import random
import hashlib
from src.constants import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth import get_user, create_access_token, authenticate_user
import json

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


with open("src/db.json") as f:
    db = json.load(f)


def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/health_check", status_code=status.HTTP_200_OK)
def health_check() -> Dict:
    return {"status": "ok"}


@app.post("/get_array", status_code=status.HTTP_200_OK, response_model=OutputModel)
def get_array(
    inp: SentenceInput, current_user: Annotated[User, Depends(get_current_active_user)]
) -> List[float]:
    sentence = inp.sentence
    seed = int(hashlib.sha256(sentence.encode()).hexdigest(), 16)
    random.seed(seed)
    array_length = 500
    random_floats = [random.uniform(1.0, 1000.0) for _ in range(array_length)]
    response = {"output": random_floats}
    print(response)
    return response
