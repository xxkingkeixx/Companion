###########################################################################################
# import  NICKS IMRPOVED CODE TO PYCHARM

#############################################################################################
import ch
import pathlib
from pathlib import Path
import random
import os
import re
import cgi
import codecs
import datetime
import binascii
import glob
import json
import imp
import webbrowser
import csv
import subprocess
import zipfile
import os.path
import sys
import io
import traceback
import time
import datetime
import binascii
import json
import threading
import urllib
import urllib2
import math
from bs4 import BeautifulSoup
from time import gmtime, strftime
from xml.etree import cElementTree as ET

import urllib2 as urlreq

##################################################################

# change FONT color NAME color , size ETC

##################################################################

class bot(ch.RoomManager):
  def onInit(self):
    self.setNameColor("FFFFFF")
    self.setFontColor("FF0000")
    self.setFontFace("arial")
    self.setFontSize(9)

################################################################################

#When someone messages in chat

################################################################################

  def onMessage(self, room, user, message):
    
                
    userTest = Path("UserDB/"+user.name+".txt")
    if userTest.exists():
      pass # Put here to avoid a syntax 
    #something
      
    
      
      
    else:
      for fname in os.listdir('UserIP/'):    
        if os.path.isfile(fname):   
          with open(fname) as f:   
            for line in f:      
              if message.ip in line:    
                print '%s' %fname
              else:
                nameTheFile = user.name
                with io.FileIO("UserDB/"+nameTheFile+".txt", "a") as file:
                  file.write(nameTheFile+" ")
                with io.FileIO("UserIP/"+nameTheFile+"-IP"+".txt", "a") as file:  
                  file.write(message.ip) 
           
      
    try:
      cmd, args = message.body.split(" ", 1)
    except:
      cmd, args = message.body, ""      
    print("[{}] {}: {}: {}".format(room.name, user.name.title(), message.body, message.ip))      
    
      
      
     
################################################################################

# ">" is set as the command toggle.  

################################################################################
    prfx = cmd[0] == ">"
    cmd = cmd[1:] if prfx else cmd

###############################################################################


#Cmds


################################################################################


#deleted for now


################################################################################

#auth system

################################################################################


#deleted for now


################################################################################
      
       
################################################################################

#The SAY command. 

################################################################################

    if cmd.lower() == "say" and prfx:
      if len(args) > 25:
        room.message("Too long >:(")
      else:
        room.message(args)
       
        
    elif cmd.lower() == "test" and prfx:
      userTest = Path("UserDB/"+user.name+".txt")
      if userTest.exists():
        room.message('This user exists')
      else:
        room.message("Error")
    
    elif cmd.lower() == "import" and prfx:
        room.message("Failed you have me in test mode..") 
    
    
     
################################################################################

#The PM command.
################################################################################
   
    elif prfx and cmd=="pm" and len(args) > 0:
      try:
        #name 
        name = args.split()[0].lower()
        # personal message 
        
        personalm = " ".join(args.split()[1:])
        
        self.pm.message(ch.User(name), "Origin: MSG FROM THE MASTER" + personalm.capitalize()+"\"")
        #tell the room 
        room.message("Message sent to "+name.capitalize()+"!")
      except:
        room.message("Error sending message.")  
        
################################################################################

#pick random number  test
  
        
################################################################################

    elif prfx and cmd == "random":
      a = random.randrange(int(args))
      room.message(str(a))
      
    elif prfx and cmd.lower() =="rooms":
      length = len(rooms)
      room.message("I'm in " +" "+ str(length) +" rooms"+" , "+ ", ".join(rooms))
      
##########################################################################################


#The YT command


##########################################################################################

    elif prfx and cmd=="yt":
      textToSearch = args.replace(" ","_")
      query = urllib.quote(textToSearch)
      url = "https://www.youtube.com/results?search_query=" + query
      response = urllib2.urlopen(url)
      html = response.read()
      soup = BeautifulSoup(html, "html5lib")
      for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'} ,limit=1):
        room.message( 'https://www.youtube.com' + vid['href'])
        
        
#ON ROOM CONNECT MESSAGE                
  def onConnect(self,room):
    room.message("SYSTEMS ONLINE: Migrate your flavors im hungry :(")
    print("ONLINE")
