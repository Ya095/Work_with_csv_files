from typing import List
from pydantic import BaseModel


class ResponseUploadFiles(BaseModel):
    uploaded_files: list[str]
    skipped_files_count: int
    skipped_filenames: list[str]


class FilesStructure(BaseModel):
    filename: str
    columns: List[str]


class ResponseGetFilesInfo(BaseModel):
    files: List[FilesStructure]


class RequestGetData(BaseModel):
    filename: str
    filter_values: str = None
    sort_col: str = None
    asc_sort: bool = True
    download_file: bool = False


class ResponseDelete(BaseModel):
    msg: str


class RequestDelete(BaseModel):
    filename: str