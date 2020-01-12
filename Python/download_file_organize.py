import os
import sys
import filecmp

import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Change DownloadPath your default Download Directory
DownloadPath="Your User Path"

DownloadFiles=os.listdir(DownloadPath)

#Dictionary with file types as key and Value as file formats
FileType = { }
FileType["Images"]= ["jpeg", "jpg", "tiff", "gif", "bmp", "png", "bpg", "svg","heif", "psd"] 
FileType["Videos"]=["mkv","avi", "flv", "wmv", "mov", "mp4", "webm", "vob", "mng","qt", "mpg", "mpeg", "3gp"]
FileType["Files"]= ["oxps", "epub", "pages", "docx", "doc", "fdf", "ods","odt", "pwi", "xsn", "xps", "dotx", "docm", "dox",
                  "rvg", "rtf", "rtfd", "wpd", "xls", "xlsx", "ppt","pptx"]
FileType["Archives"]= ["zip","a", "ar", "cpio", "iso", "tar", "gz", "rz", "7z","dmg", "rar", "xar","zip"]
FileType["Audio"]= ["aac", "aa", "aac", "dvf", "m4a", "m4b", "m4p", "mp3","msv", "ogg", "oga", "raw", "vox", "wav", "wma"]
FileType["Software"]= ["exe","msi"]
FileType["PDF"]= ["pdf"]
FileType["Miscellaneous"]=[]

#Creates folders if they Don't Exist
def createFolders(downloadFolderPath):
    for folder in FileType.keys():
        folderdirectory = downloadFolderPath + "\\" + folder
        #Creates Folder if the Folder doesn't exists in the path
        if os.path.exists(folderdirectory)==False:
            os.mkdir(folderdirectory)
        
#Move file to destination folder       
def movelogic(folder,file):
    srcPath = DownloadPath + "\\" + file
    dstPath = DownloadPath + "\\" + folder + "\\" + file
    if (os.path.isfile(dstPath)==True) and (filecmp.cmp(srcPath, dstPath)):
        os.remove(srcPath)
    elif os.path.isfile(dstPath)==False:
        os.rename(srcPath, dstPath)    
    return

#Checking for fileformat                
def moveFile(DownloadPath):
    for x in os.walk(DownloadPath):
        files_in_1stGen=x[2]     
        break
    
    for filename in files_in_1stGen:        
        temp = filename.split(".")
        fileformat=temp[-1]        
        for folder in FileType.keys():          
            if fileformat in FileType[folder]:
                movelogic(folder,filename)
            elif ("." not in filename) and (filename not in FileType.keys()):
                movelogic("Miscellaneous",filename)
                
#Creates Folder Structure
createFolders(DownloadPath)

#Event Handler
class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        moveFile(DownloadPath)

if __name__ == "__main__":
    path = DownloadPath
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
