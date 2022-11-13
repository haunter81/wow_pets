import os
import requests

def create_pet_list(kind,expa):

        OPTIONS =[]
        pet1s=[]
        code=[]
        petkind=[]
        petexpans=[]
        if os.path.exists('data.txt'): 
          with open ('data.txt') as f:
             for line in f:
                  line = line.rstrip().split(",")
                  OPTIONS.append(line[0])
                  pet1s.append("["+line[0]+"]")
                  code.append(line[1])
                  petkind.append(line[2])
                  petexpans.append(line[3])
          return OPTIONS , pet1s, code
                
        if not os.path.exists('data.txt') and not os.path.exists('file2.txt'):
           try:
              response2 = requests.get('http://haunter.mywire.org:8558/data.txt')
              grabpetdata = 1
           except ValueError:
              print ("Problem loading pet file...")
              exit()
           response2=response2.text
           with open("file2.txt", "w") as write_file:
                write_file.write(response2)
        with open ("file2.txt") as f:
                for line in f:
                    line = line.rstrip().split(",")
                    #linef =str(line[3])
                    #expa = str(expa)
                    #lined = str(line[2]) 
                    #print (line[3] ," ", expa)
                    if kind == 'All' and expa == 'All':
                       OPTIONS.append(line[0])
                       pet1s.append("["+line[0]+"]")
                       code.append(line[1])
                       petkind.append(line[2])
                       petexpans.append(line[3])
                    if kind == line[2]  and expa == line[3]:
                       OPTIONS.append(line[0])
                       pet1s.append("["+line[0]+"]")
                       code.append(line[1])
                    if kind == 'All' and line[3] == expa:
                       OPTIONS.append(line[0])
                       pet1s.append("["+line[0]+"]")
                       code.append(line[1])
                    if kind == line[2] and expa =='All':
                       OPTIONS.append(line[0])
                       pet1s.append("["+line[0]+"]")
                       code.append(line[1])
        return OPTIONS , pet1s, code 
