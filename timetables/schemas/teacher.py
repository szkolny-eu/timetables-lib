from typing import Optional

from pydantic import Field, PrivateAttr

from ..base import Nameable
from .url import URL


class Teacher(Nameable):
    name: str = Field(
        title="Full Name",
        description="The teacher's full name, or an abbreviation if not available",
    )
    url: Optional[URL] = Field(
        None, title="URL", description="An URL of this teacher's timetable"
    )
    __name_full__: Optional[str] = PrivateAttr(None)
