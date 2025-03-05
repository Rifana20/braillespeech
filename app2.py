import streamlit as st
import os
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
from streamlit.components.v1 import html

# Title for the app
st.title("🧠 Speech-to-Braille Converter")
st.write("Convert your speech or text into Braille.")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f5f3e7;
        color: #4b3f2f;
        font-family: 'Helvetica', sans-serif;
    }
    .main .block-container {
        background-color: #f5f3e7;
    }
    .stButton>button {
        background-color: #d2b48c;
        color: #fff;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Simple JavaScript to capture speech from the browser and send it to the Streamlit backend
speech_recognition_js = """
<script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    function startRecording() {
        recognition.start();
        document.getElementById('status').innerText = 'Listening...';
    }

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        window.parent.postMessage({type: 'speech', text: transcript}, '*');
    }

    recognition.onerror = function(event) {
        document.getElementById('status').innerText = 'Error occurred: ' + event.error;
    }
</script>
<button onclick="startRecording()">Start Recording</button>
<p id="status"></p>
"""

# Display the JavaScript component to capture speech
html(speech_recognition_js)

# Process the speech after capturing it
st.write("Recognized text will appear here:")
input_text = st.text_input("Recognized Text")

# Process the input text with Braille conversion
braille_dict = {
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100',
    'f': '111000', 'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100',
    'k': '100010', 'l': '101010', 'm': '110010', 'n': '110110', 'o': '100110',
    'p': '111010', 'q': '111110', 'r': '101110', 's': '011010', 't': '011110',
    'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011', 'y': '110111',
    'z': '100111', ' ': '000000'
}

unicode_braille_map = {
    '100000': '⠁', '101000': '⠃', '110000': '⠉', '110100': '⠙', '100100': '⠑',
    '111000': '⠋', '111100': '⠛', '101100': '⠓', '011000': '⠊', '011100': '⠚',
    '100010': '⠅', '101010': '⠇', '110010': '⠍', '110110': '⠝', '100110': '⠕',
    '111010': '⠏', '111110': '⠟', '101110': '⠗', '011010': '⠎', '011110': '⠧',
    '100011': '⠥', '101011': '⠧', '011101': '⠺', '110011': '⠭', '110111': '⠽',
    '100111': '⠵', '000000': '⠠'
}

def convert_to_braille_unicode(text):
    text = text.lower()
    braille_output = []
    
    for char in text:
        if char in braille_dict:
            braille_output.append(unicode_braille_map[braille_dict[char]])
        else:
            braille_output.append('⠿')  # Unknown character
    
    return ''.join(braille_output)

# Display the result
if input_text:
    braille_unicode = convert_to_braille_unicode(input_text)
    st.subheader("🔤 Original Text")
    st.write(input_text)
    st.subheader("🟤 Braille Representation")
    st.write(braille_unicode)

    # Text-to-speech using gTTS
    tts = gTTS(text=input_text, lang='en')
    audio_file = "output.mp3"
    tts.save(audio_file)
    st.audio(audio_file, format="audio/mp3")
    os.remove(audio_file)  # Clean up the saved audio file
