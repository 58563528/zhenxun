

import copy
from contextvars import ContextVar
from typing import Any, List, Dict, Type, TypeVar, Generic, AsyncIterator

from pydantic import BaseModel as _BaseModel, Field, parse_obj_as

from ..request import Requester

_T = TypeVar("_T", bound="BaseModel")

_requester: ContextVar[Requester] = ContextVar("_requester")


class BaseModel(_BaseModel):
    requester: Requester = Field(default_factory=_requester.get)

    def __init__(self, **data):
        hd = None
        if "requester" in data:
            hd = _requester.set(data["requester"])
        super(BaseModel, self).__init__(**data)
        if hd:
            _requester.reset(hd)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    async def close(self):
        await self.requester.close()

    @classmethod
    def parse_obj(cls: Type[_T], obj: dict) -> _T:
        return super(BaseModel, cls).parse_obj(obj)  # type: ignore


C = TypeVar("C", bound=BaseModel)


class PaginatedList(AsyncIterator, Generic[C]):

    def __init__(self,
                 cls: Type[C],
                 requester: Requester,
                 *args,
                 per_page: int = 30,
                 **kwargs):
        self.cls = cls
        self.requester = requester
        self.args = args
        self.kwargs = kwargs
        self.per_page = per_page
        self._contents: List[C] = []
        self._index = 0
        self._current_page = 0

    async def __anext__(self) -> C:
        if self._index >= len(self._contents):
            content = await self._get_next_page()
            if not content:
                raise StopAsyncIteration
        current = self._contents[self._index]
        self._index += 1
        return current

    def __aiter__(self) -> "PaginatedList[C]":
        new_page = copy.deepcopy(self)
        new_page._index = 0
        return new_page

    async def _get_next_page(self) -> List[C]:
        self._current_page += 1
        params: Dict[str, Any] = self.kwargs.setdefault("params", {})
        params["page"] = self._current_page
        params["per_page"] = self.per_page
        response = await self.requester.request_json(*self.args, **self.kwargs)
        content = response.json()
        self._contents.extend([
            parse_obj_as(self.cls, {
                "requester": self.requester,
                **x
            }) for x in content
        ])
        return content


from .issue import Issue
from .label import Label
from .license import License
from .comment import Comment
from .hook import Hook, HookConfig
from .timeline import TimelineEvent
from .permissions import Permissions
from .user import User, Organization
from .repository import LazyRepository, Repository
