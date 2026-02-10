from pydantic import BaseModel
from datetime import datetime


class MessageOut(BaseModel):
    id: int
    user_id: int
    text: str
    emotion: str
    created_at: datetime
