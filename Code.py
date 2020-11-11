# Função do Código: Receber um audio mp3 como parâmetro para fazer a transcrição do audio
# Criador: Vitor de Almeida Recoaro.
# Versão: 1.5
# Data: 10/06/2020.
# Novas funcionalidades: 1.1 - Delete all the "temporaly" files and folders.
# 1.2 - Save a ".txt" file, with the transcribed audio.
# 1.3 - How much files do you want to transcribe? You can do this just running this program once.
# 1.4 - If the transcribe text file exist, the file will be erased and start over.
# 1.5 - You can do multiple files when the program is running.

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

def Transcribe_Audio(AUDIO_FILE,filepath,op): #Recive the audio file, to do the speech recognition
    r = sr.Recognizer()
    if(op==1):
        txt_file = open((filepath+".txt"),"w+")
    else:
        txt_file = open((filepath+".txt"),"a+")
    with sr.AudioFile(AUDIO_FILE) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    try: 
        txt_file.write(r.recognize_google(audio,language='pt-BR')) #If you want to change the language, view all parameters in this url : https://cloud.google.com/speech-to-text/docs/languages
        txt_file.close()
    except sr.UnknownValueError:
        print("We can't understand the audio!")
    return 2

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
        extract.export(folder+"/Cut"+str(i)+".wav", format = "wav") 
        i += 1
        begin_miliseconds += 45000
        end_miliseconds += 45000
        if(end_miliseconds>(song.duration_seconds*1000)):
            end_miliseconds = song.duration_seconds*1000
            test += 1
    return i

another = 'Y'
while(another=='Y' or another=='y'):
    number_files = int(input("How much files do you want to do:\n"))
    while(number_files<=0):
        number_files = int(input("Enter a valid number: \n"))
    aux = 0
    PATH = [] # Create an array to save all files path.
    while(aux<number_files):
        PATH.append(input("Place here the mp3 audio path:\n"))
        aux += 1
    aux = 0
    while(aux<number_files):
        if(os.path.isfile(PATH[aux])==True):
            print("Processing...\nJust wait =D.\n\n")
            osname = os.uname()
            last_bar = PATH[aux].rfind("/")
            folder = PATH[aux][:last_bar]
            last_point = PATH[aux].rfind(".")
            filename = PATH[aux][last_bar:last_point]
            folder = folder + filename
            audios = Cut_audio(folder,PATH[aux])
            trimmedAudios = 1
            again = 2 
            if((os.path.isfile(folder+".txt"))==True): 
                txt_file = open((folder+".txt"),"r")
                last_line = txt_file.readlines()
                txt_file.close()
                last_line = last_line[-1]
                if(last_line==".END"): # Test if the mark show that file is complete.
                    op = input("The file already exist.\nDo you want to transcribe again?\nAnwser (Y/N): ")
                    while(op!='N' and op!='n' and op!='Y' and op!='y'):
                        op = input("Enter a valid anwser (Y/N): ")
                    if(op=='n' or op=='N'):
                        again = 0
                        Clean_prompt(os.uname())
                    else:
                        again = 1
            if(again!=0):
                while((os.path.isfile(folder+"/Cut"+str(trimmedAudios)+".wav"))==True):
                    again = Transcribe_Audio((folder+"/Cut"+str(trimmedAudios)+".wav"),folder,again) #If again is 2, the file is open in mode "append", if 1 the file is open in mode "write" cleaning the file.
                    trimmedAudios += 1
                txt_file = open((folder+".txt"),"a+")
                txt_file.write("\n.END") # This is mark a to test if the file is complete. 
                txt_file.close()
            i = 1        
            while(i<audios):
                os.remove(folder+"/Cut"+str(i)+".wav")
                i += 1
            os.rmdir(folder)
            print("Complete!\n\n")
        else:
            input("I can't find the file.\nPress ENTER to continue.")
            Clean_prompt(os.uname())
        aux +=1
    another = input("Do you want in another audio (Y/N) ?\nAnwser: ")
    while(another!='Y' and another!='y' and another!='N' and another!='n'):
        another = input("This anwser is not valid.\nChoose (Y/N): ")

