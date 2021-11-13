from os.path import dirname
from pathlib import Path
from typing import Union

import aiofiles
from aiohttp import ClientSession
from pydantic import HttpUrl

from ...base import AppBaseModel


class File(AppBaseModel):
    path: Union[HttpUrl, Path, str]

    async def read(self, session: ClientSession) -> bytes:
        if isinstance(self.path, HttpUrl):
            async with session.get(str(self.path)) as r:
                data = await r.read()
        elif isinstance(self.path, Path):
            async with aiofiles.open(self.path, "rb") as f:
                data = await f.read()
        else:
            raise TypeError("Path must be a valid URL or file path.")
        return data

    def parent(self) -> "File":
        if isinstance(self.path, HttpUrl):
            return File(path=dirname(self.path))
        elif isinstance(self.path, Path):
            return File(path=self.path.parent)
        else:
            raise TypeError("Path must be a valid URL or file path.")

    def child(self, name: str) -> "File":
        if isinstance(self.path, HttpUrl):
            return File(path=self.path + "/" + name)
        elif isinstance(self.path, Path):
            return File(path=self.path.joinpath(name))
        else:
            raise TypeError("Path must be a valid URL or file path.")

    def sibling(self, name: str) -> "File":
        return self.parent().child(name)

    def __str__(self) -> str:
        return str(self.path)

    def __hash__(self) -> int:
        return hash(self.path)
