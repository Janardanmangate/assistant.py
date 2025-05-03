import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import webbrowser
import datetime
import os

# Initialize the pyttsx3 engine (for text-to-speech)
engine = pyttsx3.init()

# Function to speak to the user
def speak(text):
    print(f"Assistant: {text}")  # Print to console for debugging
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")  # Debugging message
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")  # Debugging message
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")  # Debugging message
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the speech service.")
        return None

# Function to tell the current time
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to open a website
def open_website(website):
    webbrowser.open(f"https://{website}")
    speak(f"Opening {website} for you.")

# Function to search on Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Could you be more specific? I found multiple results: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("Sorry, I couldn't reach Wikipedia. Please check your internet connection.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find anything on Wikipedia for that topic.")

# Function to handle shutdown
def shutdown_system():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

# Main function to run the assistant
def main():
    speak("Hello, I am your assistant. How can I help you today?")
    while True:
        command = listen()

        if command is None:
            continue

        if "time" in command:
            tell_time()
        elif "joke" in command:
            tell_joke()
        elif "open" in command:
            website = command.split("open ")[1]
            open_website(website)
        elif "search" in command:
            query = command.split("search for ")[1]
            search_wikipedia(query)
        elif "shutdown" in command:
            shutdown_system()
            break
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Assistant shutting down.")
        print("Assistant shutting down.")  # For debugging
