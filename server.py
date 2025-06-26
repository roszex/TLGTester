from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import uvicorn

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/webapp", StaticFiles(directory="webapp"), name="webapp")

# Специальные обработчики для изображений
@app.get("/webapp/1_page_photo.jpeg")
async def get_image_1():
    response = FileResponse("webapp/1_page_photo.jpeg")
    response.headers["Cache-Control"] = "public, max-age=31536000"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.get("/webapp/2_page_photo.jpeg")
async def get_image_2():
    response = FileResponse("webapp/2_page_photo.jpeg")
    response.headers["Cache-Control"] = "public, max-age=31536000"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Обработчик для корневого пути - перенаправляем на первую страницу
@app.get("/")
async def root():
    return FileResponse("webapp/page_1/index.html")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 