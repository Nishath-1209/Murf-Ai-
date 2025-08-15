from pydantic import BaseModel


class LLMRequest(BaseModel):
    message: str


class LLMResponse(BaseModel):
    reply: str
