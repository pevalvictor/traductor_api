
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    def __init__(self, repo_id: str):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(repo_id)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(repo_id)
        except Exception as e:
            raise RuntimeError(f"No se pudo cargar el modelo desde Hugging Face ({repo_id}): {e}")

    def translate(self, text: str) -> str:
        if not text.strip():
            return "[Texto vacío]"
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model.generate(**inputs, max_length=128)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