#Welcome guests who join the chat    
  def onJoin(self, room, user):
    room.message("Welcome "+" "+" "+user.name.capitalize())


 ################################################################################


#PM Log System/Auth System/Ping


################################################################################

    
  def onPMMessage(self, pm, user, body):
        self.setNameColor("FFFFFF")
        self.setFontColor("FF0000")
        self.setFontFace("arial")
        self.setFontSize(9)
        
        if body.startswith("_addToPing"):
          
          auth = open('auth.txt', 'a')
          
          nameValue = " ".join(body.split()[1:])
          
          authFormatting = "\n"+ nameValue
        
          auth.write(authFormatting)
          
          
          auth.close()
          
          
          
          pm.message(user, nameValue+ " has been authorized to PING")
          
        elif body.startswith("_p3"):
          nameTheFile = " ".join(body.split()[1:])
          
          
          with io.FileIO("UserTables/"+nameTheFile+".txt", "w") as file:
            file.write("3")
            
            auth = open('auth2.txt', 'a')
          
            nameValue = " ".join(body.split()[1:])
          
            authFormatting = "\n"+ nameValue
        
            auth.write(authFormatting)
          
          
            auth.close()
          
          pm.message(user, nameValue+ " has been given 3 Pings")
          
          self.pm.message(ch.User(nameValue), "You have been given 3 Pings by an Administrator. Use them by sending me a msg with _ping . Enjoy! *Testing ignore this* ")
        
        
          
          
        elif body.startswith("_p"):
          n = user.name
          numFile = open("UserTables/"+user.name+".txt", 'r+')
          numFileWrite = open ("UserTables/"+user.name+".txt", 'w+')
          numVal = numFile.read()
          
          if n in open("auth2.txt").read():
            
            if '3' in open("UserTables/"+user.name+".txt").read():
              numFileWrite('2')
              pm.message(user, "You have "+numVal+" pings left")
             
            elif '2' in open("UserTables/"+user.name+".txt").read():
              numFileWrite('1')
              pm.message(user, "You have "+numVal+" pings left" )
              
            elif "1" in open("UserTables/"+user.name+".txt").read():
              numFileWrite('0')
              pm.message(user, "You have "+numVal+" pings left. Purchase more for continued access!" )
             
        elif "tube.com" in body:
          removespaces = body.replace(" ","")
          pm.message(user, "Message Relayed to Master and Parent Chats :)")
            
          pmlogger = open('LOGGER.html', 'a')
            
          adminlogger = open('ADMINLOG.txt', 'a')
            
          time = str(datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%y'))
            
          pmFormatting = user.name.capitalize()+":  " + removespaces + "  ["+time+"]"
            
          self.pm.message(ch.User("eaaj"), pmFormatting)
          for room in self.rooms:
              room.message("Received PM from "+ pmFormatting)
            
          adminlogger.write(pmFormatting+"\n")
            
          adminlogger.close()
            
          pmlogger.close()
        
          print("[PM]"+user.name.capitalize()+": "+body) 
           
        
        elif body.startswith("_ping"):
          u = user.name
          
          if u in open('auth.txt').read():
            
            fc = open('ADMINLOG.txt', 'r')
            file_contents = fc.read()
            pm.message(user, "You are an Authorized user. Current Secrets revealed :" + file_contents)
            fc.close()
          else:
            pm.message(user, "You are not Authorized to use this command. Visit http://suko.tv/secrets for more details.")
              
          
        else:
          pm.message(user, "Message Relayed to Master and Parent Chats :)")
          
          pmlogger = open('LOGGER.html', 'a')
          
          adminlogger = open('ADMINLOG.txt', 'a')
          
          time = str(datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%y'))
          
          pmFormatting = user.name.capitalize()+":  " + body + "  ["+time+"]"
          
          self.pm.message(ch.User("eaaj"), pmFormatting)
          for room in self.rooms:
                  room.message("Received PM from "+ pmFormatting)
          
          adminlogger.write(pmFormatting+"\n")
          
          adminlogger.close()
          
          pmlogger.close()
        
        print("[PM]"+user.name.capitalize()+": "+body) 
    
  

###############################################################################


#start it up


###############################################################################
    
rooms = ["tenzaishikai"]
username = "iceball"
password = "onepiece"

bot.easy_start(rooms,username,password)