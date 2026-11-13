from fastapi import status, HTTPException
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.db.models import FeatureFlag
from app.schemas.flags import FlagResponse, FlagUpdate, FlagCreate, FlagDetailResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api import constant as con

router = APIRouter(prefix="/"+con.EP_FLAGS, tags=[con.EP_FLAGS])
@router.post("/", response_model=FlagResponse, status_code=status.HTTP_201_CREATED)
def create_flag(schema: FlagCreate, session:Session=Depends(get_db))->FlagResponse:
    """Create a new feature flag.

    Persists a feature flag derived from the provided ``FlagCreate`` payload,
    storing its key, enabled state, rollout percentage, and optional target users.

    Args:
        schema: Validated payload describing the flag to create.
        session: Database session injected via dependency.

    Returns:
        FlagResponse: The newly created feature flag, refreshed from the database.

    Raises:
        HTTPException: 409 Conflict if a flag with the same ``flag_key`` already exists.
    """
    stmt=select(FeatureFlag).where(FeatureFlag.flag_key==schema.flag_key)
    flag_exists=session.scalar(stmt)
    if flag_exists: raise HTTPException(status.HTTP_409_CONFLICT, detail=con.ERROR_ALREADY_EXISTS)

    flag_orm=FeatureFlag(flag_key=schema.flag_key,
                     enabled=schema.enabled,
                     rollout_percentage=schema.rollout_percentage,
                     target_users=schema.target_users if schema.target_users is not None else None
                     )
    session.add(flag_orm)
    session.commit()
    session.refresh(flag_orm)
    return flag_orm # noqa

@router.get("/"+con.EP_FLAG_KEY, response_model=FlagDetailResponse, status_code=status.HTTP_200_OK)
def get_flag(flag_key:str, session:Session=Depends(get_db)):
    """Return A serialized Feature Flag with rules added identified in the URL.

    Args:
        flag_key: Key given in the URL.
        session: Database session injected via dependency.

    Raises:
        HTTPException: 404 Not Found, if flag can not be found.
    """
    stmt=select(FeatureFlag).where(FeatureFlag.flag_key==flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_KEY_FOUND)

    return feature_flag

@router.get("/", response_model=list[FlagResponse], status_code=status.HTTP_200_OK)
def get_flags(session:Session=Depends(get_db)):
    """Return rules exclusive, all flags in DB.

    Args:
        session: Database session injected via dependency.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found.
    """
    stmt=select(FeatureFlag)
    feature_flags=session.scalars(stmt).all()
    return feature_flags

@router.patch("/"+con.EP_FLAG_KEY, response_model=FlagResponse, status_code=status.HTTP_200_OK)
def patch_flag(flag_patch:FlagUpdate, flag_key:str, session:Session=Depends(get_db)):
    """Update a specific flag with optional parameters.

    Args:
        flag_patch: Incoming body.
        flag_key: Key to be updated given in the URL.
        session: Database session injected via dependency.

    Returns:
        Updated flag.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_KEY_FOUND)

    update_values=flag_patch.model_dump(exclude_unset=True)
    for k, v in update_values.items():
        setattr(feature_flag, k, v)

    session.commit()
    session.refresh(feature_flag)
    return feature_flag

