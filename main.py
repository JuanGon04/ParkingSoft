import os
from urllib import request

from fastapi import FastAPI, File, UploadFile,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import reconocimientoPlaca
from starlette.templating import Jinja2Templates

app = FastAPI()


# Ruta para cargar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Crear la carpeta "temp" si no existe
    os.makedirs("temp", exist_ok=True)

    # Guardar el archivo en el sistema de archivos temporalmente
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Llamar a la función ReconocimientoPlaca y pasarle la ruta del archivo
    resultado, Imagen_Marco =  reconocimientoPlaca.ReconocimientoPlaca(file_path)

    # Eliminar el archivo temporal
    os.remove(file_path)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "resultado": resultado,
            "base64_image": Imagen_Marco
        }
    )