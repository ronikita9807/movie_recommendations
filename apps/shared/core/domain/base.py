from abc import ABCMeta
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDomainModel(BaseModel, metaclass=ABCMeta):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


class BaseDTOModel(BaseModel, metaclass=ABCMeta):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        loc_by_alias=True,
        frozen=True,
        populate_by_name=True,
    )

    def serialize(self) -> dict[str, Any]:
        return self.model_dump(
            mode="json", exclude_none=True, exclude_unset=True, by_alias=True
        )
