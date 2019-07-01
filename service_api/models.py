import uuid

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String)
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

ReportStatus = Table(
    "report_status", metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('task_id', UUID(as_uuid=True), nullable=False),
    Column('status', String, nullable=False),
    Column('report_type', String, nullable=False),
    Column('file_name', String, default=None),
)
