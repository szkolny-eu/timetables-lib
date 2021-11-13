from typing import Optional

from pydantic import Field, PrivateAttr

from ..base import Nameable
from .url import URL


class Classroom(Nameable):
    name: str = Field(title="Name", description="Name of the classroom")
    url: Optional[URL] = Field(
        None, title="URL", description="An URL of this classroom's timetable"
    )
    __name_full__: Optional[str] = PrivateAttr(None)
