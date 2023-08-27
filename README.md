# Work with files (.csv)

<h3>Запуск приложения</h3>
Для запуска приложения через Docker нужно ввести следующие команды:

```
1) docker build . -t fast_api_app:latest 
2) docker run -d -p 7373:8000 --name fast_api_excel fast_api_app
```

После этого перейти по url: http://127.0.0.1:7373/docs

<h3>Описание работы api</h3>  

1) >"/files/upload_files"
   
Описание: позволяет загрузить один или несколько файлов, с расширением ```.csv``` (файлы с другим расширением 
   загружены не будут).  
Загруженные файлы сохраняются в папку "files" проекта.

2) >"/files/get_files_info"

Описание работы: получение информации обо всех загруженных файлах и названия их колонок.  

3) >"/files/data/{files}"
   
Описание: получение данные из конкретного файла с опциональными фильтрацией и 
   сортировкой по одному или нескольким столбцам.  
Описание параметров:
- ``` filename``` [обязательный параметр] - имя файла, например: file1.csv
- ``` filter_values``` - фильтрация по столбцам. Пример ввода данных: year=2011, class=A.  
Можно вводить 1 или несколько параметров. Есть следующие варианты фильтрации:  
  - =
  - !=
  - \>=
  - <=
  - \>
  - <
- ``` sort_col ``` - колонки по которым можно сортировать. Можно сортировать по 1 или нескольким колонкам. Пример 
  ввода: year, date
- ``` asc_sort ``` - сортировка по возрастанию - True, по убыванию - False. Если заданы колонки для сортировки.
- ``` download_file``` - возможность скачать итоговый файл (с уже примененными фильтрацией и сортировкой).  
Файл удаляется с сервера после скачивания.

4) >"/files/delete/{filename}"

Описание: удаление файла по названию. Пример передачи данных: file1.csv
