################################################################################


#PM Log System/Auth System/Ping
#ignore this

################################################################################

    
def onPMMessage(self, pm, user, body):
        self.setFontSize(12)
        self.setFontColor("000000")
        self.setFontFace('Times')
        
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
            pm.message(user, "Good")
            
            pmlogger = open('LOGGER.html', 'a')
            
            adminlogger = open('ADMINLOG.txt', 'a')
            
            time = str(datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%y'))
            
            pmFormatting = user.name.capitalize()+":  "+body+"  ["+time+"]"
            
            pmlogger.write("<p align='center' style='color:white'><font size='8'>"+user.name.capitalize()+" "+"was here"+"</font></p><br><br>")
            
            adminlogger.write(pmFormatting+"\n")
            
            adminlogger.close()
            
            pmlogger.close()
        
        print("[PM]"+user.name.capitalize()+": "+body) 
    
     