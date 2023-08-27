from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import Response, FileResponse
from src.files_handler.schemas import ResponseUploadFiles, ResponseGetFilesInfo, ResponseDelete
import pandas as pd
from src.files_handler.utils import save_file, sorting_values, delete_file
from src.files_handler.utils import filtering_values, file_path_if_exist
import os
import asyncio


router = APIRouter(
    tags=["Files"],
    prefix="/files"
)


@router.post("/upload_files", response_model=ResponseUploadFiles)
async def upload_file(files: list[UploadFile] = File(...)) -> ResponseUploadFiles:
    tasks = []
    wrong_files = []

    for file in files:
        if file.filename.endswith(".csv"):
            task = asyncio.create_task(save_file(file))
            tasks.append(task)
        else:
            wrong_files.append(file.filename)

    await asyncio.gather(*tasks)

    return ResponseUploadFiles(
        uploaded_files=[file.filename for file in files if file.filename not in wrong_files],
        skipped_files_count=len(wrong_files),
        skipped_filenames=wrong_files
    )


@router.get("/get_files_info", response_model=ResponseGetFilesInfo)
def get_files_info() -> ResponseGetFilesInfo:
    file_data = []
    directory = "files"

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        file_data.append({"filename": filename, "columns": columns})

    return ResponseGetFilesInfo(files=file_data)


@router.get("/data/{file}")
async def get_data(
        filename: str,
        filter_values: str = None,
        sort_col: str = None,
        asc_sort: bool = True,
        download_file: bool = False,
        background_tasks: BackgroundTasks = None
):
    try:
        file_path = file_path_if_exist(filename)
        df = pd.read_csv(file_path).copy()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Файл '{filename}' не найден.")

    # Фильтрация
    if filter_values:
        df = filtering_values(filter_values, df)

    # Сортировка
    if sort_col:
        df = sorting_values(sort_col, df, asc_sort)

    # Загрузка файла
    if download_file:
        loaded_file_path = f"files_for_loading/{filename[:-4]}.xlsx"

        writer = pd.ExcelWriter(loaded_file_path)
        df.to_excel(excel_writer=writer, index=False)
        writer._save()
        background_tasks.add_task(delete_file, loaded_file_path)

        return FileResponse(path=loaded_file_path, filename=f"{filename[:-4]}.xlsx",
                            media_type="multipart/form-data")

    data = df.to_csv(index=False)
    return Response(content=data, media_type="text/csv")


@router.delete("/delete/{filename}", response_model=ResponseDelete)
async def del_file(filename: str) -> ResponseDelete:
    try:
        file_path = file_path_if_exist(filename)
        os.remove(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Файл '{filename}' не найден.")

    return ResponseDelete(msg=f"Файл '{filename}' успешно удален.")
