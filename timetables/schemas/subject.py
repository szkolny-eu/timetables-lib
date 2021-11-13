from pydantic import Field

from ..base import Nameable


class Subject(Nameable):
    name: str = Field(title="Name", description="Name of the subject")
