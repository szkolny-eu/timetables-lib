from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


def to_camel_caps(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def to_camel_case(name: str) -> str:
    name = name.title()
    return name[0].lower() + name[1:]


class AppBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel_caps
        allow_population_by_field_name = True

    def equals(self, **kwargs) -> bool:
        d = self.dict()
        return all(d[k] == v for k, v in kwargs.items() if k and v)


class AppGenericModel(GenericModel):
    class Config:
        alias_generator = to_camel_caps
        allow_population_by_field_name = True


class UUIdentifiable(AppBaseModel):
    internal_id: UUID = Field(title="Internal ID")


class Identifiable(AppBaseModel):
    internal_id: int = Field(title="Internal ID")


class Nameable(Identifiable):
    name: str = Field(title="Name")

    def matches(self, name: Optional[str], internal_id: Optional[int]) -> bool:
        return self.name == name or self.internal_id == internal_id

    @classmethod
    def hash_code(cls, name: str, **kwargs) -> str:
        return name
