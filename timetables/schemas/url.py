from typing import TypeVar

from pydantic import FilePath, HttpUrl

URL = TypeVar("URL", HttpUrl, FilePath)
