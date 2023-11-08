from pydantic import BaseModel


class DeleteModel(BaseModel):
    filename: str
