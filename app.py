import streamlit as st
import nltk
from gtts import gTTS
from speech_recognition import Recognizer, AudioData
import io
import os

# Download the necessary NLTK data for tokenization
nltk.download('punkt')

# Braille and punctuation mappings
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

punctuation_unicode_map = {
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒', '"': '⠶',
    "'": '⠄', '(': '⠷', ')': '⠾', '-': '⠤'
}

def convert_to_braille_unicode(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    braille_output = []
    for token in tokens:
        for char in token:
            if char in braille_dict:
                braille_output.append(unicode_braille_map[braille_dict[char]])
            elif char in punctuation_unicode_map:
                braille_output.append(punctuation_unicode_map[char])
            elif char.isdigit():
                braille_output.append('⠴')
                braille_output.append(unicode_braille_map[braille_dict[char]])
            elif char == ' ':
                braille_output.append('⠠')
            else:
                braille_output.append('⠿')
    return ''.join(braille_output)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    return "output.mp3"

# Function to process uploaded audio file
def process_audio(uploaded_file):
    recognizer = Recognizer()
    audio_data = AudioData(uploaded_file.read(), 16000, 2)  # 16000 Hz, 2 bytes per sample
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        return None

st.title("🧠 Speech-to-Braille Converter")
st.write("Convert your speech or text into Braille with an elegant cream-brown interface.")

option = st.radio("Choose an option:", ["Enter text manually", "Use speech input"])

input_text = ""

if option == "Enter text manually":
    input_text = st.text_input("Enter your text:")
elif option == "Use speech input":
    uploaded_audio = st.file_uploader("Upload your audio file (WAV or MP3)", type=["wav", "mp3"])
    if uploaded_audio is not None:
        input_text = process_audio(uploaded_audio)
        if input_text:
            st.success(f"Recognized Text: {input_text}")
        else:
            st.error("Sorry, could not recognize the speech.")

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

