import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from tkinter import *
from tkinter import ttk

# Initialize translator 
translator = Translator()

# List of all languages sorted by their names
language_names = sorted(LANGUAGES.values())

# Function to get language code from language name
def get_language_code(lang_name):
    for code, name in LANGUAGES.items():
        if name.lower() == lang_name.lower():
            return code
    return "en"  # fallback to English if not found

# Function to capture speech input and return as text
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source)
        try:
            speech_text = recognizer.recognize_google(audio)
            print(f"You said: {speech_text}")
            src_text.delete("1.0", END)  # Clear previous input
            src_text.insert(END, speech_text)
        except Exception as e:
            print(f"Sorry, could not understand. {e}")
            src_text.delete("1.0", END)
            src_text.insert(END, "Could not understand speech.")

# Function to convert text to speech
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("translated_audio.mp3")
    os.system("start translated_audio.mp3")

# Function to translate the input text
def translate_text():
    try:
        input_text = src_text.get("1.0", END).strip()
        from_lang_code = get_language_code(src_lang.get())
        to_lang_code = get_language_code(dest_lang.get())

        translated = translator.translate(input_text, src=from_lang_code, dest=to_lang_code)
        dest_text.delete("1.0", END)
        dest_text.insert(END, translated.text)

        # Speak the translated text
        speak_text(translated.text)

    except Exception as e:
        dest_text.delete("1.0", END)
        dest_text.insert(END, f"Error: {str(e)}")

# Create main window
root = Tk()
root.title("AI Translator for Travelers")
root.geometry("800x600")
root.config(bg='#f0f0ff')

# --- Title Heading ---
Label(root, text="AI Translator for Travelers", font=("Segoe UI", 24, "bold"), bg="#f0f0ff", fg="#2f4f4f").pack(pady=15)

# --- Language Selection Frame ---
frame_lang = Frame(root, bg='#f0f0ff')
frame_lang.pack(pady=10)

# --- Source Language Combo ---
Label(frame_lang, text="From:", font=("Segoe UI", 12), bg="#f0f0ff").grid(row=0, column=0, padx=10)
src_lang = ttk.Combobox(frame_lang, values=language_names, width=25)
src_lang.set("english")
src_lang.grid(row=0, column=1)

# --- Target Language Combo ---
Label(frame_lang, text="To:", font=("Segoe UI", 12), bg="#f0f0ff").grid(row=0, column=2, padx=10)
dest_lang = ttk.Combobox(frame_lang, values=language_names, width=25)
dest_lang.set("hindi")
dest_lang.grid(row=0, column=3)

# --- Source Text ---
Label(root, text="Enter Text or Speak:", font=("Segoe UI", 12, "bold"), bg="#f0f0ff").pack(pady=(20, 5))
src_text = Text(root, font=("Segoe UI", 12), height=6, width=90, wrap=WORD, bd=2, relief=GROOVE)
src_text.pack()

# --- Speak Button for Speech Input ---
Button(root, text="Speak Input", font=("Segoe UI", 12, "bold"), bg="#4682b4", fg="white", width=20, command=listen_speech).pack(pady=10)

# --- Translate Button ---
Button(root, text="Translate", font=("Segoe UI", 12, "bold"), bg="#4682b4", fg="white",
       width=20, command=translate_text).pack(pady=20)

# --- Translated Text Output ---
Label(root, text="Translated Output:", font=("Segoe UI", 12, "bold"), bg="#f0f0ff").pack(pady=(10, 5))
dest_text = Text(root, font=("Segoe UI", 12), height=6, width=90, wrap=WORD, bd=2, relief=GROOVE)
dest_text.pack()

root.mainloop()
