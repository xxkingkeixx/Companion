a = raw_input("Add your command with arguments here")


def check(a):
    if a == 'lol':
        return True
    else:
        return False
        
if check(a):
    print 'True!'
else:
    print 'False!'