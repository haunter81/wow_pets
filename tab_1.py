import os
import requests
from prettytable import PrettyTable
import pandas as pd

def print_list():
      pets= []
      price1=[]
      if os.path.exists('custom_pet_list.txt'): 
            with open ('custom_pet_list.txt') as f:
               for line in f:
                   line = line.rstrip().split(",")
                   pets.append(line[0])
                   price1.append(line[1])
      else:
            text1 = "there isn't any custom list saved"
            return text1  
      tab1 = PrettyTable() #check for merge
      tab1.field_names = (["Pet", "Price"])
      c_pet_dict =dict(zip(pets,price1))
      for c_pet in c_pet_dict:
           tab1.add_row([c_pet ,c_pet_dict[c_pet]])
      text1 =tab1.get_string(sortby="Pet")
      return text1

def remove_pet_list(choice):
      pets =[]
      price1=[]
      if os.path.exists('custom_pet_list.txt'): 
            with open ('custom_pet_list.txt', "r") as f:
               for line in f:
                   line = line.rstrip().split(",")
                   pets.append(line[0])
                   price1.append(line[1])
      else:
            text1 = "there isn't any custom list saved"
            return text1
      c_pet_dict =dict(zip(pets,price1))
      if choice in c_pet_dict:
         del c_pet_dict[choice]
         #keys = c_pet_dict.keys()
         #values = c_pet_dict.values()
         os.remove('custom_pet_list.txt')
         for c_pet in c_pet_dict:
             newlist = c_pet,c_pet_dict[c_pet]
             s = ",".join(map(str, newlist)) 
             with open ('custom_pet_list.txt' , 'a') as f:
                f.write(s+ "\n")
                f.close() 
         text1 ="done"
         return text1  
def fetchall(region2): ##### 0550
      server_name= []
      server_code=[]
      tab1 = PrettyTable()
      tab1.field_names = (["Server", "Pet","Price"])
      pets=[]
      price1=[]
      if os.path.exists('custom_pet_list.txt'): 
            with open ('custom_pet_list.txt') as f:
               for line in f:
                   line = line.rstrip().split(",")
                   pets.append(line[0])
                   price1.append(line[1])
      
      c_pet_dict =dict(zip(pets,price1)) ## times apo tin lista
      if not os.path.exists('custom_pet_list.txt'):
         text1 =  "Please create a list first!"
         #self.textBrowser_2.append("Please create a list first!")
         return text1
      if os.path.exists('server_set.txt'):
          with open ('server_set.txt') as f:
               for lines in f:
                    lines = lines.rstrip().split(",")
                    server_name.append(lines[0])
          del server_name[0]
      if not os.path.exists('server_set.txt') and region2 =="EU":
         outputfile="http://haunter.mywire.org:8558/output.csv"
         response3 = requests.get('http://haunter.mywire.org:8558/server.txt')
         response3=response3.text
      if not os.path.exists('server_set.txt') and region2 =="US":
         outputfile="http://haunter.mywire.org:8558/output_us.csv"
         response3 = requests.get('http://haunter.mywire.org:8558/server_us.txt')
         response3=response3.text
      if not os.path.exists('server_set.txt'):
        with open("file3.txt", "w") as write_file:
             write_file.write(response3)
        with open ("file3.txt") as f:
           for lines in f:
               lines = lines.rstrip().split(",")
               server_name.append(lines[0])             
      if os.path.exists('server_set.txt'):
         outputfile="http://haunter.mywire.org:8558/output.csv"
         data = pd.read_csv(outputfile)
         server_csv = list(data.columns)
         server_csv.remove('Pet Name')
         reg=0
         if server_name[0] in server_csv:
           reg == 1
           for server_c in server_name:
               server_dict=dict(zip(data['Pet Name'], data[server_c])) #times apo to output
               for pet_c in c_pet_dict:
                   price2 = float(server_dict[pet_c])
                   price3 = float(c_pet_dict[pet_c])
                   #print ("pet:",pet_c,"server:",server_c,"price:",price2)
                   if price2 < price3 and price2 !=0:
                      tab1.add_row([server_c ,pet_c,price2])
           text1 =  tab1.get_string(sortby="Pet") 
           #self.textBrowser_2.append(tab1.get_string(sortby="Pet"))                     
           return text1
         if reg == 1:
            pass
         else:
             outputfile="http://haunter.mywire.org:8558/output_us.csv"
             data = pd.read_csv(outputfile)
             server_csv = list(data.columns)
             server_csv.remove('Pet Name')
             if server_name[0] in server_csv:
                for server_c in server_name:
                    server_dict=dict(zip(data['Pet Name'], data[server_c])) #times apo to output
                    for pet_c in c_pet_dict:
                        price2 = float(server_dict[pet_c])
                        price3 = float(c_pet_dict[pet_c])
                        if price2 < price3 and price2 !=0:
                           tab1.add_row([server_c ,pet_c,price2])
                text1 =  tab1.get_string(sortby="Pet")
                #self.textBrowser_2.append(tab1.get_string(sortby="Pet"))                     
                return text1
      data = pd.read_csv(outputfile)
      server_csv = list(data.columns)
      server_csv.remove('Pet Name')
      if server_name[0] in server_csv:
         for server_c in server_name:
             server_dict=dict(zip(data['Pet Name'], data[server_c])) #times apo to output
             for pet_c in c_pet_dict:
                 price2 = float(server_dict[pet_c])
                 price3 = float(c_pet_dict[pet_c])
                 #print ("pet:",pet_c,"server:",server_c,"price:",price2)
                 if price2 < price3 and price2 !=0:
                    tab1.add_row([server_c ,pet_c,price2])
         text1 =  tab1.get_string(sortby="Pet")
         #self.textBrowser_2.append(tab1.get_string(sortby="Pet"))                     
         return text1      
