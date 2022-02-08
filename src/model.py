import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
    DateTime,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@0.0.0.0/atlan"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseMixin(Base):
    __abstract__ = True
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    status = Column(String(50), nullable=False, default="active")
    meta = Column(JSON, nullable=True)


class Forms(BaseMixin):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    published = Column(Integer, nullable=False, default=0)


class FormDefinition(BaseMixin):
    __tablename__ = "form_definition"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, nullable=False)
    question = Column(String, nullable=False)
    published = Column(Integer, nullable=False, default=0)
    form_id = Column(Integer, ForeignKey(Forms.id), nullable=False)


class FormData(BaseMixin):
    __tablename__ = "form_data"

    id = Column(Integer, primary_key=True, index=True)
    form_definition_id = Column(Integer, ForeignKey(FormDefinition.id), nullable=False)
    form_id = Column(Integer, ForeignKey(Forms.id), nullable=False)
    data = Column(JSON, nullable=False)


class Integration(BaseMixin):
    __tablename__ = "integration"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, ForeignKey(FormDefinition.id), nullable=False)
    action = Column(String, nullable=False)


class IntegrationForm(BaseMixin):
    __tablename__ = "integration_form"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey(Forms.id), nullable=False)
    integration_id = Column(Integer, ForeignKey(Integration.id), nullable=False)


class IntegrationEvent(BaseMixin):
    __tablename__ = "integration_event"

    id = Column(Integer, primary_key=True, index=True)
    integration_id = Column(Integer, ForeignKey(Integration.id), nullable=False)
    form_id = Column(Integer, ForeignKey(Forms.id), nullable=False)
    row_id = Column(Integer, ForeignKey(FormData.id), nullable=True)
    data = Column(JSON, nullable=False)
    action_status = Column(String(50), nullable=False, default="pending")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
