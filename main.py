import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from google import genai


recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):

    client = genai.Client(api_key="gemini-api-key")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{command} (give rich and short response)",
    )
    cleaned_text = response.text.replace('**', '').replace('*', '')
    return cleaned_text


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing ALfred....")
    while True:

        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "alfred"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Alfred Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error: ".format(e))