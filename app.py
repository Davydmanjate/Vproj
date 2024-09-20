from flask import Flask, request, render_template, send_file
import pdfplumber
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Função para extrair texto de um arquivo PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Função para traduzir o texto
def translate_text(text, dest_language):
    translator = Translator()  # Removido o timeout
    translated = translator.translate(text, dest=dest_language)
    return translated.text

# Função para converter texto em fala (TTS)
def text_to_speech(text, language, output_file):
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)

# Rota principal para carregar o documento
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        language = request.form['language']
        
        if file:
            file_path = os.path.join('uploaded.pdf')
            file.save(file_path)
            
            # Extrair texto do PDF
            text = extract_text_from_pdf(file_path)
            
            # Traduzir texto
            translated_text = translate_text(text, language)
            
            # Gerar áudio do texto traduzido
            audio_file = 'translated.mp3'
            text_to_speech(translated_text, language, audio_file)
            
            # Remover o arquivo PDF após a extração do texto (opcional)
            os.remove(file_path)
            
            # Enviar o arquivo de áudio para download
            return send_file(audio_file, as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
