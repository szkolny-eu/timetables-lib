from enum import IntEnum
from typing import Optional

from pydantic import Field

from ..base import Nameable
from .url import URL


class Register(Nameable):
    class Type(IntEnum):
        CLASS = 0
        OTHER = 1

    name: str = Field(title="Name", description="Name of the register")
    type: Type = Field(title="Type", description="Type of the group")
    url: Optional[URL] = Field(
        None, title="URL", description="An URL of this register's timetable"
    )

    # noinspection PyShadowingBuiltins
    @classmethod
    def hash_code(cls, name: str, **kwargs) -> str:
        type: Register.Type = kwargs["type"]
        return f"{type.name} {super().hash_code(name)}"
