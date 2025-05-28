from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    def __init__(self, model_repo_url: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_repo_url)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_repo_url)

    def translate(self, text: str) -> str:
        if not text.strip():
            return "[Texto vacío]"
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model.generate(**inputs, max_length=128)
        translated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated
