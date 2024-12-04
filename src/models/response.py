import uuid
from datetime import datetime

from pydantic import BaseModel, RootModel


class Entity(BaseModel):
    id: uuid.UUID
    case_id: str
    case_date: datetime
    name: str
    description: str | None


class AllEntities(RootModel[list[Entity]]):
    root: list[Entity]
