#Cron job to evaluate submitted programs

import time,subprocess
import os

#Function to validate output when fed given input
def testOtpt(name,inpu,outpu,tname):
    #Using cmd to run the file
    p = subprocess.Popen('python uploads/'+tname+'/'+name, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        output,err=p.communicate(input=inpu,timeout=2)
        if (output):
            if(output==outpu):
                return True
            else:
                return False
        else:
            #Catching syntax/runtime errors
            #i=err.index(b'C:\\Users\\Praneeth\\Desktop\\Exts\\node\\cron\\entries')
            #err=err[:i]+err[i+26:]
            write(name,err.decode('UTF-8'),tname)
            
    except subprocess.TimeoutExpired as e:
        #Catching infinite loops/ time hog programs
        p.kill()
        write(name,e,tname)

def write(name,val,tname):
    #Simple file write function
    fo=open('results/'+tname+'/'+name[:len(name)-3]+'.txt','w')
    fo.write(val)
    fo.close()

def updatescore(tname,pts):
    #Score updation
    fo1=open('./uploads/'+tname+'/tdata.txt','r')
    data=fo1.readlines()
    score=int(data[0])
    fo1.close()    
    fo2=open('./uploads/'+tname+'/tdata.txt','w')
    fo2.write(str(score+pts))
    fo2.close()

while 1:
    #Control duration between loops
    time.sleep(5)
    print('Waiting')
    teams = os.scandir('uploads/')
    for team in teams:
        entries = os.scandir('uploads/'+team.name+'/')
        for entry in entries:
            #Flag to check if already evaluated
            fl=0
            outputs = os.scandir('results/'+team.name+'/')
            for otpt in outputs:
                if (entry.name[:len(entry.name)-2]==otpt.name[:len(otpt.name)-3] or entry.name=='tdata.txt'):
                    fl=1
                    break
            if not fl:
                #Evaluation
                if (entry.name[:3]=='abc'):
                    if (testOtpt(entry.name,b'12\n13',b'Sum is 25\r\n',team.name)==True):
                        write(entry.name,'Test Set Passed',team.name)
                        updatescore(team.name,10)
                    elif (testOtpt(entry.name,b'12\n13',b'Sum is 25\r\n',team.name)==False):
                        write(entry.name,'Test Set Failed',team.name)


