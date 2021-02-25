import time,subprocess
import os

def testOtpt(name,inpu):
    p = subprocess.Popen('python entries/'+name, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        output,err=p.communicate(input=inpu,timeout=2)
        if (output):
            fo=open('outputs/'+name[:len(name)-3]+'.txt','w')
            fo.write(output.decode('UTF-8'))
            fo.close()
        else:
            fo=open('outputs/'+name[:len(name)-3]+'.err','w')
            #i=err.index(b'C:\\Users\\Praneeth\\Desktop\\Exts\\node\\cron\\entries')
            #err=err[:i]+err[i+26:]
            fo.write(err.decode('UTF-8'))
            fo.close()
    except subprocess.TimeoutExpired as e:
        p.kill()
        fo=open('outputs/'+name[:len(name)-3]+'.err','w')
        fo.write(e)
        fo.close()

while 1:
    time.sleep(3)
    print('Waiting')
    entries = os.scandir('entries/')
    outputs = os.scandir('outputs/')
    for entry in entries:
        fl=0
        for otpt in outputs:
            if (entry.name[:len(entry.name)-2]==otpt.name[:len(otpt.name)-3]):
                fl=1
        if not fl:
            if (entry.name=='abc.py'):
                testOtpt(entry.name,b'12\n13')
            else:
                testOtpt(entry.name,b'')

