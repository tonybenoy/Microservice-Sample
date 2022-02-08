from typing import Any, Dict

from pydantic import BaseModel

from enum import Enum, IntEnum


class PublishedStatus(IntEnum):
    unpublished = 0
    published = 1


class TypeQuestions(IntEnum):
    text = 0
    number = 1
    date = 2


class Status(str, Enum):
    active = "active"
    inactive = "inactive"


class FormNew(BaseModel):
    name: str
    published: PublishedStatus = PublishedStatus.published


class FormDefinitionNew(BaseModel):
    type: TypeQuestions
    question: str
    published: PublishedStatus = PublishedStatus.published


class FormDataNew(BaseModel):
    data: Dict[str, Any]


class IntegrationNew(BaseModel):
    name: str
    action: str


class AssignIntegration(BaseModel):
    form_id: int
    integration_id: int
