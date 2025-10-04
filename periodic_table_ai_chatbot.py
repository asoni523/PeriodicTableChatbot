# periodic_table_ai_chatbot.py - Periodic Table AI Chatbot is an interactive 
# voice-enabled assistant that helps users learn about chemical 
# elements in a conversational way.
# 
# Please cite this work if used in projects, research, or publications.
# Author: Anil Kumar Soni
# Created: Aug 18, 2025
# Updated: Sep 04, 2025

import speech_recognition as sr
import pygame
from gtts import gTTS
import tempfile
import os
import openai

# Initialize OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize pygame mixer
pygame.mixer.init()

def speak(text, lang='en'):
    """Speak text using gTTS in chunks (sentence by sentence) via pygame."""
    try:
        # Split text into sentences for faster feedback
        import re
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            if not sentence.strip():
                continue
            tts = gTTS(text=sentence.strip(), lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tmp_path = fp.name
                tts.save(tmp_path)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            # Attempt to remove temp file, silently ignore if still in use
            try:
                os.remove(tmp_path)
            except PermissionError:
                pass
    except Exception as e:
        print(f"TTS Error: {e}")

def ask_openai(question):
    """Query OpenAI GPT for a chemistry answer."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who explains chemistry and elements simply."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return None

# Introduction
intro_text = "Hello! I am your chemistry assistant. Ask me anything about the periodic table or elements."
speak(intro_text)

# Main loop
while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            question = recognizer.recognize_google(audio).lower()
            print(f"You: {question}")

            if "exit" in question or "quit" in question:
                speak("Goodbye! Keep learning chemistry.")
                break

            answer = ask_openai(question)
            if answer:
                print(f"Assistant: {answer}")
                speak(answer)
            else:
                speak("Sorry, I couldn't get an answer. Please try again.")

    except sr.UnknownValueError:
        print("Assistant: Could not understand. Please repeat.")
        speak("I didn't catch that. Could you repeat?")
    except sr.RequestError as e:
        print(f"Assistant: Speech recognition service error: {e}")
        speak("There is an error with the speech recognition service.")
