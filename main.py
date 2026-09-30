import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import requests
#pip install opencv-python
import cv2
import pyautogui
from pprint import pprint


engine = pyttsx3.init()
engine.setProperty("rate", 150)
voice = engine.getProperty("voices")
engine.setProperty(voice, voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            cm = r.recognize_google(audio, language="en-US")
            print(f"You said: {cm}\n")
        except:
            print("I didn't understand, please repeat again.\n")
            speak("I didn't understand, please repeat again.")
            return "None"
    return cm


NAME = "None"


def welcome():
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 12:
        print("Hello. good morning.\n")
        speak("Hello. good morning.")
    elif 12 <= hour <= 16:
        print("Hello. good afternoon.\n")
        speak("Hello. good afternoon.")
    else:
        print("Hello. good evening.\n")
        speak("Hello. good evening.")

    print("What is your name?\n")
    speak("What is your name?\n")
    global NAME
    while True:
        NAME = take_command().lower()
        if NAME != "None":
            break

    print(f"Welcome {NAME}. Let's start.\n")
    speak(f"Welcome {NAME}. Let's start.")


welcome()


while True:
    print("how can i help you?\n")
    speak("how can i help you?")
    command = take_command().lower()

    if "bye" or "stop" in command:
        print(f"Goodbye {NAME}.\n")
        speak(f"Goodbye {NAME}.")
        break

    if "wikipedia" in command:
        print("Searching Wikipedia.\n")
        speak("Searching Wikipedia.")
        command = command.replace("wikipedia", "")
        print("How many sentences of the result would you like me to read to you?\n")
        speak("How many sentences of the result would you like me to read to you?")
        try:
            sentences = int(take_command())
        except:
            sentences = 3

        result = wikipedia.summary(command, sentences=sentences)
        print(f"Sentences of your search result in Wikipedia:\n")
        speak(f"Sentences of your search result in Wikipedia:")
        pprint(result+"\n")
        speak(result)

    elif "youtube" in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        print("Opening youtube...\n")
        speak("Opening youtube...")
        time.sleep(5)

    elif "google" in command:
        webbrowser.open_new_tab("https://www.google.com")
        print("Opening google...\n")
        speak("Opening google...")
        time.sleep(5)

    elif "gmail" in command:
        webbrowser.open_new_tab("https://www.gmail.com")
        print("Opening Gmail...\n")
        speak("Opening Gmail...")
        time.sleep(5)

    elif "news" in command:
        webbrowser.open_new_tab("https://www.news.google.com")
        print("Opening news...\n")
        speak("Opening news...")
        time.sleep(5)

    elif "time" in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(str_time+ "\n")
        speak(f"the time is {str_time}")

    elif "camera" or "photo" in command:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        if ret:
            cv2.imwrite("webcam.png", frame)
        camera.release()
        cv2.destroyAllWindows()
        print("Your photo was taken.\n")
        speak("Your photo was taken.")

    elif "screenshot" in command:
        my_screenshot = pyautogui.screenshot()
        my_screenshot.save("screenshot.png")
        print("Your screenshot was taken.\n")
        speak("Your screenshot was taken.")

    elif "search" in command:
        command = command.replace("search", "")
        print(f"Searching {command}...\n")
        speak(f"Searching {command}...")
        webbrowser.open_new_tab(command)
        time.sleep(5)

    elif "question" in command:
        print("Now i can answer your calculation and geography questions.\n")
        speak("Now i can answer your calculation and geography questions.")
        question = take_command()
        app_id = ""
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        print(answer+"\n")
        speak(answer)

    elif "who" or "what are you" in command:
        print("Hello, I am version 1 of the voice assistant and i was programed by Ahmadreza\n")
        speak("Hello, I am version 1 of the voice assistant and i was programed by Ahmadreza")

    elif "who made you" in command:
        print("I was programed by Ahmadreza\n")
        speak("I was programed by Ahmadreza")

    elif "note" in command:
        print(f"What should i write {NAME}?\n")
        speak(f"What should i write {NAME}?")
        note = take_command()
        print(f"{NAME} should i include time?\n")
        speak(f"{NAME} should i include time?")
        ans = take_command()
        if "y" in ans:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            with open("note.txt", "w") as file:
                file.write(str_time + "\n")
                file.write("-" * 40 + "\n")
                file.write(note)
        else:
            with open("note.txt", "w") as file:
                file.write(note)

    elif "show note" in command:
        print("Showing notes:\n")
        speak("Showing notes:")
        with open("note.txt", "r") as file:
            s = file.read()
            print(s + "\n")
            speak(s)

    elif "open telegram" in command:
        print("Opening telegram...\n")
        speak("Opening telegram...")
        os.startfile(r"C:\Users\lenovo\AppData\Roaming\Telegram Desktop\Telegram.exe")

    elif "logout" in command:
        print("Your system will log out in 5 seconds!\n")
        speak("Your system will log out in 5 seconds!")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])

    elif "shutdown" in command:
        print("Your system will shut down in 5 seconds!\n")
        speak("Your system will shut down in 5 seconds!")
        time.sleep(5)
        subprocess.call(["shutdown", "/s"])

    elif "restart" in command:
        print("Your system will restart in 5 seconds!\n")
        speak("Your system will restart in 5 seconds!")
        time.sleep(5)
        subprocess.call(["shutdown", "/r"])

    elif "weather" in command:
        api_key = ""
        base_url = "https://www.api.openweathermap.org/data/2.5/weather?"
        print("What is the city name?\n")
        speak("What is the city name?")
        city_name = take_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        res = response.json()
        if res["cod"] != "404":
            main = res["main"]
            temperature = main["temp"]
            humidity = main["temp"]
            weather = res["temp"]
            weather_description = weather[0]["description"]
            print(f"Temperature in Kelvin unit = {temperature}\n")
            speak(f"Temperature in Kelvin unit= {temperature}")
            print(f"Humidity is = {humidity}\n percentage")
            speak(f"Humidity is = {humidity} percentage")
            print(f"Weather description is = {weather_description}\n")
            speak(f"Weather description is = {weather_description}")