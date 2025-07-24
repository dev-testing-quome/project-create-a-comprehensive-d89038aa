import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
    address = Column(String(255))
    cases = relationship("Case", back_populates="client")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    case_name = Column(String(255), nullable=False)
    case_number = Column(String(50))
    description = Column(Text)
    status = Column(String(50))
    court_date = Column(DateTime)
    assigned_lawyer = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    client = relationship("Client", back_populates="cases")
    documents = relationship("Document", back_populates="case")
    tasks = relationship("Task", back_populates="case")


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    description = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    case = relationship("Case", back_populates="documents")


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    description = Column(Text, nullable=False)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    assigned_to = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    case = relationship("Case", back_populates="tasks")
