# Importing all necessary libraries
import os
from pytube import YouTube
from pytube import Search
import random
from moviepy.editor import *
import shutil
import time

#For coloring the text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Intro message
# f"{bcolors.OKGREEN} [GREEN] {bcolors.ENDC}"
# f"{bcolors.OKCYAN} [CYAN] {bcolors.ENDC}"
print(f"{bcolors.OKGREEN} Hello, welcome to VidSave! I'll walk you through downloading your music! \n {bcolors.ENDC}")

print(f"{bcolors.OKGREEN} Please enter the names of all the music you want, separated by enters.\nOnce done, type y and I will begin Installation process {bcolors.ENDC}")

#Empty list of song names
songs = []


done = False
while not done:
    # Message for input
    name = input(f"{bcolors.OKCYAN} Write the name of the Song, type y if done :  {bcolors.ENDC}")
    
    nameLy = name + "lyrics"
    #end it
    if name.lower() == "y":
        done = True
    elif nameLy in songs:
        #Message if song is already there
        print(f"{bcolors.FAIL} Whoops, looks like you already added that song!{bcolors.ENDC}")
    else:
        #Find a lyric video of the song
        songs.append(nameLy)

    

print(f"{bcolors.OKGREEN} Ok, Saving the following songs ->\n {bcolors.ENDC}")
#Show songs being saved
print(songs)

#Make a folder with random name in downloads
randomNum = random.randint(1,1000)
folder = f"./{randomNum}"
os.mkdir(folder)

#To store links
links = []

#Function to search all of the songs, and collect the lists
print(f"{bcolors.OKGREEN} Searching for songs {bcolors.ENDC}")

for s in songs:
    searchList = Search(str(s))

    #Get the first result, take the video ID, and make it into a youtube link, and add to link
    firstResult = str(searchList.results[0])
    vidID = firstResult.split("=")[1].replace(">","")
    finalLink = "https://www.youtube.com/watch?v=" + vidID
    links.append(finalLink)

print(f"{bcolors.OKGREEN} Searching Complete! {bcolors.ENDC}")
print(f"{bcolors.OKGREEN} {str(len(links))} songs added {bcolors.ENDC}")

#Go through the list and download each file one by one, to the previously made folder

print(f"{bcolors.OKGREEN} Downloading all songs... {bcolors.ENDC}")

print(f"{bcolors.FAIL} Note : Please ignore the error messages{bcolors.ENDC}")
time.sleep(3)


counter = 0
total = len(links)

for l in links:

    #Download the video at lowest rez to the folder
    target = YouTube(l)
    songName = str(songs[counter]).replace(" ", "_") + ".mp4"
    target.streams.filter(file_extension="mp4").first().download(folder, filename=songName)
    counter += 1
    print(f"Downloaded {counter} / {total}")


print(f"{bcolors.OKGREEN} Converting to MP3 files... {bcolors.ENDC}")

# Videos are obtained in MP4 files, so we must convert to MP3

#Code from SO for conversion
def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)     
    mp4_without_frames.close() 
    

for file in os.listdir(folder):

    #Get the file path
    filePath =folder + "/" + file

    # Creat a name for the new files
    fileName = file.split(".")[0]
    fileNameWithExt = str(fileName) + ".mp3"  

    #convert
    mp4_to_mp3(filePath, fileNameWithExt)

    #Delete the original File
    os.remove(filePath)  

    #Take the mp3 and put it in original folder
    mp3Start =fileNameWithExt
    mp3End = folder + "/" + fileNameWithExt
    shutil.move(mp3Start, mp3End)


#Delete the original File#End message
print(f"{bcolors.OKGREEN} Downloading complete! Files have been saved to {folder} {bcolors.ENDC}")