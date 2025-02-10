from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_camel


class PublicCommand(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="ignore", frozen=True
    )
