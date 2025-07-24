from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    cases: list = []

class CaseBase(BaseModel):
    case_name: str
    case_number: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    court_date: Optional[datetime] = None
    assigned_lawyer: Optional[str] = None

class CaseCreate(CaseBase):
    client_id: int

class CaseUpdate(CaseBase):
    pass

class Case(CaseBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime
    documents: list = []
    tasks: list = []

class DocumentBase(BaseModel):
    file_name: str
    file_path: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    case_id: int

class Document(DocumentBase):
    id: int
    case_id: int
    uploaded_at: datetime

class TaskBase(BaseModel):
    description: str
    due_date: Optional[datetime] = None
    completed: Optional[bool] = False
    assigned_to: Optional[str] = None

class TaskCreate(TaskBase):
    case_id: int

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    case_id: int
    created_at: datetime
    updated_at: datetime
