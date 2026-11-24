from fastapi import status, HTTPException
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.db.models import FeatureFlag, Rule
from app.schemas.flags import FlagResponse, FlagUpdate, FlagCreate, FlagDetailResponse, RuleCreate, RuleResponse, \
    RuleUpdate
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
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

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
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    update_values=flag_patch.model_dump(exclude_unset=True)
    for k, v in update_values.items():
        setattr(feature_flag, k, v)

    session.commit()
    session.refresh(feature_flag)
    return feature_flag

@router.delete("/"+con.EP_FLAG_KEY, status_code=status.HTTP_204_NO_CONTENT)
def delete_flag(flag_key:str, session:Session=Depends(get_db)):
    """Delete a specific flag with optional parameters.

    Args:
        flag_key: Key to be updated given in the URL.
        session: Database session injected via dependency.

    Returns:
        None on success.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    session.delete(feature_flag)
    session.commit()
    return None

@router.post("/" + con.EP_FLAG_KEY +"/" + con.EP_RULES, response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
def create_rule(flag_key:str, schema: RuleCreate, session:Session=Depends(get_db)):
    """Create a new rules for flag in URL.

    Persists rules derived from the provided pydantic payload,
    storing its attributes.

    Args:
        flag_key: Flag identifier in URL.
        schema: Validated payload describing the rules to create.
        session: Database session injected via dependency.

    Returns:
        RuleResponse: The newly created rules, refreshed from the database.

    Raises:
        HTTPException: 409 Conflict if a flag with the same ``flag_key`` does not exist.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag = session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    rule_orm = Rule(feature_flag_id=feature_flag.id,
                    name=schema.name,
                    rule_type=schema.rule_type,
                    conditions=schema.conditions.model_dump(),
                    enabled=schema.enabled,
                    )
    session.add(rule_orm)
    session.commit()
    session.refresh(rule_orm)

    return rule_orm

@router.patch("/" + con.EP_FLAG_KEY + "/" + con.EP_RULES + "/" + con.EP_RULE_ID, response_model=RuleResponse, status_code=status.HTTP_200_OK)
def update_rule(flag_key:str, rule_id:int, patch_schema:RuleUpdate, session:Session=Depends(get_db)):
    """Update a specific flag's rule(s) with optional parameters.

    Args:
        rule_id: Rule identifier.
        flag_key: Key to be updated given in the URL.
        patch_schema: Incoming rule schema object.
        session: Database session injected via dependency.

    Returns:
        Updated rule.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found or rule belong to different flag.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    stmt = select(Rule).where(Rule.id == rule_id, Rule.feature_flag_id == feature_flag.id) # check both rule_id and flag_id match
    rules = session.scalar(stmt)
    if not rules: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_RULE_FOUND)

    update_values=patch_schema.model_dump(exclude_unset=True)
    for k, v in update_values.items():
        setattr(rules, k, v)

    session.commit()
    session.refresh(rules)
    return rules

@router.get("/" + con.EP_FLAG_KEY + "/" + con.EP_RULES, response_model=list[RuleResponse], status_code=status.HTTP_200_OK)
def get_rule(flag_key:str, session:Session=Depends(get_db)):
    """Update a specific flag's rule(s) with optional parameters.

    Args:
        flag_key: Key to be updated given in the URL.
        session: Database session injected via dependency.

    Returns:
        Updated rule.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found or rule belong to different flag.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    stmt = select(Rule).where(Rule.feature_flag_id == feature_flag.id) # check flag_id match
    rules = session.scalars(stmt).all()

    return rules

@router.delete("/" + con.EP_FLAG_KEY + "/" + con.EP_RULES + "/" + con.EP_RULE_ID, status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(flag_key:str, rule_id:int, session:Session=Depends(get_db)):
    """Delete a specific rule with optional parameters.

    Args:
        flag_key: Key to be updated given in the URL.
        rule_id: Rule identifier.
        session: Database session injected via dependency.

    Returns:
        None on success.

    Raises:
        HTTPException: 404 Not Found, if no flag can not be found.
    """
    stmt = select(FeatureFlag).where(FeatureFlag.flag_key == flag_key)
    feature_flag=session.scalar(stmt)
    if not feature_flag: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_FLAG_KEY_FOUND)

    stmt = select(Rule).where(Rule.id == rule_id, Rule.feature_flag_id == feature_flag.id) # check both rule_id and flag_id match
    rules = session.scalar(stmt)
    if not rules: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=con.ERROR_NO_RULE_FOUND)

    session.delete(rules)
    session.commit()
    return None