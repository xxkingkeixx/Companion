"""
@projectname: Companion
@hostsite: Chatango.com


"""
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
from configparser import ConfigParser
import urllib2 as urlreq
from mysql.connector import MySQLConnection, Error


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    @param filename: name of the configuration file
    @param section: section of database configuration
    @return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

def connect():
    """ Connect to MySQL database """
 
    db_config = read_db_config()
 
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
 
        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
 
    except Error as error:
        print(error)
 
    finally:
        conn.close()
        print('Connection closed.')
 
 
if __name__ == '__main__':
    connect()

#end

class bot(ch.RoomManager):
  
  
  
  def onInit(self):
    self.setNameColor("FFFFFF")
    self.setFontColor("FF0000")
    self.setFontFace("arial")
    self.setFontSize(9)
    
  """
  @param self: Bot 
  @param room: The Chatroom
  @param user: The Chatango user
  @param message: The message in the chatroom
  

  """

  def onMessage(self, room, user, message):
    try:
      cmd, args = message.body.split(" ", 1)
    except:
      cmd, args = message.body, ""      
    print("[{}] {}: {}: {}".format(room.name, user.name.title(), message.body, message.ip))      
    
    """
    @param prfx: The Command init
    @param cmd: The second part of the body
    @param _: The argument after the command
    
    """
    
    prfx = cmd[0] == ">"
    cmd = cmd[1:] if prfx else cmd
    _ = args

    """
    @param name: the username
    @param pm: chatango pm
    
    """
    def pmcmd(_): 
      try:
        name = _.split()[0].lower()
        personalm = " ".join(_.split()[1:])
        self.pm.message(ch.User(name), "Origin: MSG FROM THE MASTER" + personalm.capitalize()+"\"")
        room.message("Message sent to "+name.capitalize()+"!")
      except:
        room.message("Error sending message.")  
        
    """ 
    Outputs Query Result from youtube keyword search 
    @module beautifulsoup
    
    """
    
    def yt(_):
      textToSearch = args.replace(" ","_")
      query = urllib.quote(textToSearch)
      url = "https://www.youtube.com/results?search_query=" + query
      response = urllib2.urlopen(url)
      html = response.read()
      soup = BeautifulSoup(html, "html5lib")
      for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'} ,limit=1):
        room.message( 'https://www.youtube.com' + vid['href'])
        
    """ 
    SQL INSERT FUNCTION
    
    @param tablename: The target SQL table
    @param column: The target column in the table
    @param _: The user input
    @return: Returns confirmation that the record was added to the SQL table
    """
    
    def insert(tablename,column,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table",""," ")) ):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('INSERT INTO {}({}) VALUES("{}") '.format(tablename,column,_))
          conn.commit()
          room.message("Added {} to {}.".format(_,tablename))      
            
        except Error as e:
          room.message(e)
        finally:
          cursor.close()
          conn.close() 
    
        
        
    """
    The bot commands
    @param result: runs function based on command
    @func lambda: Runs arguments if any in command
    @return: Returns output if command in dictionary
    
    """

    result = {
    prfx and 'say': lambda _:  _,
    prfx and 'test': lambda _: 'Working!',
    prfx and 'pm': lambda _: pmcmd(_),
    prfx and 'random': lambda _: str(random.randrange(int(_))),
    prfx and 'rooms': lambda _:  "I'm in "+ str(len(rooms)) +" rooms , " + ", ".join(rooms),
    prfx and 'yt': lambda _: yt(_),
    prfx and 'wallofshame': lambda _: insert('wallofshame','message',_)
    
    }[cmd](_)

    room.message(result)
     
    
    
   
    
     
        
   
   
        
             
  def onConnect(self,room):
    room.message("SYSTEMS ONLINE: Migrate your flavors im hungry :(")
    print("ONLINE")
#Welcome guests who join the chat    
  def onJoin(self, room, user):
    room.message("Welcome "+" "+" "+user.name.capitalize())




  
   
    
  def onPMMessage(self, pm, user, body):
        self.setNameColor("FFFFFF")
        self.setFontColor("FF0000")
        self.setFontFace("arial")
        self.setFontSize(9)
        
        
        
         
          
       
             
        if "tube.com" in body:
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