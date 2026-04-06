from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.domain.exceptions import (
    AnalysisJobNotFoundError,
    EmptyZipFileError,
    InvalidStatusTransitionError,
    InvalidZipFileError,
    NoSourceFilesError,
    ProjectNotFoundError,
    RequirementNotFoundError,
)


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


async def project_not_found_handler(request: Request, exc: ProjectNotFoundError) -> JSONResponse:
    return _error_response(404, "NOT_FOUND", str(exc))


async def analysis_job_not_found_handler(request: Request, exc: AnalysisJobNotFoundError) -> JSONResponse:
    return _error_response(404, "NOT_FOUND", str(exc))


async def requirement_not_found_handler(request: Request, exc: RequirementNotFoundError) -> JSONResponse:
    return _error_response(404, "NOT_FOUND", str(exc))


async def invalid_zip_handler(request: Request, exc: InvalidZipFileError) -> JSONResponse:
    return _error_response(422, "INVALID_ZIP", str(exc))


async def empty_zip_handler(request: Request, exc: EmptyZipFileError) -> JSONResponse:
    return _error_response(422, "EMPTY_ZIP", str(exc))


async def no_source_files_handler(request: Request, exc: NoSourceFilesError) -> JSONResponse:
    return _error_response(422, "NO_SOURCE_FILES", str(exc))


async def invalid_status_transition_handler(request: Request, exc: InvalidStatusTransitionError) -> JSONResponse:
    return _error_response(422, "INVALID_STATUS_TRANSITION", str(exc))


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return _error_response(422, "VALIDATION_ERROR", str(exc))


def register_error_handlers(app) -> None:
    app.add_exception_handler(ProjectNotFoundError, project_not_found_handler)
    app.add_exception_handler(AnalysisJobNotFoundError, analysis_job_not_found_handler)
    app.add_exception_handler(RequirementNotFoundError, requirement_not_found_handler)
    app.add_exception_handler(InvalidZipFileError, invalid_zip_handler)
    app.add_exception_handler(EmptyZipFileError, empty_zip_handler)
    app.add_exception_handler(NoSourceFilesError, no_source_files_handler)
    app.add_exception_handler(InvalidStatusTransitionError, invalid_status_transition_handler)
    app.add_exception_handler(ValueError, value_error_handler)
