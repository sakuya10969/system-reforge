import io
import zipfile
from dataclasses import dataclass

from app.domain.exceptions import EmptyZipFileError, InvalidZipFileError

LANGUAGE_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".java": "java",
    ".kt": "kotlin",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".php": "php",
    ".swift": "swift",
    ".scala": "scala",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "shell",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".xml": "xml",
    ".md": "markdown",
}


@dataclass
class ExtractedFile:
    file_path: str
    content: bytes
    language: str | None


def detect_language(file_path: str) -> str | None:
    suffix = "." + file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    return LANGUAGE_MAP.get(suffix)


def is_excluded_entry(name: str) -> bool:
    parts = name.split("/")
    for part in parts:
        if part.startswith(".") or part in {"__MACOSX", "__pycache__", "node_modules"}:
            return True
    return name.endswith("/")


def extract_zip(data: bytes) -> list[ExtractedFile]:
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as e:
        raise InvalidZipFileError(str(e)) from e

    entries = [
        entry for entry in zf.infolist()
        if not is_excluded_entry(entry.filename)
    ]

    if not entries:
        raise EmptyZipFileError("ZIP contains no processable files")

    result: list[ExtractedFile] = []
    for entry in entries:
        content = zf.read(entry.filename)
        result.append(ExtractedFile(
            file_path=entry.filename,
            content=content,
            language=detect_language(entry.filename),
        ))
    return result
