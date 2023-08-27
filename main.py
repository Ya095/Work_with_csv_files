from fastapi import FastAPI
from src.files_handler.api_handlers import router as file_router


app = FastAPI(
    title="Work with files (.csv)"
)

app.include_router(file_router)