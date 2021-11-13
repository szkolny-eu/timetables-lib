from datetime import date
from hashlib import md5
from typing import List, Optional, Type, TypeVar

from ...base import AppBaseModel, Nameable
from ...schemas import Classroom, Lesson, Register, Subject, Teacher, Team
from .file import File

T = TypeVar("T", bound=Nameable)


class Dataset(AppBaseModel):
    date_generated: date = date.today()
    lessons: List[Lesson] = []

    classrooms: List[Classroom] = []
    subjects: List[Subject] = []
    teachers: List[Teacher] = []

    registers: List[Register] = []
    teams: List[Team] = []

    files: List[File] = []

    @staticmethod
    def _read_object(
        items: List[T],
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
        **kwargs,
    ) -> Optional[T]:
        return next(
            filter(
                lambda item: item.matches(name, internal_id) and item.equals(**kwargs),
                items,
            ),
            None,
        )

    @classmethod
    def _has_object(
        cls,
        items: List[T],
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
        **kwargs,
    ) -> bool:
        return not not cls._read_object(items, name, internal_id, **kwargs)

    @classmethod
    def _get_object(
        cls,
        items: List[T],
        model: Type[T],
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
        **kwargs,
    ) -> T:
        item = cls._read_object(items, name, internal_id, **kwargs)
        if item and internal_id:
            item.internal_id = internal_id
        if item and name:
            item.name = name
        if not item:
            if not name:
                raise TypeError("Must specify the name to create an item")
            if not internal_id:
                hash_code = model.hash_code(name=name, **kwargs)
                digest = md5(hash_code.encode("utf-8")).digest()
                internal_id = int.from_bytes(digest, byteorder="big") % (10 ** 11)
            item = model(**kwargs, internal_id=internal_id, name=name)
            items.append(item)
        return item

    def get_classroom(
        self, name: Optional[str] = None, internal_id: Optional[int] = None, **kwargs
    ) -> Classroom:
        return self._get_object(
            items=self.classrooms,
            model=Classroom,
            name=name,
            internal_id=internal_id,
            **kwargs,
        )

    def get_subject(
        self, name: Optional[str] = None, internal_id: Optional[int] = None, **kwargs
    ) -> Subject:
        return self._get_object(
            items=self.subjects,
            model=Subject,
            name=name,
            internal_id=internal_id,
            **kwargs,
        )

    def get_teacher(
        self, name: Optional[str] = None, internal_id: Optional[int] = None, **kwargs
    ) -> Teacher:
        return self._get_object(
            items=self.teachers,
            model=Teacher,
            name=name,
            internal_id=internal_id,
            **kwargs,
        )

    # noinspection PyShadowingBuiltins
    def get_register(
        self,
        type: Register.Type,
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
        **kwargs,
    ) -> Register:
        return self._get_object(
            items=self.registers,
            model=Register,
            name=name,
            internal_id=internal_id,
            type=type,
            **kwargs,
        )

    def get_team(
        self,
        register: Register,
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
        **kwargs,
    ) -> Team:
        return self._get_object(
            items=self.teams,
            model=Team,
            name=name,
            internal_id=internal_id,
            register_=register,
            **kwargs,
        )

    def has_classroom(
        self, name: Optional[str] = None, internal_id: Optional[int] = None
    ) -> bool:
        return self._has_object(self.classrooms, name, internal_id)

    def has_subject(
        self, name: Optional[str] = None, internal_id: Optional[int] = None
    ) -> bool:
        return self._has_object(self.subjects, name, internal_id)

    def has_teacher(
        self, name: Optional[str] = None, internal_id: Optional[int] = None
    ) -> bool:
        return self._has_object(self.teachers, name, internal_id)

    # noinspection PyShadowingBuiltins
    def has_register(
        self,
        type: Register.Type,
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
    ) -> bool:
        return self._has_object(self.registers, name, internal_id, type=type)

    def has_team(
        self,
        register: Register,
        name: Optional[str] = None,
        internal_id: Optional[int] = None,
    ) -> bool:
        return self._has_object(self.teams, name, internal_id, register_=register)
