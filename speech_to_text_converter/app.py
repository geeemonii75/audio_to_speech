import os
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Process the audio file from the POST request
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'})

    # Save the audio file to a temporary location
    audio_path = os.path.join('tmp', audio_file.filename)
    audio_file.save(audio_path)

    # Perform speech-to-text conversion using SpeechRecognition
    text = recognize_speech(audio_path)

    return jsonify({'text': text})

def recognize_speech(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    # Perform speech recognition
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Speech recognition could not understand the audio."
    except sr.RequestError as e:
        text = f"Error occurred during speech recognition: {e}"

    return text

if __name__ == '__main__':
    app.run(debug=True)