# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.translate import Translator
from gtts import gTTS
import os

# Crear instancia de FastAPI
app = FastAPI(title="Traductor Quechua ↔ Español")

# Cargar modelos
es_qu_translator = Translator("app/model_es_qu")
qu_es_translator = Translator("app/model_qu_es")

# Esquema de entrada
class TranslationRequest(BaseModel):
    text: str

# Endpoints de traducción
@app.post("/traducir-es-qu")
def traducir_es_qu(data: TranslationRequest):
    result = es_qu_translator.translate(data.text)
    return {"origen": "español", "destino": "quechua", "traduccion": result}

@app.post("/traducir-qu-es")
def traducir_qu_es(data: TranslationRequest):
    result = qu_es_translator.translate(data.text)
    return {"origen": "quechua", "destino": "español", "traduccion": result}

# Ruta a la carpeta estática
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Establecer index.html como página raíz
@app.get("/")
def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html no encontrado"}

# Voz humanizada: generar el archivo
@app.post("/voz")
def sintetizar_voz(data: TranslationRequest):
    tts = gTTS(text=data.text, lang='es')
    tts.save("voz.mp3")
    return {"msg": "ok"}

# Voz humanizada: servir el audio
@app.get("/voz.mp3")
def servir_audio():
    return FileResponse("voz.mp3", media_type="audio/mpeg")