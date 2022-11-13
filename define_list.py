import os
import requests

def define_list(region2):
        #region2 = self.comboBox_2.currentText()
        server_name=[]
        server_code=[]
        if os.path.exists('server_set.txt'):
              server_name= []
              server_code=[]
              with open ('server_set.txt') as f:
                   for lines in f:
                       lines = lines.rstrip().split(",")
                       server_name.append(lines[0])
                       server_code.append(lines[1])
              region2=server_name[0]
              del server_name[0]
              del server_code[0]
              return server_name , server_code, region2
        if region2 and not os.path.exists('server.txt'):#choose eu or us
           if region2=="EU":
              response3 = requests.get('http://haunter.mywire.org:8558/server.txt')
              response3=response3.text
           if region2=="US":
              response3 = requests.get('http://haunter.mywire.org:8558/server_us.txt')
              response3=response3.text
           with open("file3.txt", "w") as write_file:
                write_file.write(response3)
           with open ("file3.txt") as f:
                for lines in f:
                    lines = lines.rstrip().split(",")
                    server_name.append(lines[0])
                    server_code.append(lines[1])
           return server_name , server_code , region2          
        if region2=="EU" and os.path.exists('server.txt'): 
           with open ('server.txt') as f:
                for lines in f:
                    lines = lines.rstrip().split(",")
                    server_name.append(lines[0])
                    server_code.append(lines[1])
           return server_name , server_code , region2           
        if region2=="US" and os.path.exists('server_us.txt'): 
           with open ('server_us.txt') as f:
                for lines in f:
                    lines = lines.rstrip().split(",")
                    server_name.append(lines[0])
                    server_code.append(lines[1])
           return server_name , server_code , region2
