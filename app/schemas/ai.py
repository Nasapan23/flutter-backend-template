from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Chat message schema
    """
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """
    Schema for chat completion request
    """
    messages: List[Message]
    model: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, gt=0, le=4096)


class ChatCompletionResponse(BaseModel):
    """
    Schema for chat completion response
    """
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


class ModelInfoResponse(BaseModel):
    """
    Schema for model information
    """
    id: str
    owned_by: str
    created: int 