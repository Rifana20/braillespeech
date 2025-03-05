import streamlit as st
from gtts import gTTS
from speech_recognition import Recognizer
import sounddevice as sd
import numpy as np
import io
import os

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

# Braille dictionary
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

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"

# Function to record audio using sounddevice
def record_audio(duration=5, samplerate=44100):
    st.write("Listening...")
    # Record audio for 5 seconds
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return audio_data

st.title("🧠 Speech-to-Braille Converter")
st.write("Convert your speech or text into Braille.")

option = st.radio("Choose an option:", ["Enter text manually", "Use speech input"])

input_text = ""

if option == "Enter text manually":
    input_text = st.text_input("Enter your text:")
elif option == "Use speech input":
    if st.button("🎙️ Start Recording"):
        audio_data = record_audio()  # Record using sounddevice
        recognizer = Recognizer()
        audio = recognizer.record(audio_data, duration=5)  # Use recorded audio data for recognition
        try:
            input_text = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {input_text}")
        except Exception as e:
            st.error(f"Error: {e}")

if input_text:
    braille_unicode = convert_to_braille_unicode(input_text)
    st.subheader("🔤 Original Text")
    st.write(input_text)
    st.subheader("🟤 Braille Representation")
    st.write(braille_unicode)

    audio_file = text_to_speech(input_text)
    with open(audio_file, "rb") as audio:
        st.audio(audio.read(), format="audio/mp3")
    os.remove(audio_file)
