from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    s3_prefix: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    source_files: Mapped[list["SourceFileModel"]] = relationship("SourceFileModel", back_populates="project", cascade="all, delete-orphan")
    analysis_jobs: Mapped[list["AnalysisJobModel"]] = relationship("AnalysisJobModel", back_populates="project", cascade="all, delete-orphan")


class SourceFileModel(Base):
    __tablename__ = "source_files"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    language: Mapped[str | None] = mapped_column(String(64), nullable=True)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="source_files")

    __table_args__ = (Index("idx_source_files_project_id", "project_id"),)


class AnalysisJobModel(Base):
    __tablename__ = "analysis_jobs"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped["ProjectModel"] = relationship("ProjectModel", back_populates="analysis_jobs")
    dependency_edges: Mapped[list["DependencyEdgeModel"]] = relationship("DependencyEdgeModel", back_populates="job", cascade="all, delete-orphan")
    business_rules: Mapped[list["BusinessRuleModel"]] = relationship("BusinessRuleModel", back_populates="job", cascade="all, delete-orphan")
    requirements: Mapped[list["RequirementModel"]] = relationship("RequirementModel", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_analysis_jobs_project_id", "project_id"),
        Index("idx_analysis_jobs_status", "status"),
    )


class DependencyEdgeModel(Base):
    __tablename__ = "dependency_edges"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False)
    source_file_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("source_files.id", ondelete="CASCADE"), nullable=False)
    target_file_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("source_files.id", ondelete="CASCADE"), nullable=False)
    dependency_type: Mapped[str] = mapped_column(String(32), nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)

    job: Mapped["AnalysisJobModel"] = relationship("AnalysisJobModel", back_populates="dependency_edges")

    __table_args__ = (Index("idx_dependency_edges_job_id", "job_id"),)


class BusinessRuleModel(Base):
    __tablename__ = "business_rules"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False)
    source_file_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("source_files.id", ondelete="SET NULL"), nullable=True)
    rule_type: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_location: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    job: Mapped["AnalysisJobModel"] = relationship("AnalysisJobModel", back_populates="business_rules")

    __table_args__ = (
        Index("idx_business_rules_job_id", "job_id"),
        Index("idx_business_rules_source_file_id", "source_file_id"),
    )


class RequirementModel(Base):
    __tablename__ = "requirements"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    source_rules: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    job: Mapped["AnalysisJobModel"] = relationship("AnalysisJobModel", back_populates="requirements")

    __table_args__ = (
        Index("idx_requirements_job_id", "job_id"),
        Index("idx_requirements_status", "status"),
    )
