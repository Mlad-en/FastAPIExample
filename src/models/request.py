from datetime import datetime

from pydantic import BaseModel, Field


class Entity(BaseModel):
    case_id: str = Field(min_length=36, max_length=36)
    case_date: datetime
    name: str = Field(max_length=255)
    description: str | None = Field(default=None)
