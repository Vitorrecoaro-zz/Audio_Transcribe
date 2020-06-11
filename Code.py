# Função do Código: Receber um audio mp3 como parâmetro para fazer a transcrição do audio
# Criador: Vitor de Almeida Recoaro.
# Versão: 1.2
# Data: 10/06/2020.
#Novas funcionalidades: 1.1 - Delete all the "temporaly" files and folders.
#1.2 - Save a ".txt" file, with the transcribed audio.

import speech_recognition as sr
import sys as sy
import os
from pydub import AudioSegment as au

def Clean_prompt(osname): #Clear the prompt screen
    osname = str(osname[0])
    if(osname=="Linux"):
        os.system("clear")
    elif(osname=="Windows"):
        os.system("cls")

def Transcribe_Audio(AUDIO_FILE,filepath): #Recive the audio file, to do the speech recognition
    r = sr.Recognizer()
    txt_file = open((filepath+".txt"),"a+")
    with sr.AudioFile(AUDIO_FILE) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    try: 
        txt_file.write(r.recognize_google(audio,language='pt-BR')) #If you want to change the language, view all parameters in this url : https://cloud.google.com/speech-to-text/docs/languages
        txt_file.close()
    except sr.UnknownValueError:
        print("We can't understand the audio!")

def Cut_audio(folder,PATH): #Cut a big audio to do speech recognition
    if (os.path.isdir(folder)==False):
        os.mkdir(folder)  #Create a folder for all audio cuts in the same folder of audio.
    begin_miliseconds = 0
    end_miliseconds = 45000
    i = 1
    song = au.from_mp3(PATH) #Open the audio file, which have been trimmed
    if(end_miliseconds>(song.duration_seconds*1000)):
        end_miliseconds = song.duration_seconds*1000
    test = 0
    while(end_miliseconds<=(song.duration_seconds*1000) and test<2): #Trim all audio in each 45 seconds
        extract = song[begin_miliseconds:end_miliseconds]
        if(str(osname[0])=="Linux"):
            extract.export(folder+"/Cut"+str(i)+".wav", format = "wav")
        elif(str(osname[0])=="Windows"):
            extract.export(folder+"\\Cut"+str(i)+".wav", format = "wav") 
        i += 1
        begin_miliseconds += 45000
        end_miliseconds += 45000
        if(end_miliseconds>(song.duration_seconds*1000)):
            end_miliseconds = song.duration_seconds*1000
            test += 1

PATH = input("Place here the mp3 audio path:\n")
if(os.path.isfile(PATH)==True):
    osname = os.uname()
    if(str(osname[0])=="Linux"):
        last_bar = PATH.rfind("/")
        folder = PATH[:last_bar]
    elif(str(osname[0])=="Windows"):
        last_bar = PATH.rfind("\\")
        folder = PATH[:last_bar]
    last_point = PATH.rfind(".")
    filename = PATH[last_bar:last_point]
    folder = folder + filename
    Cut_audio(folder,PATH)
    trimmedAudios = 1
    if(str(osname[0])=="Linux"):
        while((os.path.isfile(folder+"/Cut"+str(trimmedAudios)+".wav"))==True):
            Transcribe_Audio((folder+"/Cut"+str(trimmedAudios)+".wav"),folder)
            trimmedAudios += 1
    elif(str(osname[0])=="Windows"):
        while(os.path.isfile(folder+"\\Cut"+str(trimmedAudios)+".wav"==True)):
            Transcribe_Audio((folder+"\\Cut"+str(trimmedAudios)+".wav"),folder)
            trimmedAudios += 1
    i = 1        
    while(i<trimmedAudios):
        if(str(osname[0])=="Linux"):
            os.remove(folder+"/Cut"+str(i)+".wav")
        elif(str(osname[0])=="Windows"):
            os.remove(folder+"\\Cut"+str(i)+".wav")
        i += 1
    if(str(osname[0])=="Linux"):
        os.rmdir(folder)
    elif(str(osname[0])=="Windows"):
        os.rmdir(folder)
else:
        input("I can't find the file.\nPress ENTER to continue.")
        Clean_prompt(os.uname())

