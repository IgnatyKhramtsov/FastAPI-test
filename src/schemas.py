from datetime import datetime

from pydantic import BaseModel


class ParstxtCreate(BaseModel):
    id: int
    datetime: datetime
    title: str
    count_x: int


class Get_Avg_X(BaseModel):
    datetime: str
    title: str
    x_avg_count_in_line: float