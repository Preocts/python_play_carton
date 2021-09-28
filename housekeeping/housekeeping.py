"""
Uttiliy for file management
"""
import gzip
import os
from pathlib import Path
from datetime import datetime
from datetime import timedelta


def delete_after_days(directory: str, glob_pattern: str, retain_for_days: int) -> None:
    """Deletes matching files older than retention period, unrecoverable!"""
    expiry = datetime.now() - timedelta(days=retain_for_days)
    filepath = Path(directory)
    for file in filepath.glob(glob_pattern):
        created = datetime.fromtimestamp(os.path.getctime(file))
        if expiry > created:
            os.remove(file)


def gzip_archive(directory: str, glob_pattern: str) -> None:
    """GZip files, deletes, and places results in nested '/archive' subdirectory"""
    filepath = Path(directory)
    archivepath = Path(directory) / "archive"
    files = [file for file in filepath.glob(glob_pattern) if file.is_file()]
    if not files:
        return None

    archivepath.mkdir(parents=True, exist_ok=True)

    for file in files:
        with gzip.open(archivepath / f"{file.name}.gzip", mode="wb") as archive:
            with file.open(mode="rb") as infile:
                archive.write(infile.read())
