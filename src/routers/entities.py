from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db import actions, session
from src.db.errors import DBNotFoundError
from src.models import request, response

router = APIRouter(
    prefix="/entities",
)


@router.post("/", response_model=response.Entity)
def create_entity(
    entity: request.Entity, db: Session = Depends(session.get_db)
) -> response.Entity:
    db_entity = actions.create_db_entity(entity, db)
    return response.Entity(**db_entity.__dict__)


@router.get("/", response_model=response.AllEntities)
def get_all_entities(db: Session = Depends(session.get_db)) -> list[response.Entity]:
    entities = actions.get_all_db_entities(db)
    return [response.Entity(**entity.__dict__) for entity in entities]


@router.get("/{uuid}", response_model=response.Entity)
def get_entity(uuid: UUID, db: Session = Depends(session.get_db)):
    try:
        db_entity = actions.get_db_entity(uuid, db)
        return response.Entity(**db_entity.__dict__)
    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{uuid}", response_model=response.Entity)
def update_entity(
    uuid: UUID, update_values: request.Entity, db: Session = Depends(session.get_db)
):
    try:
        db_entity = actions.update_db_entity(uuid, update_values, db)
        return response.Entity(**db_entity.__dict__)
    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{uuid}", response_model=response.Entity)
def delete_entity(uuid: UUID, db: Session = Depends(session.get_db)):
    try:
        db_entity = actions.delete_db_entity(uuid, db)
        return response.Entity(**db_entity.__dict__)
    except DBNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
