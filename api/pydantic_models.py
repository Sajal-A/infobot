from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

class ModelName(str,Enum):
    GPT_4o = "gpt-4o"
    GPT_4o_MINI = "gpt-4o-mini" 

class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT_4o_MINI)

class QueryResponse(BaseModel):
    answer: str
    session_id: Optional[str]
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
