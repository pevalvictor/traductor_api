# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from app.translate import Translator
import os

# Instanciar FastAPI
app = FastAPI(title="Traductor Quechua ↔ Español")

# Cargar modelos directamente desde Hugging Face
es_qu_translator = Translator("VICTORPEVAL25/modelo-es-qu")
qu_es_translator = Translator("VICTORPEVAL25/modelo-qu-es")

# Modelo para entrada
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

# Sintetizador de voz (usando gTTS)
@app.post("/voz")
def sintetizar_voz(data: TranslationRequest):
    tts = gTTS(text=data.text, lang="es")
    tts.save("voz.mp3")
    return {"mensaje": "Voz generada correctamente"}

@app.get("/voz.mp3")
def servir_audio():
    return FileResponse("voz.mp3", media_type="audio/mpeg")

# Montar archivos estáticos (JS, HTML, etc.)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Página principal
@app.get("/")
def root():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path) if os.path.exists(index_path) else {"error": "Archivo index.html no encontrado"}
