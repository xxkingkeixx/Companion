"""
@projectname: Companion
@hostsite: Chatango.com


"""
import ch
import requests
import pathlib
from pathlib import Path
import random
import os
import re
import cgi
import codecs
import datetime
import binascii
import HTMLParser
import glob
import json
import imp
import webbrowser
import csv
import subprocess
from subprocess import call
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
import resp
from bs4 import BeautifulSoup
from time import gmtime, strftime
from xml.etree import cElementTree as ET
from configparser import ConfigParser
import urllib2 as urlreq
from mysql.connector import MySQLConnection, Error

################################################################################

#DATABASE CONNECTION BOIIIII

################################################################################

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



################################################################################

#START CHATROOM SECTION  BOIIIIIIIIIIIIIIIIIII

################################################################################

class bot(ch.RoomManager):
  
  
  
  def onInit(self):
    self.setNameColor("FFFFFF")
    self.setFontColor("CC0033")
    self.setFontFace("0")
    self.setFontSize(10)
    self.enableBg()  
    self.enableRecording()
    
    

        
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
    
    if ((user.name).startswith(('#','!'))):
      pass
     
    else:
      try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format('username','users','username',user.name))
        rows = cursor.fetchone()
              
        if(rows == None):
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
          cursor.close()
          conn.close()    
        
        else:
          cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format('ip','users','username',user.name))
          rows = cursor.fetchall()
          row = rows[0]
          
          if((row != str(message.ip)) and len(message.ip) > 1):
            
            a = "users" 
            b = "username" 
            c = "ip" 
            d = user.name.title() 
            e = message.ip
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}" '.format(a,c,e,b,d))
            conn.commit()
            cursor.close()
            conn.close()
          else:
            cursor.close()
            conn.close()
            pass
      
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
      
    
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
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:  
        try:
          name = _.split()[0].lower()
          personalm = " ".join(_.split()[1:])
          self.pm.message(ch.User(name), "Sent from {}...".format(user.name) + personalm.capitalize()+"\"")
          room.message("Message sent to "+name.capitalize()+"!")
        except:
          room.message("Error sending message.")  
        
    """ 
    Outputs Query Result from youtube keyword search 
    @module beautifulsoup
    
    """
    
    def yt(_):
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:  
        textToSearch = args.replace(" ","_")
        query = urllib.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html5lib")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'} ,limit=1):
          room.message( 'https://www.youtube.com' + vid['href'])
    
    """
    NOTIFICATION FUNCTION
    
    
    """
    
    def notify(message,var):
      dbconfig = read_db_config()
      conn = MySQLConnection(**dbconfig)
      cursor = conn.cursor()
      cursor.execute('select username from users where notifications=0 and username IN (select follower from followers where followed like "{}")'.format(var))
      results = cursor.fetchall()
      for result in results:
        self.pm.message(ch.User(str(result[0])), message)
      conn.close()  
    
    def pm(user,message):
      self.pm.message(ch.User(str(user)), message)
    
    """ 
    SQL INSERT FUNCTION
    
    @param tablename: The target SQL table
    @param column: The target column in the table
    @param _: The user input
    @return: Returns confirmation that the record was added to the SQL table
    """
    
    def insert(tablename,column,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == "" ):
        room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('INSERT INTO {}({}) VALUES("{}") '.format(tablename,column,_))
          conn.commit()
          room.message("Added {} to {} *pukes* ".format(_,tablename))      
          notify("{} just added...  {}  ..to the Wall of Shame! ;) ".format(user.name,_),user.name)
          
            
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
        room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) ORDER BY id DESC LIMIT 25'.format(column,tablename))
          rows = cursor.fetchall()
 
          if tablename == 'wallofshame':
            room.message(' :@ Here are the last 25 messages added to the Wall of Shame. To view the Wall , go to http://chatangu.tk/wallofshame')
            
            results = []
            for count, row in enumerate(rows, 1):
               
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
    Mods Command
    
    @return: Returns list of admins 
    """
    def mods(_):
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:  
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
            
          room.message('Current Admins *bored* ')    
          room.message('... '.join(results)) 
            
            
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()
   
    
    """
    Add admin Command 
    """
    def addadmin(tablename,column,_):
      _ , __ = _.split(" ", 1)
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format(column,tablename,column,_))
          rows = cursor.fetchone()
            
          if(rows == None):
            room.message(' *stop* That user doesn\'t exist')
          else:
            if(__ == ('moderator')):
              cursor.execute('UPDATE {} SET su = 1 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as Moderator! :) '.format(_))
            elif(__ == ('admin')):
              cursor.execute('UPDATE {} SET su = 2 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as Administrator! 8) '.format(_))
            elif(__ == ('superuser')):
              cursor.execute('UPDATE {} SET su = 3 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              room.message('Set {} as a SuperUser.. are you sure you meant to do this? :o '.format(_))  
        except Error as e:
          print e
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
    def update(tablename,column,column2,var,_,message,alert):
     
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          if _ ==  " ":
            room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
          if column == "notifications" and _ == 'on':
            cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            room.message(" ;) You turned notifications ON! (on by default if you didn't turn it off) You will now receive notifications when someone you are following has an update!  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ]")
          elif column == "notifications" and _ == 'off':
            cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            room.message(" :| You turned notifications OFF! You will not receive any notifications when someone you are following has an update.  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ]")
          elif column == "nofollow" and _ == 'on':
            cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            room.message('You tried: UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var) )
            room.message(" :| You changed your profile to PRIVATE! You are not allowing anyone to follow you at this point. Are you sure you didn't mean to block someone instead?  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot] ") 
          elif column == "nofollow" and _ == 'off':
            cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            room.message(" ;) You changed your profile to PUBLIC! You are allowing anyone to follow you (unless you block someone with the block command)  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ] ")   
              
          else:  
            
            cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}"'.format(tablename,column,_,column2,var))
            conn.commit()    
            room.message('Updated your {} to {} ! *star* '.format(column,_))
            if alert == 0:
              notify("{} just updated {} to... {}  ".format(var,message,_),var)
            else:
              pass
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()    
    
    """
    Follow / Unfollow Command
    """
    def social(tablename,tablename2,tablename3,column,column2,column3,column4,column5,column6,var,_,n):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message(' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          cursor.execute("""SELECT({}) FROM({}) 
          WHERE {} LIKE '{}'""".format(column,tablename,column,_))
          
          rows = cursor.fetchone()
          
          if(rows == None):
            room.message(' *stop* That user doesn\'t exist')
            cursor.close()
            conn.close()
          if(rows != None):
            i = rows[0]
         
          if i.lower() == _ :
            if n == 1:
              cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename3,column5,_,column6,var))
              conn.commit()
              room.message('You unfollowed {}.. You will not receive anymore updates from this person  *hb* '.format(_))
            else:  
              
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format(column2,tablename,column,_))
              rows = cursor.fetchone()
              test = rows[0]
              if test == 0:
                a = True
              else:
                room.message(' *stop* This user is PRIVATE so you can\'t follow them')
                cursor.close()
                conn.close()
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,_,column3,var))
              rows = cursor.fetchone()
            
              if rows == None:
                b = True
              else:
                room.message('This user has blocked you.. maybe talk to them and get back to me? *hb* ')
                cursor.close()
                conn.close()
            if(a and b == True):
              try:
                cursor.execute('INSERT INTO {}({},{}) VALUES("{}","{}") '.format(tablename3,column5,column6,_,var))
                conn.commit()
                room.message('You are now following {}! You will receive notifications whenever this user has an update! *star* '.format(_))
                notify("{} is now following {}.".format(var,_),var)
                pm(_,'{} just followed you!'.format(var))
              except Error as e:
                room.message(' *stop* You have already followed this person!.')
              finally:
                cursor.close()
                conn.close()
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()
   
    def manage(tablename,tablename2,tablename3,tablename4,column,column3,column4,column5,column6,var,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          cursor.execute("""SELECT({}) FROM({}) 
          WHERE {} LIKE '{}'""".format(column,tablename,column,_))
          
          rows = cursor.fetchone()
          
          if(rows == None):
            room.message(' *stop* That user doesn\'t exist')
            
          else:
            i = rows[0]
            if tablename3 == 'block':
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,var,column3,_))
              rows = cursor.fetchone()
              if rows == None:
                try:
                  cursor.execute('INSERT INTO {}({},{}) VALUES("{}","{}") '.format(tablename2,column3,column4,_,var))
                  conn.commit()
                  cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename4,column5,var,column6,_))
                  conn.commit()
                  
                  room.message('Blocked {} *hb* This person cannot follow you or access your information. '.format(_))
                  
                except Error as e:
                  print(e)
              else:
                room.message(' *stop* You already blocked {}..  Did you mean to unblock?'.format(_))
            
            
            if tablename3 == 'unblock':
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,var,column3,_))
              rows = cursor.fetchone()
              
              if rows == None:
                room.message(' *stop* You never blocked {}'.format(_))
              else:    
                cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename2,column4,var,column3,_))
                conn.commit()
                room.message('You unblocked {}.. how sweet of you *h* *blush*'.format(_))
        
        finally:
          cursor.close()
          conn.close()
    
    """
    View Followers Command
    
    Return: The user's followers or a selected user
    """
    def followers(_,var,x):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table"))):
        room.message('You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        room.message('No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          if (_ == "" and x == 0):
            cursor.execute('select follower from followers where followed = "{}"'.format(var))
            rows = cursor.fetchall()
            results = []
            room.message('You have {} followers'.format(cursor.rowcount))
            for count, row in enumerate(rows, 1):
                     
              results.append('{}. {} '.format(count,row[0]))
            if(cursor.rowcount == 0):
              pass
            else:
              room.message('... '.join(results))
         
          elif (_ == "" and x == 1):
            cursor.execute('select followed from followers where follower like "{}"'.format(var))
            rows = cursor.fetchall()
            results = []
            room.message('You are following {} user(s)'.format(cursor.rowcount))
            for count, row in enumerate(rows, 1):
                     
              results.append(str(count)+ ": " + row[0])
                  
            if(cursor.rowcount == 0):
              pass
            else:
              room.message('... '.join(results))   
         
          
          
          else:
            cursor.execute("SELECT({}) FROM({}) WHERE {} LIKE '{}'".format('username','users','username',_))
          
            rows = cursor.fetchone()
          
            if(rows == None):
              room.message(' *stop* That user doesn\'t exist')
            
            else:
             
              if(_ != "" and x == 0):
                cursor.execute('select follower from followers where followed = "{}"'.format(_))
                rows = cursor.fetchall()
                results = []
                room.message('{} has {} followers'.format(_,cursor.rowcount))
                for count, row in enumerate(rows, 1):
                       
                  results.append(str(count)+ ": " + row[0])
                      
                if(cursor.rowcount == 0):
                  pass
                else:
                  room.message('... '.join(results))
              elif (_ != "" and x == 1):
                cursor.execute('select followed from followers where follower like "{}"'.format(_))
                rows = cursor.fetchall()
                room.message('{} is following {} user(s)'.format(_,cursor.rowcount))
                results = []
                
                for count, row in enumerate(rows, 1):
                       
                  results.append(str(count)+ ": " + row[0])
                        
                if(cursor.rowcount == 0):
                  pass
                else:
                  room.message('... '.join(results))      
        
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()  
   
    """
    Restart Bot animation: Power Cycles Bot with delays
    
    
    """
    def restart():
      #prompt
      room.message('Saving states... powering off.. zzzz')
      #cycle 1
      a = lambda x: room.message('{}'.format(x))
      b = 'Rebooting *star* '
      c =threading.Timer(4,a,[b])
      c.start()
      #cycle2
      d = lambda x: room.disconnect() 
      e = threading.Timer(8,d,"_")
      e.start()
      #reboot
      f = lambda x: os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
      g = threading.Timer(9,f,"_")
      g.start()
      
    """
    The helper commands
    
    @return: Returns information about bot and main helper commands
          
    """
    def help():
      room.message(' *star* To see General Commands (like say) ,use >general . For Social Commands (like status) , use >social. For Merchant Commands (like Currency) , use >merchant. Keep in mind many commands may change and some will be eliminated for pm or chat usage only. Updates will be regularly added to my Documentation , http://chatangu.tk/bot ')
    def gcmds():
      room.message(" *star* General Commands: help , general , merchant , say , random, rooms, math , pm , yt , gi, ud , gs , reddit , addAdmin , removeAdmin , admin+ , admin- , mods , ipInfo  , whois , whoami, reboot ..")
    def scmds():
      room.message("Social Commands: followers  ,follow  , feed  , popularity  ,checkpopularity  ,mostHated  ,mostLoved  , topTrolls  ,status  ,mood  ,age  , schedule  , randompic  , listFavoriteThings  , showUserComment  , showRecentComments  ,showCurrency  ,currency  ,rlpic , nickname , whyhate , whylove , whystalk , whyfriend ,whyreject , Goodnight , goodnightAll , goodmorning , goodmorningAll , +friend ,-friend ,+lover ,-lover ,+hater ,-hater ,+stalker ,-stalker ,+crush ,-crush ,+ex ,-ex ,+reject ,-reject , +randompic ,+status ,+mood ,+favoritething ,-favoritething ,+userComment ,-userComment ,+comment ,-whyhate ,-whylove ,-whystalk ,-whyfriend ,voteHate ,votedLove ,voteTroll , unfollow , blockfollow , unblockfollow , nofollow...")
    def mcmds():
      room.message('NotImplemented')
    
    """
    Whoami Command
    
    @return:  Returns the user's name , if no nickname , the user's rl name , age, rl pic, role, and if top percent of followed users  
    """  
    def who(x,y):
      try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('select * from users where username like "{}"'.format(x))
          rows = cursor.fetchone()
          row = rows
          #assign
          rlpic = row[7]
          role = row[2]
          ip = row[1]
          username = row[3]
          rlname =  row[13]
          age = row[6]
          nickname = row[8]
          
          
          
          if role == 0:
            role = 'Role: User'
          if role == 1:
            role = 'Role: Moderator'
          if role == 2:
            role = 'Role: Admin'
          if role == 3:
            role = 'Role: Superuser'  
          
          if nickname == None:
            nickname = ' [n/a] '
          if rlpic == None:
            rlpic = ' [n/a] '
          if age == None:
            age = ' [n/a] '
          if rlname == None:
            rlname = ' [n/a] '  
            
          
          if y == 0:  
            try:
              if len(ip) > 1:
                cursor.execute('select username from users where ip = "{}"'.format(ip))
                result = cursor.fetchall()  
                aliases = cursor.rowcount
                lst = []
                  
                for count, uname in enumerate(result, 1):
                  lst.append(" {}: {} ".format(count,uname[0]))
                output = "...".join(lst)
                
                cursor.execute('select follower from followers where followed = "{}"'.format(x))
                r = cursor.fetchall()
                n = cursor.rowcount
                print('you tried: select follower from followers where followed = "{}"'.format(x))
                for x in r:
                  print x[0]
                print n
                
                  
                room.message('{} [{}]: Hey {} *h* , your name is {} , age {} with {} follower(s). You have {} alternate account(s) recorded.({})'.format(rlpic,role,username,rlname,age,n,aliases,output))  
              if len(ip) < 1:
                cursor.execute('select follower from followers where followed = "{}"'.format(x))
                r = cursor.fetchall()
                n = cursor.rowcount
                print('you tried: select follower from followers where followed = "{}"'.format(x))
                for x in r:
                  print x[0]
                print n
                
                  
                room.message('{} [{}]: Hey {} *h* , your name is {} , age {} with {} follower(s). You have {} alternate account(s) recorded.'.format(rlpic,role,username,rlname,age,n,0)) 
              
            except Error as e:
              print e
              
          else:
            if len(ip) > 1:
              cursor.execute('select username from users where ip = "{}"'.format(ip))
              result = cursor.fetchall()  
              aliases = cursor.rowcount
              lst = []
                    
              for count, uname in enumerate(result, 1):
                lst.append(" {}: {} ".format(count,uname[0]))
              output = "...".join(lst)
                  
              cursor.execute('select follower from followers where followed like "{}"'.format(x))
              r = cursor.fetchall()
              n = cursor.rowcount
                  
              room.message('{} [{}]: I found: {}  *h* !, Real name is {} , age {} with {} follower(s). {} has {} alternate account(s) recorded.({})'.format(rlpic,role,username,rlname,age,n,username,aliases,output))              
            if len(ip) < 1:
              cursor.execute('select follower from followers where followed like "{}"'.format(x))
              r = cursor.fetchall()
              n = cursor.rowcount
                  
              room.message('{} [{}]: I found: {}  *h* !, Real name is {} , age {} with {} follower(s). {} has {} alternate account(s) recorded'.format(rlpic,role,username,rlname,age,n,username,0))
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
    """
    Owner
    """
    def owner():
      room.message('Results: &nbsp; {} owns this room'.format(room.ownername))
    
    """
    Join & Leave
    """
    def roomManager(_,mode):
      try:
        url = "http://ust.chatango.com/groupinfo/"+_[0]+"/"+_[1]+"/"+_+"/gprofile.xml"
        resp = requests.get(url)
        if resp.status_code == 404:
          room.message('This room doesn\'t exist')
          return
        
        else:  
          if mode == 0:
            if _ in self.roomnames:
             room.message('I am already in {}'.format(_))
             return
            else:
              rooms.append(_)
              room.message('Joining {}...'.format(_))
              self.joinRoom(_)
          if mode == 1:
            if _ not in self.roomnames:
              room.message('I\'m not in {}'.format(_))
              return
            else:
              rooms.remove(_)
              room.message('Leaving {}...'.format(_))
              self.leaveRoom(_)
      except Error as e:
        room.message(str(e))
        
    """
    Popularity
       
    @return : Users with most followers    
    """    
    def popular():
      try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT followed, count(*) FROM followers GROUP BY followed ORDER BY count(*) DESC LIMIT 25")
        rows = cursor.fetchall()
        storage = []
        
        for count, x in enumerate(rows, 1):
          user = x[0]
          followers = x[1]
          storage.append(' #{} {} ({})  '.format(count,user,followers))
        
          
        room.message("Here are the top 25 most popular users! (based on followers) *h* : {}".format(",".join(storage)))  
      except Error as e:
        print e
      finally:
        conn.close()
        cursor.close()
    
    """
    change attribute
    
    """
    def attribute(_):
      _ , __ = _.split(" ", 1)
      if __ == 'color':
        self.setFontColor('{}'.format(_))
      if __ == 'font':
        self.setFontFace('{}'.format(_))
      if __ == 'size':
        self.setFontSize(_)  
      if __ == 'name':
        self.setNameColor('{}'.format(_))  
    
    
        
    """
    The bot commands
    @param result: runs function based on command
    @func lambda: Runs arguments if any in command
    @return: Returns output if command in dictionary
    
    """
    try:
      result = {
      prfx and 'say': lambda _:  _,
      prfx and 'test': lambda _: '<br/> <i>Working</i> <b> hey !',
      prfx and 'pm': lambda _: pmcmd(_),
      prfx and 'random': lambda _: str(random.randrange(int(_))),
      prfx and 'rooms': lambda _:  "I'm in "+ str(len(rooms)) +" rooms , " + ", ".join(rooms),
      prfx and 'yt': lambda _: yt(_),
      prfx and 'change': lambda _: attribute(_),
      prfx and 'join': lambda _: roomManager(_,0),
      prfx and 'leave': lambda _: roomManager(_,1),
      prfx and '+wos': lambda _: insert('wallofshame','message',_),
      prfx and 'wos': lambda _: simpleSelect('wallofshame','message',_),
      prfx and 'addadmin': lambda _: addadmin('users','username',_),
      prfx and 'owner': lambda _: owner(),
      prfx and 'mods' : lambda _: mods(_),
      prfx and 'nickname': lambda _: update('users','nickname','username',user.name,_,'nickname',0) ,
      prfx and 'age': lambda _: update('users','age','username',user.name,_,'age',0),
      prfx and 'rlname': lambda _: update('users','rlname','username',user.name,_,'rlname',0),
      prfx and 'rlpic': lambda _: update('users','rlpic','username',user.name,_,'rlpic',0),
      prfx and 'mood': lambda _: update('users','mood','username',user.name,_,'mood',0),
      prfx and 'status': lambda _: update('users','status','username',user.name,_,'status',0),
      prfx and 'notifications': lambda _: update('users','notifications','username',user.name,_,None,1),
      prfx and 'private': lambda _: update('users','nofollow','username',user.name,_,None,1),
      prfx and 'follow': lambda _: social('users','block','followers','username','nofollow','blocked','blocker','followed','follower',user.name,_,0),
      prfx and 'unfollow': lambda _: social('users','block','followers','username','nofollow','blocked','blocker','followed','follower',user.name,_,1),
      prfx and 'block': lambda _: manage('users','block','block','followers','username','blocked','blocker','followed','follower',user.name,_),
      prfx and 'unblock': lambda _: manage('users','block','unblock','followers','username','blocked','blocker','followed','follower',user.name,_),
      prfx and 'help': lambda _: help(),
      prfx and 'general': lambda _: gcmds(),
      prfx and 'social': lambda _: scmds(),
      prfx and 'merchant': lambda _: mcmds(),
      prfx and 'reboot':lambda _: restart(),
      prfx and 'followers':lambda _: followers(_,user.name,0),
      prfx and 'following':lambda _: followers(_,user.name,1),
      prfx and 'whoami':lambda _: who(user.name,0),
      prfx and 'whois':lambda _: who(_,1),
      prfx and 'popular':lambda _: popular()
      
      }[cmd](_)
  
      room.message(result)
    except:
      pass
  
  def onConnect(self,room):
    room.message("*waves*  Procfile declares types -> worker  I'm in test mode.  , ")
    print("ONLINE")
   
  
  
  
  ##############################################################################
  
  #PM SECTION BOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
  
  ##############################################################################
  
  def onPMMessage(self,pm,user,body):
    self.setNameColor("FFFFFF")
    self.setFontColor("666666")
    self.setFontFace("Verdana")
    self.setFontSize(10)
    self.enableBg()  
    self.enableRecording()
    
    try:
      cmd, args = body.split(" ", 1)
    except:
      cmd, args = body, ""      
   
    print "[PM] {} : {}".format(user.name,body) 
    """
    HTML PARSE
    
    Check for Unicode conversion for failsafe
    """
    h= HTMLParser.HTMLParser()
    
    prfx = h.unescape(cmd[:4]) == '>'
    cmd = cmd[4:] if prfx else cmd
    _ = args  
    
    """
    Registration
    
    @return: Confirmation of registration
    
    """
    def register():
      try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format('username','users','username',user.name))
        rows = cursor.fetchone()
            
        if(rows == None):
          a = "users" 
          b = "username" 
          d = user.name 
        
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('INSERT INTO {} ({}) VALUES("{}") '.format(a,b,d))
          conn.commit()
          self.pm.message(ch.User(user.name), 'You have just registered with companion. You will now be able to use social/merchant commands. *waves* Type >help for more information. You should definitely read my documentation at http://chatangu.tk/bot ')
            
        else:
          self.pm.message(ch.User(user.name), ' You are already registered with me!')
          
    
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
    
    """
    Check Registration
    
    @return: TRUE or error. 
    
    """
    
    def chkreg():
      try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format('username','users','username',user.name))
        rows = cursor.fetchone()
            
        if(rows == None):
          return False
            
        else:
          return True
          
    
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
    
    def test():
     if chkreg():
        self.pm.message(ch.User(user.name), 'Works *waves*')
     else:
        self.pm.message(ch.User(user.name), 'You need to register.')
    
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
        self.pm.message(ch.User(user.name), 'https://www.youtube.com' + vid['href'])
    
    """
    NOTIFICATION FUNCTION
    
    
    """
    
    def notify(message,var):
      dbconfig = read_db_config()
      conn = MySQLConnection(**dbconfig)
      cursor = conn.cursor()
      cursor.execute('select username from users where notifications=0 and username IN (select follower from followers where followed like "{}")'.format(var))
      results = cursor.fetchall()
      for result in results:
        self.pm.message(ch.User(str(result[0])), message)
    
    """ 
    SQL INSERT FUNCTION
    
    @param tablename: The target SQL table
    @param column: The target column in the table
    @param _: The user input
    @return: Returns confirmation that the record was added to the SQL table
    """
    
    def insert(tablename,column,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == "" ):
        self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('INSERT INTO {}({}) VALUES("{}") '.format(tablename,column,_))
          conn.commit()
          self.pm.message(ch.User(user.name),"Added {} to {} *pukes* ".format(_,tablename))      
          notify("{} just added...  {}  ..to the Wall of Shame! ;) ".format(user.name,_),user.name)
          
            
        except Error as e:
          print e
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
        self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) ORDER BY id DESC LIMIT 25'.format(column,tablename))
          rows = cursor.fetchall()
 
          if tablename == 'wallofshame':
            self.pm.message(ch.User(user.name),' :@ Here are the last 25 messages added to the Wall of Shame. To view the Wall , go to http://chatangu.tk/wallofshame')
            
            results = []
            for count, row in enumerate(rows, 1):
               
              results.append(str(count)+ ": " + row[0])
              
            self.pm.message(ch.User(user.name),'... '.join(results)) 
          else:
            self.pm.message(ch.User(user.name),'Last 3 records')
            results = []
            for row in rows:           
              results.append(row[0])
              
            self.pm.message(ch.User(user.name),', '.join(results))  
          
        except Error as e:
          print e
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
          
        self.pm.message(ch.User(user.name),'Current Admins *bored* ')    
        self.pm.message(ch.User(user.name),'... '.join(results)) 
          
          
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
   
    
    """
    Add admin Command 
    """
    def addadmin(tablename,column,_):
      _ , __ = _.split(" ", 1)
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format(column,tablename,column,_))
          rows = cursor.fetchone()
            
          if(rows == None):
            self.pm.message(ch.User(user.name),' *stop* That user doesn\'t exist')
          else:
            if(__ == ('moderator')):
              cursor.execute('UPDATE {} SET su = 1 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              self.pm.message(ch.User(user.name),'Set {} as Moderator! :) '.format(_))
            elif(__ == ('admin')):
              cursor.execute('UPDATE {} SET su = 2 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              self.pm.message(ch.User(user.name),'Set {} as Administrator! 8) '.format(_))
            elif(__ == ('superuser')):
              cursor.execute('UPDATE {} SET su = 3 WHERE {} = "{}"'.format(tablename,column,_))
              conn.commit()
              self.pm.message(ch.User(user.name),'Set {} as a SuperUser.. are you sure you meant to do this? :o '.format(_))  
        except Error as e:
          print e
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
    def update(tablename,column,column2,var,_,message,alert):
     
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          if _ ==  " ":
            self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
          if column == "notifications" and _ == 'on':
            cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            self.pm.message(ch.User(user.name)," ;) You turned notifications ON! (on by default if you didn't turn it off) You will now receive notifications when someone you are following has an update!  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ]")
          elif column == "notifications" and _ == 'off':
            cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            self.pm.message(ch.User(user.name)," :| You turned notifications OFF! You will not receive any notifications when someone you are following has an update.  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ]")
          elif column == "nofollow" and _ == 'on':
            cursor.execute('UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            self.pm.message(ch.User(user.name),'You tried: UPDATE {} SET {} = 1 WHERE {} = "{}"'.format(tablename,column,column2,var) )
            self.pm.message(ch.User(user.name)," :| You changed your profile to PRIVATE! You are not allowing anyone to follow you at this point. Are you sure you didn't mean to block someone instead?  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot] ") 
          elif column == "nofollow" and _ == 'off':
            cursor.execute('UPDATE {} SET {} = 0 WHERE {} = "{}"'.format(tablename,column,column2,var))
            conn.commit()
            self.pm.message(ch.User(user.name)," ;) You changed your profile to PUBLIC! You are allowing anyone to follow you (unless you block someone with the block command)  [ Confused? For more information, please visit my developer site here : http://chatangu.tk/bot ] ")   
              
          else:  
            
            cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}"'.format(tablename,column,_,column2,var))
            conn.commit()    
            self.pm.message(ch.User(user.name),'Updated your {} to {} ! *star* '.format(column,_))
            if alert == 0:
              notify("{} just updated his/her {} ! ".format(var,message),var)
            else:
              pass
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()    
    
    """
    Follow / Unfollow Command
    """
    def social(tablename,tablename2,tablename3,column,column2,column3,column4,column5,column6,var,_,n):
      _ = _.lower()
      
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        self.pm.message(ch.User(user.name),' *stop* You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          cursor.execute("""SELECT({}) FROM({}) 
          WHERE {} LIKE '{}'""".format(column,tablename,column,_))
          
          rows = cursor.fetchone()
          
          if(rows == None):
            self.pm.message(ch.User(user.name),' *stop* That user doesn\'t exist')
            cursor.close()
            conn.close()
          if(rows != None):
            i = rows[0]
          
          
            
          
          if i.lower() == _ :
            if n == 1:
              cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename3,column5,_,column6,var))
              conn.commit()
              self.pm.message(ch.User(user.name),'You unfollowed {}.. You will not receive anymore updates from this person  *hb* '.format(_))
            else:  
              
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}"'.format(column2,tablename,column,_))
              rows = cursor.fetchone()
              test = rows[0]
              if test == 0:
                a = True
              else:
                self.pm.message(ch.User(user.name),' *stop* This user is PRIVATE so you can\'t follow them')
                cursor.close()
                conn.close()
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,_,column3,var))
              rows = cursor.fetchone()
            
              if rows == None:
                b = True
              else:
                self.pm.message(ch.User(user.name),'This user has blocked you.. maybe talk to them and get back to me? *hb* ')
                cursor.close()
                conn.close()
            if(a and b == True):
              try:
                cursor.execute('INSERT INTO {}({},{}) VALUES("{}","{}") '.format(tablename3,column5,column6,_,var))
                conn.commit()
                self.pm.message(ch.User(user.name),'You are now following {}! You will receive notifications whenever this user has an update!  '.format(_))
                self.pm.message(ch.User(_),'{} is now following you'.format(user.name))
              except Error as e:
                self.pm.message(ch.User(user.name),' *stop* You have already followed this person!.')
              finally:
                cursor.close()
                conn.close()
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()
   
    def manage(tablename,tablename2,tablename3,tablename4,column,column3,column4,column5,column6,var,_):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table")) or _ == ""):
        self.pm.message(ch.User(user.name),'You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          cursor.execute("""SELECT({}) FROM({}) 
          WHERE {} LIKE '{}'""".format(column,tablename,column,_))
          
          rows = cursor.fetchone()
          
          if(rows == None):
            self.pm.message(ch.User(user.name),' *stop* That user doesn\'t exist')
            
          else:
            i = rows[0]
            if tablename3 == 'block':
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,var,column3,_))
              rows = cursor.fetchone()
              if rows == None:
                try:
                  cursor.execute('INSERT INTO {}({},{}) VALUES("{}","{}") '.format(tablename2,column3,column4,_,var))
                  conn.commit()
                  cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename4,column5,var,column6,_))
                  conn.commit()
                  
                  self.pm.message(ch.User(user.name),'Blocked {} *hb* This person cannot follow you or access your information. '.format(_))
                  
                except Error as e:
                  print(e)
              else:
                self.pm.message(ch.User(user.name),' *stop* You already blocked {}..  Did you mean to unblock?'.format(_))
            
            
            if tablename3 == 'unblock':
              cursor.execute('SELECT {} FROM({}) WHERE {} LIKE "{}" and {} like "{}"'.format(column3,tablename2,column4,var,column3,_))
              rows = cursor.fetchone()
              
              if rows == None:
                self.pm.message(ch.User(user.name),' *stop* You never blocked {}'.format(_))
              else:    
                cursor.execute('DELETE FROM {} WHERE {} LIKE "{}" and {} like "{}"'.format(tablename2,column4,var,column3,_))
                conn.commit()
                self.pm.message(ch.User(user.name),'You unblocked {}.. how sweet of you *h* *blush*'.format(_))
        
        finally:
          cursor.close()
          conn.close()   
   
      
    """
    The helper commands
    
    @return: Returns information about bot and main helper commands
          
    """
    def help():
      self.pm.message(ch.User(user.name),' *star* To see General Commands (like say) ,use >general . For Social Commands (like status) , use >social. \n For Merchant Commands (like Currency) , use >merchant. \n Keep in mind many commands may change and some will be eliminated for pm or chat usage only. Updates will be regularly added to my Documentation , http://chatangu.tk/bot ')
    def gcmds():
      self.pm.message(ch.User(user.name)," *star* General Commands: say, test, mods, random, yt, help, general, social, merchant, addadmin .")
    def scmds():
      self.pm.message(ch.User(user.name),"Social Commands: register, wos, +wos, nickname, age, rlname, rlpic, mood, status, notifications, private, follow,  followers, following, whoami, whois, popular unfollow, block, unblock  ")
    def mcmds():
      self.pm.message(ch.User(user.name),'NotImplemented')
   
    
    """
    View Followers Command
    
    Return: The user's followers or a selected user
    """
    def followers(_,var,x):
      if(_.lower().startswith(("insert into","select *","alter database","create database","create table","delete *","delete from","drop database","drop table"))):
        self.pm.message(ch.User(user.name),'You tried to perform an invalid operation... Try again or read my Documentation here.. http://chatangu.tk/bot')
      if ((user.name).startswith(('#','!'))):
        self.pm.message(ch.User(user.name),'No anons allowed ;)')
      else:
        try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          
          if (_ == "" and x == 0):
            cursor.execute('select follower from followers where followed = "{}"'.format(var))
            rows = cursor.fetchall()
            results = []
            self.pm.message(ch.User(user.name),'You have {} followers'.format(cursor.rowcount))
            for count, row in enumerate(rows, 1):
                     
              results.append('{}. {} '.format(count,row[0]))
            if(cursor.rowcount == 0):
              pass
            else:
              self.pm.message(ch.User(user.name),'... '.join(results))
         
          elif (_ == "" and x == 1):
            cursor.execute('select followed from followers where follower like "{}"'.format(var))
            rows = cursor.fetchall()
            results = []
            self.pm.message(ch.User(user.name),'You are following {} user(s)'.format(cursor.rowcount))
            for count, row in enumerate(rows, 1):
                     
              results.append(str(count)+ ": " + row[0])
                  
            if(cursor.rowcount == 0):
              pass
            else:
              self.pm.message(ch.User(user.name),'... '.join(results))   
         
          
          
          else:
            cursor.execute("SELECT({}) FROM({}) WHERE {} LIKE '{}'".format('username','users','username',_))
          
            rows = cursor.fetchone()
          
            if(rows == None):
              self.pm.message(ch.User(user.name),' *stop* That user doesn\'t exist')
            
            else:
             
              if(_ != "" and x == 0):
                cursor.execute('select follower from followers where followed = "{}"'.format(_))
                rows = cursor.fetchall()
                results = []
                self.pm.message(ch.User(user.name),'{} has {} followers'.format(_,cursor.rowcount))
                for count, row in enumerate(rows, 1):
                       
                  results.append(str(count)+ ": " + row[0])
                      
                if(cursor.rowcount == 0):
                  pass
                else:
                  self.pm.message(ch.User(user.name),'... '.join(results))
              elif (_ != "" and x == 1):
                cursor.execute('select followed from followers where follower like "{}"'.format(_))
                rows = cursor.fetchall()
                self.pm.message(ch.User(user.name),'{} is following {} user(s)'.format(_,cursor.rowcount))
                results = []
                
                for count, row in enumerate(rows, 1):
                       
                  results.append(str(count)+ ": " + row[0])
                        
                if(cursor.rowcount == 0):
                  pass
                else:
                  self.pm.message(ch.User(user.name),'... '.join(results))      
        
        except Error as e:
          print e
        finally:
          cursor.close()
          conn.close()
    
    """
    Whoami Command
    
    @return:  Returns the user's name , if no nickname , the user's rl name , age, rl pic, role, and if top percent of followed users  
    """  
    def who(x,y):
      try:
          dbconfig = read_db_config()
          conn = MySQLConnection(**dbconfig)
          cursor = conn.cursor()
          cursor.execute('select * from users where username like "{}"'.format(x))
          rows = cursor.fetchone()
          row = rows
          #assign
          rlpic = row[7]
          role = row[2]
          ip = row[1]
          username = row[3]
          rlname =  row[13]
          age = row[6]
          nickname = row[8]
          
          
          
          if role == 0:
            role = 'Role: User'
          if role == 1:
            role = 'Role: Moderator'
          if role == 2:
            role = 'Role: Admin'
          if role == 3:
            role = 'Role: Superuser'  
          if (username == 'Eaaj' or 'Debugger' or 'Classic'):
            role = "MASTER!"
          if nickname == None:
            nickname = ' [n/a] '
          if rlpic == None:
            rlpic = ' [n/a] '
          if age == None:
            age = ' [n/a] '
          if rlname == None:
            rlname = ' [n/a] '  
            
          
          if y == 0:  
            try:
              if len(ip) > 1:
                cursor.execute('select username from users where ip = "{}"'.format(ip))
                result = cursor.fetchall()  
                aliases = cursor.rowcount
                lst = []
                  
                for count, uname in enumerate(result, 1):
                  lst.append(" {}: {} ".format(count,uname[0]))
                output = "...".join(lst)
                
                cursor.execute('select follower from followers where followed = "{}"'.format(x))
                r = cursor.fetchall()
                n = cursor.rowcount
                print('you tried: select follower from followers where followed = "{}"'.format(x))
                for x in r:
                  print x[0]
                print n
                
                  
                self.pm.message(ch.User(user.name),'{} [{}]: Hey {} *h* , your name is {} , age {} with {} follower(s). You have {} alternate account(s) recorded.({})'.format(rlpic,role,username,rlname,age,n,aliases,output))  
              if len(ip) < 1:
                cursor.execute('select follower from followers where followed = "{}"'.format(x))
                r = cursor.fetchall()
                n = cursor.rowcount
                print('you tried: select follower from followers where followed = "{}"'.format(x))
                for x in r:
                  print x[0]
                print n
                
                  
                self.pm.message(ch.User(user.name),'{} [{}]: Hey {} *h* , your name is {} , age {} with {} follower(s). You have {} alternate account(s) recorded.({})'.format(rlpic,role,username,rlname,age,n,0,output)) 
                
            except Error as e:
              print e
              
          else:
            if len(ip) > 1:
              cursor.execute('select username from users where ip = "{}"'.format(ip))
              result = cursor.fetchall()  
              aliases = cursor.rowcount
              lst = []
                    
              for count, uname in enumerate(result, 1):
                lst.append(" {}: {} ".format(count,uname[0]))
              output = "...".join(lst)
                  
              cursor.execute('select follower from followers where followed like "{}"'.format(x))
              r = cursor.fetchall()
              n = cursor.rowcount
                
              self.pm.message(ch.User(user.name),'{} [{}]: I found: {}  *h* !, Real name is {} , age {} with {} follower(s). {} has {} alternate account(s) recorded.({})'.format(rlpic,role,username,rlname,age,n,username,aliases,output))              
          if len(ip) < 1:
              cursor.execute('select follower from followers where followed like "{}"'.format(x))
              r = cursor.fetchall()
              n = cursor.rowcount 
              self.pm.message(ch.User(user.name),'{} [{}]: I found: {}  *h* !, Real name is {} , age {} with {} follower(s). {} has {} alternate account(s) recorded.'.format(rlpic,role,username,rlname,age,n,username,0))  
      except Error as e:
        print e
      finally:
        cursor.close()
        conn.close()
    
    """
    Popularity
       
    @return : Users with most followers    
    """    
    def popular():
      try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT followed, count(*) FROM followers GROUP BY followed ORDER BY count(*) DESC LIMIT 25")
        rows = cursor.fetchall()
        storage = []
        
        for count, x in enumerate(rows, 1):
          user = x[0]
          followers = x[1]
          storage.append(' #{} {} ({})  '.format(count,user,followers))
        
          
        self.pm.message(ch.User(user.name),"Here are the top 25 most popular users! (based on followers) *h* : {}".format(",".join(storage)))  
      except Error as e:
        print e
      finally:
        conn.close()
        cursor.close()
    
    
    """
    The PM commands
    @param result: runs function based on command
    @func lambda: Runs arguments if any in command
    @return: Returns output if command in dictionary else skips
    
    """
    
    
    try:
           
      result = {
      prfx and 'say': lambda _:  _,
      prfx and 'test': lambda _:  test(),
      prfx and 'mods': lambda _:  mods(_),
      prfx and 'register': lambda _:  register(),
      prfx and 'random': lambda _: str(random.randrange(int(_))),
      prfx and 'yt': lambda _: yt(_),
      prfx and '+wos': lambda _: insert('wallofshame','message',_),
      prfx and 'wos': lambda _: simpleSelect('wallofshame','message',_),
      prfx and 'addadmin': lambda _: addadmin('users','username',_),
      prfx and 'nickname': lambda _: update('users','nickname','username',user.name,_,'nickname',0) ,
      prfx and 'age': lambda _: update('users','age','username',user.name,_,'age',0),
      prfx and 'rlname': lambda _: update('users','rlname','username',user.name,_,'rlname',0),
      prfx and 'rlpic': lambda _: update('users','rlpic','username',user.name,_,'rlpic',0),
      prfx and 'mood': lambda _: update('users','mood','username',user.name,_,'mood',0),
      prfx and 'status': lambda _: update('users','status','username',user.name,_,'status',0),
      prfx and 'notifications': lambda _: update('users','notifications','username',user.name,_,None,1),
      prfx and 'private': lambda _: update('users','nofollow','username',user.name,_,None,1),
      prfx and 'follow': lambda _: social('users','block','followers','username','nofollow','blocked','blocker','followed','follower',user.name,_,0),
      prfx and 'unfollow': lambda _: social('users','block','followers','username','nofollow','blocked','blocker','followed','follower',user.name,_,1),
      prfx and 'block': lambda _: manage('users','block','block','followers','username','blocked','blocker','followed','follower',user.name,_),
      prfx and 'unblock': lambda _: manage('users','block','unblock','followers','username','blocked','blocker','followed','follower',user.name,_),
      prfx and 'help': lambda _: help(),
      prfx and 'general': lambda _: gcmds(),
      prfx and 'social': lambda _: scmds(),
      prfx and 'merchant': lambda _: mcmds(),
      prfx and 'followers':lambda _: followers(_,user.name,0),
      prfx and 'following':lambda _: followers(_,user.name,1),
      prfx and 'whoami':lambda _: who(user.name,0),
      prfx and 'whois':lambda _: who(_,1),
      prfx and 'popular':lambda _: popular()
      
      }[cmd](_)
    
      self.pm.message(ch.User(user.name), result)
        
    except:
      pass
    
 
###############################################################################


#start it up


###############################################################################
    
rooms = ["network"]
username = "dashboard"
password = "one.piece1"

bot.easy_start(rooms,username,password)