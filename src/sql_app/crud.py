from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import UserCreate
from schemas import PermissionCreate
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_family_name(db: Session, family_name: str):
    return db.query(models.User).filter(models.User.family_name == family_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.deleted == False).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    setattr(db_user, 'deleted', True)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user: UserCreate):
    db_user = models.User(email=user.email, family_name=user.family_name, given_name=user.given_name,
                          birthdate=user.birthdate)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()


def create_permission(db: Session, permission: PermissionCreate):
    db_perm = models.Permission(type=permission.type, display_name=permission.display_name)
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm


# I'm sure there is a better way to do these last two functions than what I am doing here.... Given real world effort
# I would find the best way...
def grant_permission_to_user(db: Session, perm_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    permission = db.query(models.Permission).filter(models.Permission.id == perm_id).first()

    if user:
        if user.permissions is not None:
            perms = []
            for perm in user.permissions:
                perms.append(perm)
            perms.append(permission)
            setattr(user, 'permissions', perms)
        else:
            setattr(user, 'permissions', [permission])
        db.commit()
        db.refresh(user)
        return user
    raise HTTPException(detail=f"No user with id {user_id}", status_code=400)


def revoke_permission_from_user(db: Session, perm_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    perm_lookup = db.query(models.permission_instance).filter(models.User.id == user_id,
                                                              models.Permission.id == perm_id).first()
    if user and perm_lookup:
        perms = []
        for perm in user.permissions:
            if perm.id != perm_id:
                perms.append(perm)
        setattr(user, 'permissions', perms)
        db.commit()
        db.refresh(user)
        return user
    if not user:
        raise HTTPException(detail=f"No user with id {user_id}", status_code=400)
    if not perm_lookup:
        # Business logic dependant usually, would just return a 200 and carry on as not to leak data.
        raise HTTPException(detail="Permission not granted to user", status_code=400)
