######Following libraries should be installed
#gTTS
#SpeechRecognition
#pyglet
#pyaudio
#terminaltables
#gpiozero pigpio

import speech_recognition as sr
import webbrowser 
import speak
import pyglet
import os
import time
import fnmatch
from terminaltables import SingleTable
import  json, urllib.parse
from urllib.request import urlopen
from time import sleep


######Raspberry pi configuration for light on off. Uncomment single line comments when you configured your pi
# os.environ["PIGPIO_ADDR"] = "fe80::b6b2:6253:181e:a033%14"
# os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

######Library for controlling raspberry pi's gpio pin
# from gpiozero import LED

######Set GPIO Pin
# led = LED(26)



print("-" * 15 + "==Bangla & English voice recognition by Python==" + "-" * 15)

def main_program():
    print ("\n\n\n\nSay: \n\t 'search in internet'  --> Search internet \n\t 'search in computer'  --> Search within computer \n\t 'temperature'  --> Current temperature of any city  \n\t 'date' \n\t 'time' \n\t 'light on or off'\n\t 'exit' --> to close the program \n\n") 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Reducing ambient noise
        r.energy_threshold = 4000  
        r.dynamic_energy_threshold = True 
        try: 
            audio = r.listen(source)
            en_voice_recog = r.recognize_google(audio)
            bn_voice_recog = r.recognize_google(audio, language='bn-BD')

            if "search in internet" in en_voice_recog:
                r2 = sr.Recognizer()
                with sr.Microphone() as source:
                    pyglet.media.load("audio.what-info-in-internet.mp3").play()
                    print("What information you want to search")
                    audio2 = r2.listen(source)

                    try:
                        print('Please wait')
                        pyglet.media.load("audio.please-wait.mp3").play()
                        url = 'https://www.google.com.bd/search?q=' + r.recognize_google(audio2)
                        webbrowser.open_new(url)
                        time.sleep(2)
                
                    except sr.UnknownValueError:
                            print("I could not understand audio")
                            speak.tts("I could not understand audio", lang='en')
                    except sr.RequestError as e:
                            print("Could not request results from Google Speech Recognition service; {0}".format(e))
                
                
            elif "search in computer" in en_voice_recog:
                r3 = sr.Recognizer()
                with sr.Microphone() as source:
                    pyglet.media.load("audio.say-file-name.mp3").play()
                    print("Please say the file name")
                    audio3 = r3.listen(source) 
                    fileName = r.recognize_google(audio3)

                def find(pattern):
                    with sr.Microphone() as source:
                        pyglet.media.load("audio.searching-file.mp3").play()
                        time.sleep(4)
                        print("\n=====================Searching file named: " + fileName + "\n")
                        
                        SearchResult = os.getcwd() + "\\searchResult.txt"  
                        if os.path.isfile(SearchResult):
                            os.remove("searchResult.txt")
                        count = 1

                        for root, dirs, files in os.walk('C:\\'):
                            for name in files:
                                if fnmatch.fnmatch(name[:len(pattern)], pattern):
                                    table_data = [
                                        ['Search ID', 'File Location', 'File Name'],
                                        [str(count), os.path.join(root, name), os.path.join(name)]
                                    ]
                                    table = SingleTable(table_data)
                                    print (table.table)
                                    file = open("searchResult.txt","a") 
                                    file.write(str(count) + ','   + os.path.join(root, name))
                                    file.write('\n')               
                                    file.close()
                                    count+=1

                        if os.path.isfile(SearchResult) != True:
                            pyglet.media.load("audio.no-file-found.mp3").play()
                            print('Sorry, no result found')
                            print("\n\n===================Search finish=====================")
                            time.sleep(3)
                            main_program()

                        else:
                            r4 = sr.Recognizer()
                            with sr.Microphone() as source:
                                pyglet.media.load("audio.open-file.mp3").play()
                                print("Say 'yes'/'no'") 
                                audio4 = r4.listen(source)

                            if 'yes' in r.recognize_google(audio4):
                                def user_said_yes_to_open():
                                    r5 = sr.Recognizer()
                                    with sr.Microphone() as source:
                                        pyglet.media.load("audio.search-id-correspond-to-file.mp3").play()
                                        print("Tell the search id from given search result:") 
                                        audio5 = r5.listen(source)

                                        with sr.Microphone() as source:
                                            speak.tts("Opening the file"  , lang='en')
                                            print("\nOpening the file ")

                                        file_id = r.recognize_google(audio5) 
                                        file = open("searchResult.txt")
                                        for line in file:
                                            x=line.split(",")
                                            x[-1] = x[-1].strip()
                                            if (x[0] == str(file_id)):
                                                try:
                                                    os.startfile(x[1], 'open')
                                                except FileNotFoundError:
                                                    print("Cant'open the file'")
                                user_said_yes_to_open()
                                
                                time.sleep(3)
                                search_yes_loop = True
                                while search_yes_loop:
                                    with sr.Microphone() as source:
                                        r6 = sr.Recognizer()
                                        pyglet.media.load("audio.open-another-file.mp3").play()
                                        print("Open another file? (Say: 'yes'/'no')")  
                                        audio6 = r6.listen(source)
                                        
                                        if 'yes' in r.recognize_google(audio6):
                                            user_said_yes_to_open()
                                    
                                        elif 'no' in r.recognize_google(audio6):
                                            search_yes_loop  = False
                                            main_program()       
                                
                            elif 'no' in r.recognize_google(audio4):
                                main_program()                                    

                find(fileName)

            elif "temperature" in en_voice_recog or "তাপমাত্রা" in bn_voice_recog:
                def find_wheather():
                    weather_r = sr.Recognizer()
                    with sr.Microphone() as source:
                        speak.tts("Please say the city name", lang='en')
                        print("Say the city name")
                        weather_audio = weather_r.listen(source) 

                        baseurl = "https://query.yahooapis.com/v1/public/yql?"
                        current_city = r.recognize_google(weather_audio)
                        yql_query = "select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + current_city + "') and u='c'"
                        yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
                        result = urllib.request.urlopen(yql_url).read()
                        data = json.loads(result)
                        fetched_temp = data['query']['results']['channel']['item']['condition']['temp']
                        print ("Temperature is "+ fetched_temp + " degree celcius")
                        speak.tts("Current temperature of " + current_city + " is " + fetched_temp + " degree celsius", lang='en')

                        time.sleep(2)
                        main_program()
                find_wheather()      

            ######Raspberry pi configuration for light on off. Uncomment single line comments when you configured your pi
            # elif "light on" in en_voice_recog or "জ্বালাও" in bn_voice_recog:
            #     led.on() 
            #     print("Light on")

            # elif "light off" in en_voice_recog or "নিভাও" in bn_voice_recog:
            #     led.off()
            #     print("Light off")

            elif "date" in en_voice_recog or "তারিখ" in bn_voice_recog:
                speak.tts("today's date is: " + time.strftime("%d, %b %Y") ,lang = "en")
                print ("Today's date: " + time.strftime("%d, %b %y"))
                main_program()

            elif "time" in en_voice_recog or "বাজে" in bn_voice_recog:
                speak.tts("Time is: " + time.strftime("%I:%M %p") ,lang = "en")
                print ("Currnet time is: " + time.strftime("%I:%M %p"))
                main_program()
                
            elif "exit" in en_voice_recog:
                print("Closing the program")
                time.sleep(2)
                os._exit(0)

        except sr.UnknownValueError:
            print("Couldn't understand the voice. There might be too much noise in the surroundings. Please say again")
            main_program()

while True:
    main_program()
