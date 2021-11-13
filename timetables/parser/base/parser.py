from abc import abstractmethod
from time import time
from typing import Optional

from aiohttp import ClientSession

from .dataset import Dataset
from .file import File


class Parser:
    def __init__(self, ds: Optional[Dataset] = None):
        self.ds = ds or Dataset()
        self.session = ClientSession()

    def enqueue(self, *files: File) -> "Parser":
        for file in files:
            if file not in self.ds.files:
                self.ds.files.append(file)
        return self

    async def run_all(self, *files: File) -> Dataset:
        self.enqueue(*files)
        while len(self.ds.files):
            await self.run_next()
        await self.cleanup()
        return self.ds

    async def run_next(self) -> None:
        if not self.ds.files:
            return
        file = self.ds.files.pop(0)

        print(f"Parsing '{file}'... ", end="")
        start = time()
        await self._parse_file(file)
        end = time()
        print("{:.3f} s".format(end - start))

    async def cleanup(self) -> None:
        pass

    @abstractmethod
    async def _parse_file(self, file: File) -> None:
        raise NotImplementedError("This Parser instance is not implemented properly.")

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def __aenter__(self) -> "Parser":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()
