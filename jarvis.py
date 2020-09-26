import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os         # system control 
import smtplib    # send mail
import pyautogui  # screenshot
import psutil     # control cpu
import pyjokes

engin = pyttsx3.init('sapi5')
voices = engin.getProperty('voices')
engin.setProperty('voice', voices[1].id)  # voice of a girl

# speak
def speak(audio):
    engin.say(audio)
    engin.runAndWait()  # Without this command, speech will not be audible to us.

# according to time wish you
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Moring!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")  
    speak("I am Elsa Mam, Please tell me how can I help you") 

# take command that you speak and return it string
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.
    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

# send email on your required email
def sendEmail(to, content):
    """
    Do not forget to 'enable the less secure apps' feature in your Gmail account.
    Otherwise, the sendEmail function will not work properly.
    """
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()  # connect to server of gmail
    server.starttls()  # to provide you secuirty
    server.login('youremail@gmail.com', 'your-password') # set your email and password its demo
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'how are you' in query:
            speak("I am Fine Mam")
        # Logic for executing tasks based on query
        elif 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        # youtube
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        # google
        elif 'open google' in query:
            webbrowser.open("google.com")
        # search chrome
        elif 'open chrome' in query:
            speak("What do you want to search!")
            search = takeCommand()
            path_of_chrome = 'Google Chrome.lnk %s'
            webbrowser.get(path_of_chrome).open_new_tab(search+'.com')
        # stack overflow
        elif 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        # play music
        elif 'play music' in query:
            music_dir = 'Video'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
        # sing song
        elif 'sing song' in query:
            speak('ok Mam')
            song = open('song.txt', 'r').read()
            speak(song)
        # time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        # open VS code
        elif 'open code' in query:
            codePath = "Visual Studio Code.lnk"
            os.startfile(codePath)
        # email
        elif 'email to someone' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "youremail@gmail.com"   # send email  
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")
        # save a remind in jarvis
        elif 'write down' in query:
            speak('What should i write down Mam!')
            note = takeCommand()
            remember = open('save_remind.txt', 'w')
            remember.write(note)
            remember.close()
            speak('Its done Mam'+ note)
        # ask jarvis to if save a remind
        elif 'anything you save' in query:
            try:
                reminder = open('save_remind.txt', 'r').read()
                speak('Yes Mam, You told me to remember that' + reminder)
            except Exception as e:
                print(e)
                speak('None Mam')
        # shut down system
        elif 'shutdown' in query:
            try:
                speak('Mam you realy want to shut down')
                ins = takeCommand()
                if ins == 'yes':
                    os.system('shutdown /s /t 1')
                else:
                    break
            except Exception as e:
                speak('Again speak mam')
        # restart system
        elif 'restart' in query:
            try:
                speak('Mam you realy want to restart')
                ins = takeCommand()
                if ins == 'yes':
                    os.system('shutdown /r /t 1')
                else:
                    break
            except Exception as e:
                speak('Again speak mam')
        # logout system
        elif 'logout' in query:
            try:
                speak('Mam you realy want to logout')
                ins = takeCommand()
                if ins == 'yes':
                    os.system('shutdown -1')
                else:
                    break
            except Exception as e:
                speak('Again speak mam')
        # take screen shot
        elif 'screenshot' in query:
            img = pyautogui.screenshot()
            img.save('jarvis.png')
            speak('Its done Mam')
        # check bettery status
        elif 'status bettery' in query:
            cpu = str(psutil.cpu_percent())
            print(cpu)
            speak(f"you have use {cpu} of cpu")
            bettery = psutil.sensors_battery().percent
            print(bettery)
            speak(f"you have use {bettery} of bettery")
        # listen joke
        elif 'joke' in query:
            tell_joke = pyjokes.get_joke()
            print(tell_joke)
            speak(tell_joke)
        # quit program
        elif 'exit' in query:
            speak('Ok Mam! Good Bye')
            os._exit(0)
