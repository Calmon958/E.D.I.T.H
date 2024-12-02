
import tkinter as tkinter
from tkinter import scrolledtext
import pyttsx3
import SpeechRecogintion as sr
from vosk import Model, KaldiRecognizer
import os
import json
import threading


#initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 130)  #Speed is adjustable
engine.setProperty('voice', 'english') #Modify voice properties


def speak(text):
    #Convert text to speech
    engine.say(text)
    engine.runAndWait()

    #initialize Vosk Model
    model_path = "/home/tails/vosk-model-small-en-us-0.15"  #path to where the model is
    if not os.path.exsist(model_path):
        print(f"Model path {model_path} does not exsist")
        exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    def recognize_speech():
        """Recognize speech from microphone"""
        recognizer_instance = sr.Recognizer()
        with sr.Microphone() as source:
            log_message("Listenning for voice commands...")
            audio = recognizer_instance.listen(source)

            #Use vork for offline recognition
            if recognizer.AcceptWaveForm(audio.get_wav_data()):
                result = json.loads(recognizer.Result())
                return result.get("text", "")
        return ""

def handle_voice_command():
    """Handle voice commands in a thread"""
    while True:
        command = recognize_speech()
        if commnd:
            log_message(f"You said: {command}")
            process_command(command)

def process_command():
    """Processes recognoxed or manually entered command"""
    if "exit" in command or "quit" in command:
        log_message("Login out... See you later Sir")
        speak("See you next time Sir")
        root.destroy() #for closing the GUI
    elif "hello" in command:
        response = "Hello Sir, what do you have for me today?"
        log_message(response)
        speak(response)
    else:
            response = "I didn't quite catch that. Could you repeat?"
            log_message(response)
            speak(response)


def log_message():
    """Logs a message to the GUI log box"""
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, f"{message}\n")
    log_box.config(state=tk.DISABLED)
    log_box.see(tk.END)


def manual_command_handler():
    """Handles manual input commands"""
    command = manual_input.get()
    manual_input.delete(0, tk.END)
    log_message(f"Manual input: {command}")
    process_command(command)

def start_voice_thread():
    """Starts separate thread fo voice recognition"""
    voice_thread = threading.Thread(target=handle_voice_command, daemon=True)
    voice_thread.start()

#Build GUI
root = tk.Tk()
root.title("EDITH PA")


#Create a scrollable text box for logs
log_box = scrolledtext.ScrolledText(root, width=50, height=20, state=tk.DISABLED)
log_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

#Create an entry box for manual input
manual_input = tk.Entry(root, width=40)
manual_input.grid(row=1, column =0, padx=10, pady=5)

#Create buttons
send_button = tk.Button(root, text="Send Command", command=manual_command_handler)