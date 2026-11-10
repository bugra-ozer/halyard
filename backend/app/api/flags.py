from fastapi import status, HTTPException
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.db.models import FeatureFlag
from app.schemas.flags import FlagResponse, FlagUpdate, FlagCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api import constant as con

router = APIRouter(prefix="/"+con.FLAG, tags=[con.FLAG])
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