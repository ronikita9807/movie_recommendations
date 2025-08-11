from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str = Field(..., example="Saved successfully")


class ErrorResponse(BaseModel):
    detail: str = Field(
        ...,
        example="Duplicate key error: duplicate key value violates unique constraint ...",
    )
