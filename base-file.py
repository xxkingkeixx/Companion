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
    try:
        a = "users" 
        b = "username" 
        c = "ip" 
        d = user.name.title() 
        e = message.ip
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO {}({},{}) VALUES("{}","{}") '.format(a,c,b,e,d))
        conn.commit()
          
    except Error as e:
      room.message(e)
    finally:
      cursor.close()
      conn.close()
    """
    
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
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == "" ):
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
    SQL SELECT FUNCTION
    Simple Select without user parameters
    @return: returns list of elements in table and the sum
    """
    def simpleSelect(tablename,column,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) ):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) ORDER BY id DESC LIMIT 25'.format(column,tablename))
          rows = cursor.fetchall()
 
          if tablename == 'wallofshame':
            room.message('Here are the last 25 messages added to the Wall of Shame. To view the Wall , go to http://chatangu.tk/wallofshame')
            results = []
            count = 0
            for row in rows:
              count += 1
              results.append(str(count)+ ": " + row[0])
              
            room.message('... '.join(results)) 
          else:
            room.message('Last 3 records')
            results = []
            for row in rows:           
              results.append(row[0])
              
            room.message(', '.join(results))  
          
        except Error as e:
          room.message(e)
        finally:
          cursor.close()
          conn.close()
    """
    Mods Coomand
    
    @return: Returns list of admins 
    """
    def mods(_):
      try:
          
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()  
        cursor.execute('SELECT username,su FROM users WHERE su LIKE "1" OR su LIKE "2" OR su LIKE "3"')
        rows = cursor.fetchall()
        results = []
        count = 0
        
        for row in rows:
          count += 1
          role = " "
          i = row[1]
          if i == 1:
            role = 'Moderator'
          elif i == 2:
            role = 'Administrator'
          elif i == 3:
            role = 'Super User'
            
          results.append(str(count)+ ": " + str(row[0]) + " ({})".format(role))
          
        room.message('Current Admins')    
        room.message('... '.join(results)) 
          
          
      except Error as e:
        room.message(str(e))
      finally:
        cursor.close()
        conn.close()
   
    
    """
    Add admin Command 
    """
    def addadmin(tablename,column,_):
      _ , __ = _.split(" ", 1)
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format(column,tablename,column,_))
          rows = cursor.fetchone()
            
          if(rows == None):
            room.message('That user doesn\'t exist')
          else:
            if(__ == ('moderator')):
              cursor.execute('UPDATE {} SET su = 1 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as Moderator!'.format(_))
            elif(__ == ('admin')):
              cursor.execute('UPDATE {} SET su = 2 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as Administrator!'.format(_))
            elif(__ == ('superuser')):
              cursor.execute('UPDATE {} SET su = 3 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as a SuperUser.. are you sure you meant to do this?'.format(_))  
            
            
          
          
        except Error as e:
          room.message(str(e))
        finally:
          cursor.close()
          conn.close()
    """
    SQL Update Function
    @tablename : The table 
    @column : The column the is changing
    @column2 : The username column
    @var: The username
    @_: The provided change 
          
    @return : returns confirmation of updated column in table      
    """      
    def update(tablename,column,column2,var,_):
     
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          if column == "notification" or "nofollow":
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            if _ == "" or " ":
              room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
            elif column == "notification" and _ == 'on':
              cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
              conn.commit()
              room.message("You turned notifications ON! (on by default if you didn't turn it off) You will now receive notifications when someone you are following has an update!  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ")
            elif column == "notification" and _ == 'off':
              cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
              conn.commit()
              room.message("You turned notifications OFF! You will not receive any notifications when someone you are following has an update.  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ")
            elif column == "nofollow" and _ == 'on':
              cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
              conn.commit()
              room.message("You changed your profile to PRIVATE! You are not allowing anyone to follow you at this point. Are you sure you didn't mean to block someone instead?  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ") 
            elif column == "nofollow" and _ == 'off':
              cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
              conn.commit()
              room.message("You changed your profile to PUBLIC! You are allowing anyone to follow you (unless you block someone with the block command)  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ")   
              
              
            
          else:  
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}"'.format(tablename,column,_,column2,var))
            conn.commit()    
            room.message('Updated your {} to {} !'.format(column,_))  
        except Error as e:
          room.message(str(e))
        finally:
          cursor.close()
          conn.close()    
    
    
          
          
    """
    Whoami Command
    
    @return:  Returns the user's name , if no nickname , the user's rl name , age, rl pic, role, and if top percent of followed users  
    """  
        
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
    prfx and '+wos': lambda _: insert('wallofshame','message',_),
    prfx and 'wos': lambda _: simpleSelect('wallofshame','message',_),
    prfx and 'addadmin': lambda _: addadmin('users','username',_),
    prfx and 'mods' : lambda _: mods(_),
    prfx and 'nickname': lambda _: update('users','nickname','username',user.name,_),
    prfx and 'age': lambda _: update('users','age','username',user.name,_),
    prfx and 'rlname': lambda _: update('users','rlname','username',user.name,_),
    prfx and 'mood': lambda _: update('users','mood','username',user.name,_),
    prfx and 'status': lambda _: update('users','status','username',user.name,_),
    prfx and 'notifications': lambda _: update('users','notification','username',user.name,_),
    prfx and 'private': lambda _: update('users','nofollow','username',user.name,_)
    
    
    }[cmd](_)

    room.message(result)
     
    
    
   
    
     
        
   
   
        
             
  def onConnect(self,room):
    room.message("SYSTEMS ONLINE: Migrate your flavors im hungry :(")
    print("ONLINE")
   
  def onJoin(self, room, user):
    room.message("Welcome "+ user.name.capitalize())




  
   
    
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