from typing import List

import uvicorn
from fastapi import FastAPI, Response, Depends, HTTPException
from sql_app.database import SessionLocal, engine
import sql_app.crud as crud
import sql_app.models as models
from sqlalchemy.orm import Session
import schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{id}", response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    return


@app.get("/users", response_model=schemas.User)
def get_user_by_family_name(family_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_family_name(db, family_name)
    return user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}/permissions", response_model=schemas.User)
def grant_permission(user_id: int, permission_id: int, db: Session = Depends(get_db)):
    return crud.grant_permission_to_user(db, perm_id=permission_id, user_id=user_id)


@app.delete("/users/{user_id}/permissions")
def revoke_permission(user_id: int, permission_id: int, db: Session = Depends(get_db)):
    return crud.revoke_permission_from_user(db, perm_id=permission_id, user_id=user_id)


@app.delete("/users/{id}", response_model=schemas.User)
def create_user(id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, id)


@app.get('/permissions', response_model=List[schemas.Permission])
def get_permissions(db: Session = Depends(get_db)):
    return crud.get_permissions(db, 0, 100)


@app.post("/permissions", response_model=schemas.Permission)
def create_permission(perm: schemas.PermissionCreate, db: Session = Depends(get_db)):
    return crud.create_permission(db, perm)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
