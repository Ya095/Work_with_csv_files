import pandas as pd
from fastapi import UploadFile, HTTPException
import os


# Сохранение файлов в директорию
async def save_file(file: UploadFile) -> None:
    with open(f"files/{file.filename}", "wb") as f:
        contents = await file.read()
        f.write(contents)


# Вернет путь к файлу, если он существует
def file_path_if_exist(filename: str) -> str:
    directory = "files"
    file_path = os.path.join(directory, filename)

    return file_path


# Фильтрация
def filtering_values(string_values: str, df: pd.DataFrame) -> pd.DataFrame:
    string_values.strip()

    def is_number(val):
        val.strip()
        try:
            val = float(val)
        except ValueError:
            pass
        return val

    try:
        arr_of_values = [num.strip() for num in string_values.split(",")]
        for value in arr_of_values:
            if "!=" in value:
                col, val = value.split("!=")
                val = is_number(val)
                df = df[df[col] != val]
            elif ">=" in value:
                col, val = value.split(">=")
                val = is_number(val)
                df = df[df[col] >= val]
            elif "<=" in value:
                col, val = value.split("<=")
                val = is_number(val)
                df = df[df[col] <= val]
            elif "=" in value:
                col, val = value.split("=")
                val = is_number(val)
                df = df[df[col] == val]
            elif ">" in value:
                col, val = value.split(">")
                val = is_number(val)
                df = df[df[col] > val]
            elif "<" in value:
                col, val = value.split("<")
                val = is_number(val)
                df = df[df[col] < val]

    except KeyError as err:
        raise HTTPException(status_code=404, detail=f"Не найдена колонка {err} в файле для фильтрации.")

    return df


# Сортировка
def sorting_values(sort_col: str, df: pd.DataFrame, asc_sort: bool) -> pd.DataFrame:
    sort_col = sort_col.strip()
    try:
        arr_of_values = [num.strip() for num in sort_col.split(",")]
        df = df.sort_values(arr_of_values, ascending=asc_sort)
    except KeyError as err:
        raise HTTPException(status_code=404, detail=f"Не найдена колонка {err} в файле для сортировки.")

    return df


# Удаление файла после передачи пользователю для скачивания
def delete_file(file_for_del_path: str) -> None:
    if os.path.exists(file_for_del_path):
        os.remove(file_for_del_path)
