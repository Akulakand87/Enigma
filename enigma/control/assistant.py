import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import pyautogui
import time
import requests
import pywhatkit as kit
import sys
import sys
import json
import os
import datetime
import speech_recognition as sr
import requests, json
model = 'llama2:7b'
context = [] 

def generate(prompt, context, top_k, top_p, temp):
    r = requests.post('http://localhost:11434/api/generate',#set local host ccordingly
                     json={
                         'model': model,
                         'prompt': prompt,
                         'context': context,
                         'options':{
                             'top_k': top_k,
                             'temperature':top_p,
                             'top_p': temp
                         }
                     },
                     stream=False)
    r.raise_for_status()
    response = ""  
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        if 'error' in body:
            raise Exception(body['error'])
        response += response_part
        if body.get('done', False):
            context = body.get('context', [])
            return response, context

def chat(input, chat_history, top_k, top_p, temp):
    chat_history = chat_history or []
    global context
    output, context = generate(input, context, top_k, top_p, temp)
    chat_history.append((input, output))
    return chat_history, chat_history
engine = pyttsx3.init('sapi5')
client = wolframalpha.Client('Your_App_ID')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)

def history(prefix, text):
    history_file = 'history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            # Check if the file is not empty
            if os.stat(history_file).st_size != 0:
                chat_history = json.load(file)
            else:
                chat_history = []
    else:
        chat_history = []

    chat_history.append({prefix: text})

    with open(history_file, 'w') as file:
        json.dump(chat_history, file, indent=4)

def speak(audio):
    history("Enigma said", audio)
    engine.say(audio)
    engine.runAndWait()
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            history("User said", query)
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Enigma"
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')

greetMe()

speak('Hello Sir, I am your digital assistant Enigma')
speak('How may I help you?')


def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))
        history("User said", query)
    history("User said", query)
    return query
        

if __name__ == '__main__':

    while True:
    
        query = myCommand();
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'me' in recipient:
                try:
                    speak('What should I speak? ')
                    content = myCommand()
        
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", 'Your_Password')
                    server.sendmail('Your_Username', "Recipient_Username", content)
                    server.close()
                    speak('Email sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')


        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            sys.exit()
           
        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()
                                    
        elif 'play music' in query:
           # music_folder = Your_music_folder_path
           # music = [music1, music2, music3, music4, music5]
           # random_music = music_folder + random.choice(music) + '.mp3'
           # os.system(random_music)    
            speak('Okay, here is your music! Enjoy!')
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"Sir time is {hour} bajke {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Enigma Quit".lower() in query.lower():
            exit()

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            webbrowser.open("https://studio.youtube.com/channel/UCxeYbp9rU_HuIwVcuHvK0pw/analytics/tab-overview/period-default")
        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"www.youtube.com/results?search_query={query}")
        elif 'open youtube' in query:
            speak("what you will like to watch ?")
            qrry = takeCommand().lower()
            kit.playonyt(f"{qrry}")
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")
        elif 'close youtube' in query:
            os.system("taskkill /f /im msedge.exe")
        elif 'open google' in query:
            speak("what should I search ?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")
            results = wikipedia.summary(qry, sentences=2)
            speak(results)
        elif 'close google' in query:
            os.system("taskkill /f /im msedge.exe")
        elif 'play music' in query:
            music_dir = 'E:\Musics'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))
        elif 'play iron man movie' in query:
            npath = "E:\ironman.mkv"
            os.startfile(npath)
        elif 'close movie' in query:
            os.system("taskkill /f /im vlc.exe")
        elif 'close music' in query:
            os.system("taskkill /f /im vlc.exe")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
        elif "restart the system" in query:
            os.system("shutdown /r /t 5")
        elif "Lock the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif "open notepad" in query:
            npath = "C:\WINDOWS\system32\\notepad.exe"
            os.startfile(npath)
        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")

        elif "go to sleep" in query:
            speak(' alright then, I am switching off')
            sys.exit()
        elif "take screenshot" in query:
            speak('tell me a name for the file')
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("screenshot saved")
        elif "what is my ip address" in query:
            speak("Checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("your ip adress is")
                speak(ipAdd)
            except Exception as e:
                speak("network is weak, please try again some time later")
        elif "volume up" in query:
            pyautogui.press("volumeup",presses = 15)
        elif "volume down" in query:
            pyautogui.press("volumedown",presses = 15)
        elif "mute" in query:
            pyautogui.press("volumemute")
        elif "refresh" in query:
            pyautogui.moveTo(1551,551, 2)
            pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
            pyautogui.moveTo(1620,667, 1)
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
        elif "scroll down" in query:
            pyautogui.scroll(1000)
        elif "drag visual studio to the right" in query:
            pyautogui.moveTo(46, 31, 2)
            pyautogui.dragRel(1857, 31, 2)
        elif "rectangular spiral" in query:
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write('paint')
            time.sleep(1)
            pyautogui.press('enter')
            pyautogui.moveTo(100, 193, 1)
            pyautogui.rightClick()
            pyautogui.click()
            distance = 300
            while distance > 0 :
                pyautogui.dragRel(distance, 0, 0.1, button="left")
                distance = distance - 10
                pyautogui.dragRel(0, distance, 0.1, button="left")
                pyautogui.dragRel(-distance, 0, 0.1, button="left")
                distance = distance - 10
                pyautogui.dragRel(0, -distance, 0.1, button="left")
        elif "close paint" in query:
            os.system("taskkill /f /im mspaint.exe")
        elif "who are you" in query :
            print('My Name Is Enigma')
            speak('My Name Is Enigma')
            print('I can Do Everything that my creator programmed me to do')
            speak('I can Do Everything that my creator programmed me to do')
        elif "who created you" in query :
            print('I Do not Know His Name, I created with Python Language, inVisual Studio Code.')
            speak('I Do not Know His Name, I created with Python Language, inVisual Studio Code.')
        elif 'close chrome' in query :
                    os.system("taskkill /f /im chrome.exe")   

        elif "tell me" in query :
            user_query = query
            chat_history, _ = chat(user_query, [], 5, 0.5, 0.5)
            print(chat_history[-1][1])
            speak(chat_history[-1][1])
        else:
            speak('Pardon me Sir, I did not understand your command!')

        
        speak('Next Command! Sir!')
        

