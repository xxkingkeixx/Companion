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
              
              cursor.execute('select username from users where ip = "{}"'.format(message.ip))
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
            
            except Error as e:
              print e
              
          else:
            
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