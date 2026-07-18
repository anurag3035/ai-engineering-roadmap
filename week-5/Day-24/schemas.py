from typing import Any, Dict, Optional

from pydantic import BaseModel


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]


class ToolResponse(BaseModel):
    tool_name: str
    result: str


class AgentResponse(BaseModel):
    user_query: str
    tool_used: Optional[str] = None
    final_response: str