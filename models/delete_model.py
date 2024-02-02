from pydantic import BaseModel


# DeleteModel: Model for delete request
class DeleteModel(BaseModel):
    filename: str
