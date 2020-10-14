from pydantic import BaseModel


class Health(BaseModel):
    health: bool


class PushMessage(BaseModel):
    message: str


class SendMessage(BaseModel):
    channel: str
    message: str


class SentReport(BaseModel):
    sent: int
    fail: int
