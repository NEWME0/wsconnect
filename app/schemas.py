from pydantic import BaseModel


__all__ = ['Health', 'PushMessage', 'SendMessage', 'SentReport']


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
