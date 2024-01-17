from datetime import datetime

from pydantic import BaseModel


class ParstxtCreate(BaseModel):
    id: int
    datetime: datetime
    title: str
    count_x: int

class Message(BaseModel):
    message: str