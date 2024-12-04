from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from src.db.errors import DBNotFoundError
from src.db.models import DBEntity
from src.models import request


def create_db_entity(entity: request.Entity, session: Session) -> DBEntity:
    db_entity = DBEntity(**entity.model_dump(exclude_none=True))
    session.add(db_entity)
    session.commit()
    session.refresh(db_entity)
    return db_entity


def get_db_entity(uuid: UUID, session: Session) -> DBEntity:
    entity = (
        session.query(DBEntity)
        .filter(DBEntity.id == uuid, DBEntity.is_deleted == False)
        .first()
    )
    if not entity:
        raise DBNotFoundError(f"Entity with id {uuid} was not found.")
    return entity


def get_all_db_entities(session: Session) -> list[DBEntity]:
    entities = session.query(DBEntity).filter(DBEntity.is_deleted == False).all()
    return entities


def delete_db_entity(uuid: UUID, session: Session) -> DBEntity:
    db_entity = get_db_entity(uuid, session)
    db_entity.is_deleted = True
    db_entity.updated_at = datetime.now()
    session.commit()
    session.refresh(db_entity)
    return db_entity


def update_db_entity(
    uuid: UUID, update_properties: request.Entity, session: Session
) -> DBEntity:
    db_entity = get_db_entity(uuid, session)
    for prop, new_value in update_properties.model_dump(exclude_none=True).items():
        setattr(db_entity, prop, new_value)
    db_entity.updated_at = datetime.now()
    session.commit()
    session.refresh(db_entity)
    return db_entity
