#Creating teams
import os

print("Enter team name : ")
tname=input()
print("Enter username and password : ")
uspass=input().split()
if not os.path.exists('./uploads/'+tname):
    #Store creds and points in a txtfile
    os.makedirs('./uploads/'+tname)
    os.makedirs('./results/'+tname)
    fo=open('./uploads/'+tname+'/tdata.txt','w')
    fo.write('0')
    fo.close()
    fo=open('./uploads/teams.txt','a')
    fo.write(tname+' '+uspass[0]+' '+uspass[1]+'\n')
    fo.close()
else:
    print("Team already exists")
