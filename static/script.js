const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
const synth = window.speechSynthesis;

document.getElementById('micButton').addEventListener('click', () => {
  const idioma = document.getElementById('idioma').value;

  recognition.lang = idioma === 'es_qu' ? 'es-PE' : 'qu-PE';

  const langSupported = ['es-PE'];
  if (!langSupported.includes(recognition.lang)) {
    alert("Idioma no soportado por reconocimiento de voz. Se usará español como fallback.");
    recognition.lang = 'es-PE';
  }

  recognition.start();
  document.getElementById('status').textContent = '🎤 Escuchando...';
});

recognition.onresult = (event) => {
  const text = event.results[0][0].transcript;
  document.getElementById('inputText').textContent = text;
  traducir(text);
};

recognition.onerror = (event) => {
  document.getElementById('status').textContent = '❌ Error en reconocimiento de voz: ' + event.error;
};

async function traducir(text) {
  const idioma = document.getElementById('idioma').value;
  const ruta = idioma === 'es_qu' ? '/traducir-es-qu' : '/traducir-qu-es';

  try {
    const response = await fetch(ruta, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error('Error en la respuesta del servidor');

    const data = await response.json();
    document.getElementById('outputText').textContent = data.traduccion;
    document.getElementById('status').textContent = '✅ Traducción realizada con éxito';

    // Requiere POST para generar voz y GET para reproducir
    await fetch("/voz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: data.traduccion })
    });
    const audio = new Audio("/voz.mp3");
    audio.play();

  } catch (error) {
    console.error(error);
    document.getElementById('status').textContent = '❌ Error: no se pudo traducir';
  }
}






