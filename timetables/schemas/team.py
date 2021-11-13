from pydantic import Field

from ..base import Nameable
from .register import Register


class Team(Nameable):
    name: str = Field(
        title="Name",
        description="Name of the team within the register, including its name",
    )
    register_: Register = Field(
        title="Register", description="A register of which this team is a part"
    )

    # noinspection PyShadowingBuiltins
    @classmethod
    def hash_code(cls, name: str, **kwargs) -> str:
        register: Register = kwargs["register_"]
        return f"{register.name} {super().hash_code(name)}"
