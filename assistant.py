import speech_recognition as SR
import pyttsx3
import requests
import lxml.html as lh
from phrases import P



RECOG = SR.Recognizer()
Data , mappings = [] , {}

def say(s) : 

    engine = pyttsx3.init()
    engine.say(s)
    engine.runAndWait()


def update() : 

    url = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(url)
    doc = lh.fromstring(page.content)

    td_elements = doc.xpath('//td')

    a , counter = 0 , 0
    temp = [] 
    flag = False

    global Data , mappings

    for elements in td_elements :

        content = elements.text_content()

        if content == '1' : flag = True
        if content == 'Total:' : break

        if flag : 

            if a % 19 != 0 : 

                temp.append(content) if content not in ['' , 'N/A'] else temp.append('not available') 

            else : 
                temp.append(content)
                Data.append(temp)
                mappings[temp[0]] = counter
                counter += 1
                temp = []
            a += 1 

    Data.remove(['1']) 

def clear_update() : 

    global Data , mappings

    say('Updating data')
    Data.clear()
    mappings.clear()
    update()

update()
flag , t_counter = False , 0

while True : 

    try : 
        with SR.Microphone() as source : 

            RECOG.adjust_for_ambient_noise(source)
            
            audio = RECOG.listen(source)
            que = RECOG.recognize_google(audio)


        if 'are you ready' in que :
             flag = True  
             say('Yes i am ready') 

        elif 'ok thank you' in que :
             say('Goodbye , have a nice day')  
             break
                

        if flag : 

            if 'update' not in que : 
                for phr , idx in P.items() : 
                    if phr in que : 
                        p = phr
                        index_ = idx
                        break

                for country in [c[0] for c in Data]  :
                    if country in que : 
                        ctr = country
                        break

                try :    
                    numeric_value = Data[mappings.get(ctr) - 1][index_]
                    say(f'The {p} in {ctr} are {numeric_value}')
                    
                except : 
                    t_counter += 1
                    if t_counter > 1 : say('Sorry I cannot understand')  
                    else : pass  
                
            else : clear_update()  

        else : pass      
    
    except : pass   
    ctr = '' 
