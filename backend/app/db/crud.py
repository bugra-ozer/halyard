from sqlalchemy.orm import Session
from app.db.models import FeatureFlag
from app.schemas.flag import Flag, FlagUpdate
from sqlalchemy import select
import constant as con

def create_flag(db: Session, flag_data:Flag):
    """Insert a new feature flag.

    Args:
        db: Active SQLAlchemy session.
        flag_data: Validated payload describing the flag to create. Its
            ``target_users`` value is normalised to a ``list`` before storage.

    Returns:
        The persisted ``FeatureFlag`` ORM instance, refreshed from the database
        so that server-generated values (e.g. ``id``) are populated.
    """

    db_flag=FeatureFlag(flag_key=flag_data.flag_key,
                        enabled=flag_data.enabled,
                        rollout_percentage=flag_data.rollout_percentage,
                        target_users=normalise_target_users(flag_data.target_users))
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag

def normalise_target_users(target_users)-> list | None:
    """Normalise a ``target_users`` value into a JSON-serialisable list.

        Converts any non-``None`` iterable (set, tuple, generator, ...) into a
        ``list`` so the value can be stored in a JSON/text column.

        Args:
            target_users: An iterable of user identifiers, or ``None``.

        Returns:
            A ``list`` of user identifiers, or ``None`` if the input was ``None``.
        """
    result = (
        list(target_users)
        if target_users is not None
        else None
    )
    return result

def get_flags(db: Session, skip: int = 0, limit: int = 100)->list[FeatureFlag]:
    """Return a page of feature flags.

    Args:
        db: Active SQLAlchemy session.
        skip: Number of rows to offset (pagination start). Defaults to 0.
        limit: Maximum number of rows to return. Defaults to 100.

    Returns:
        A list of ``FeatureFlag`` instances (empty list if none match).
    """
    stmt = select(FeatureFlag).offset(skip).limit(limit) # build query object in Py memory.
    return list(db.scalars(stmt).all()) # it executes the Python query, and unpacks the objects from [(<FeatureFlag 1>,), (<FeatureFlag 2>,)]
                                        # to [<FeatureFlag 1>, <FeatureFlag 2>]

def get_flag_by_key(db: Session, flag_key:str):
    """Fetch a single feature flag by its unique key.

    Args:
        db: Active SQLAlchemy session.
        flag_key: The flag's unique identifier.

    Returns:
        The matching ``FeatureFlag``, or ``None`` if no such flag exists.
    """
    stmt=select(FeatureFlag).where(FeatureFlag.flag_key==flag_key)
    return db.scalar(stmt)

def delete_flag(db: Session, flag_key:str):
    """Delete a feature flag by key.

    Args:
        db: Active SQLAlchemy session.
        flag_key: The flag's unique identifier.

    Returns:
        The deleted ``FeatureFlag`` instance, or ``None`` if no flag with that
        key existed (in which case nothing is committed).
    """
    db_flag=get_flag_by_key(db, flag_key)
    if not db_flag: return None

    db.delete(db_flag)
    db.commit()
    return db_flag

def update_flag(db: Session, flag_key:str, update_data:FlagUpdate)->FeatureFlag|None:
    """Apply an update payload to an existing feature flag.

    Every field present on ``update_data`` is written onto the ORM instance;
    ``target_users`` is coerced to a list when it is not ``None``.

    Args:
        db: Active SQLAlchemy session.
        flag_key: The flag's unique identifier.
        update_data: Validated update payload. Note that dumping uses
            ``exclude_unset=False``, so *all* declared fields are written —
            including fields the client did not send.

    Returns:
        The refreshed ``FeatureFlag`` instance, or ``None`` if no flag with
        that key existed (in which case nothing is committed).
    """
    db_flag=get_flag_by_key(db, flag_key)
    if not db_flag: return None

    updates=update_data.model_dump(exclude_unset=False)

    for field, value in updates.items():
        if field == con.TARGET_USERS_KEY and value is not None:
            value = list(value)
        setattr(db_flag, field, value)

    db.commit()
    db.refresh(db_flag)
    return db_flag