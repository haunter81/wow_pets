from wow_gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtGui import QFont #fix gui win bug
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
import pandas as pd
import tab_1
import os 
import create_pet_list
import define_list
from prettytable import PrettyTable
import datetime
import csv
import requests
import scrape_data

# se autin tin version(0560) moirasa ton kodika se wow_gui(gui) wow_pets(main with some fuctions) kai ta arxeia
#tab_1 -> tab_1 fuctions
#create_pet_list ...
#define_list (servers)


version = int('0560')
grabpetdata=0
OPTIONS=[]
pet1s=[]
code=[]
i=1
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if os.path.exists('server_set.txt'):
           self.ui.label_11.setText("Custom List is loaded")
           self.ui.comboBox_2.setEnabled(False)
           self.ui.textBrowser.append("Custom List is loaded | Region is deactivated")
           self.ui.pushButton_8.setEnabled(True)
        else:
           self.ui.label_11.setText("Default list is loaded")
        self.ui.pushButton_2.clicked.connect(self.deals) #
        self.ui.pushButton_3.clicked.connect(self.scanpet) #
        self.ui.pushButton_4.clicked.connect(self.petinfo) #
        self.ui.pushButton_5.clicked.connect(self.allcheap) #
        self.ui.pushButton_6.clicked.connect(self.load_list) #
        self.ui.pushButton_7.clicked.connect(self.save_list) #
        self.ui.pushButton_8.clicked.connect(self.delete_list)
        self.ui.pushButton_9.clicked.connect(self.versus_list)
        self.ui.add_pet_bn.clicked.connect(self.add_pet_list)
        self.ui.Print_list_bn.clicked.connect(self.print_list)
        self.ui.Remove_pet_bn.clicked.connect(self.remove_pet_list)
        self.ui.fetch_bn.clicked.connect(self.fetchall)
        #self.ui.delete_list_bn.clicked.connect(self.delete_all_list)
        self.ui.refreshlist.clicked.connect(self.populate_list)
        self.ui.sort_bn.clicked.connect(self.create_pet_list)

        self.ui.listWidget.addItems(OPTIONS)#
        #self.model = QStandardItemModel(self.listWidget)
        self.ui.textBrowser.setFontFamily("monospace")
        self.ui.textBrowser.setFont(QtGui.QFont("monospace", 10)) ####
        self.ui.textBrowser_2.setFontFamily("monospace")
        self.ui.textBrowser_2.setFont(QtGui.QFont("monospace", 10))
        self.ui.label_3.setText("Day - Time")
        fixed_font = QFont("monospace", 10) ##fix gui-bug
        fixed_font.setStyleHint(QFont.TypeWriter)##fix gui-bug
        self.ui.textBrowser.setFont(fixed_font)##fix gui-bug
        self.ui.textBrowser_2.setFont(fixed_font) ###0550
        ##filter
        self.ui.lineEdit.textChanged.connect(self.change)
        self.ui.checkBox_2.setChecked(True)
        self.populate_list()

    def delete_all_list():
        if os.path.exists('custom_pet_list.txt'):
           os.remove('custom_pet_list.txt')
           self.ui.textBrowser_2.append("Shopping list deleted")
        else:
           self.ui.textBrowser_2.append("Shopping list already deleted!")
    def change(self, text):
        self.ui.listWidget.clear()
        e = QtCore.QRegularExpression(text)
        filter_files = [f for f in OPTIONS if e.match(f).hasMatch()]
        self.ui.listWidget.addItems(filter_files)
        if os.path.exists('server_set.txt'):
           self.ui.label_11.setText("Custom List is loaded")
        else:
           self.ui.label_11.setText("Default list is loaded")


    def add_pet_list(self):
        try:
           choice = self.ui.listWidget.currentItem().text()
        except AttributeError:
           self.ui.textBrowser_2.append("Please choose a pet")
           return
        price1 = self.ui.pet_price_lineedit.text()
        try:
           price1 = int(price1)
        except ValueError:
           self.ui.textBrowser_2.append("Please enter price")
           return
        newlist = choice,price1
        s = ",".join(map(str, newlist))     
        with open ('custom_pet_list.txt' , 'a') as f:
           f.write(s+ "\n")
           f.close()
        text1= s+" Gold"+" added"
        self.ui.textBrowser_2.append(text1)
        self.ui.pet_price_lineedit.setText("") ### 0550

    def print_list(self):
       text1 = tab_1.print_list()
       self.ui.textBrowser_2.append(text1)

    def remove_pet_list(self):
      try:
           choice = self.ui.listWidget.currentItem().text()
      except AttributeError:
           self.ui.textBrowser_2.append("Please choose a pet")
           return
      try:
         text1 = tab_1.remove_pet_list(choice)
      except UnboundLocalError:
         self.ui.textBrowser_2.append("Please choose a pet")
         return
      self.ui.textBrowser_2.append(text1)

    def fetchall(self): ##### 0550
      region2 = self.ui.comboBox_2.currentText()
      text1 = tab_1.fetchall(region2)
      self.ui.textBrowser_2.append(text1)
#####################################################################################################2nd_tab

    def versus_list(self):
      server1=self.ui.comboBox_3.currentText()
      server2=self.ui.comboBox_4.currentText()
      region2 = self.ui.comboBox_2.currentText()

      tab1 = PrettyTable() #check for merge
      tab1.field_names = (["Pet", "Price1","Price2" , "Dif" ])
      if region2 =="EU":
         outputfile="http://haunter.mywire.org:8558/output.csv"
      if region2 =="US":
         outputfile="http://haunter.mywire.org:8558/output_us.csv"
      data = pd.read_csv(outputfile)
      server1_dict =dict(zip(data['Pet Name'],data[server1]))
      server2_dict =dict(zip(data['Pet Name'],data[server2]))
      for pet1 in server1_dict:
          dif = server1_dict[pet1] - server2_dict[pet1]
          tab1.add_row([pet1 ,server1_dict[pet1],server2_dict[pet1],dif])
      self.ui.textBrowser.append(tab1.get_string(sortby="Pet"))

    def check_version(self):
        response3 = requests.get('http://haunter.mywire.org:8558/version.txt')
        response3=int(response3.text)
        if response3 != version:
           response3 = requests.get('http://haunter.mywire.org:8558/link.txt')
           response3 = response3.text
           htmllink= "<a href=\""+response3+"\">Download update</a>"
           self.ui.label_18.setText(htmllink)
           self.ui.label_12.setText("New update found!please update your app for new features!")
    def populate_list(self):
      region2 = self.ui.comboBox_2.currentText()
      self.ui.comboBox_3.clear()
      self.ui.comboBox_4.clear()
      server_name=[]
      server_code =[]
      server_name , server_code,region2 = define_list.define_list(region2)              
      self.ui.comboBox_3.addItems(server_name)
      self.ui.comboBox_4.addItems(server_name)

    def delete_list(self):
      if os.path.exists('server_set.txt'):
         os.remove('server_set.txt')
         self.ui.label_11.setText("Default List is loaded")
         self.ui.comboBox_2.setEnabled(True)
         self.populate_list()

      
    def save_list(self):
        with open('server_set.txt','w'): pass
        list_1 = [item.text() for item in self.ui.listWidget.selectedItems()]
        server_name, server_code = self.load_list()
        default_list = dict(zip(server_name,server_code))
        
        with open('server_set.txt', 'a',newline='') as f: ####0552
             writer = csv.writer(f, delimiter=',')
             region2 = self.ui.comboBox_2.currentText()
             output = [region2,'0']
             writer.writerow(output)
        for item in list_1:
            #new_list = [item,default_list[item]]
            new_list =[item,default_list[item]]          
            #with open ('settings.txt', 'a') as f:
             #    f.write(str(new_list)+ "\n")
              #   f.close()
            with open('server_set.txt', 'a',newline='') as f:
                writer = csv.writer(f, delimiter=',') ####0550 
                output = new_list
                writer.writerow(output)
        self.ui.listWidget.clear()       
        self.ui.listWidget.addItems(OPTIONS)
        self.ui.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.textBrowser.append("List Saved!")
        self.ui.label_11.setText("Custom List is loaded")
        self.ui.comboBox_2.setEnabled(False)
        self.ui.pushButton_8.setEnabled(True)

        self.populate_list()



    def load_list(self):
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.listWidget.clear()
        self.ui.pushButton_7.setEnabled(True)
        self.ui.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        server_name=[]
        server_code=[]
        region2 = self.ui.comboBox_2.currentText()
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
        self.ui.listWidget.addItems(server_name)#

        return server_name, server_code
      
    def update_time(self):
        region2 = self.ui.comboBox_2.currentText()
        if region2=="EU":
           time_now = requests.get('http://haunter.mywire.org:8558/time_now.txt')
           time_now = time_now.text
        if region2=="US":
           time_now = requests.get('http://haunter.mywire.org:8558/time_now_us.txt')
           time_now = time_now.text
        self.ui.label_3.setText(time_now)

    def scanpet(self):
        self.update_time()
        global choice
        try:
           choice = self.ui.listWidget.currentItem().text()
        except AttributeError:
           self.ui.textBrowser.append("Please choose a Pet first")
           return
        choice = self.ui.listWidget.currentItem().text()
        region2 = self.ui.comboBox_2.currentText()
        if self.ui.checkBox.isChecked(): ##grab data from server
           from prettytable import PrettyTable
           tab3 = PrettyTable() #check for merge
           tab3.field_names = ["Server","Price", ]
           server_name , server_code, region2 = define_list.define_list(region2)              
           import pandas as pd
           if region2=="EU":
              file1="http://haunter.mywire.org:8558/output.csv"
           if region2=="US":
              file1="http://haunter.mywire.org:8558/output_us.csv"
           data = pd.read_csv(file1, index_col='Pet Name')
           data = data.fillna(0) ##fix nan
           total = 0
           times = 0
           for cserver in server_name:
               pricec = data.at[choice, cserver] #choice1
               tab3.add_row([cserver , pricec])
               total = total + pricec
               times = times + 1
           self.ui.textBrowser.append(choice)
           self.ui.textBrowser.append(tab3.get_string(sortby="Price"))
           tab3.clear_rows()
           return
        scrapeoffline.scanpet(choice)
        from scrapeoffline import tab3 
        self.ui.textBrowser.append(choice)
        self.ui.textBrowser.append(tab3.get_string(sortby="Price"))
        tab3.clear_rows()

    def deals(self):
        #self.check_version()
        self.update_time()
        region2 = self.ui.comboBox_2.currentText()
        OPTIONS = self.create_pet_list()
        data,data1,data2 = self.deals_manual(region2,OPTIONS)
        self.ui.textBrowser.append(data)
        self.ui.pushButton.setEnabled(True)

    def petinfo(self):
        self.update_time()
        global choice
        try:
           choice = self.ui.listWidget.currentItem().text()
        except AttributeError:
           self.ui.textBrowser.append("Please choose a Pet first")
           return
        self.ui.pushButton_4.setText("Scanning...")
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_4.repaint()
        #global choice
        choice = self.ui.listWidget.currentItem().text()
        scrape_data.scrapepetinfo(choice)
        from scrape_data import apperancerating , battlerating , finaltext ,pdict
        self.ui.textBrowser.append(choice) #gui print pet name
        self.ui.textBrowser.append(apperancerating)
        self.ui.textBrowser.append(battlerating)
        self.ui.textBrowser.append(finaltext)
        try:
           self.ui.textBrowser.append("Average pet value:"+pdict['Average pet value'])
        except KeyError:
          pass
        try:
           self.ui.textBrowser.append("Average level 25 value:"+pdict['Average level 25 value'])
        except KeyError:
          pass
        self.ui.textBrowser.append("---------------------------------------")
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_4.setText("Pet Info")

    def allcheap(self):
      region2 = self.ui.comboBox_2.currentText()
      self.update_time()
      choice1=self.ui.comboBox.currentText()
      #scrapeoffline.hotdeals(valuespin)##
      if self.ui.checkBox.isChecked() and choice1=="server":
         if region2=="EU" and testing==0:
            response1 = requests.get('http://haunter.kozow.com:8558/server_deals.txt')
            response1=response1.text
         if region2=="US" and testing==0:
            response1 = requests.get('http://haunter.kozow.com:8558/server_deals_us.txt')
            response1=response1.text
         if testing ==1:
            data,data1,data2 = self.deals_manual(region2,OPTIONS)
            self.ui.textBrowser.append(data1)
            return
         self.ui.textBrowser.append(response1)
         return
      if self.ui.checkBox.isChecked() and choice1=="pet":
         if region2=="EU":
            response1 = requests.get('http://haunter.kozow.com:8558/pet_deals.txt')
            response1=response1.text
         if region2=="US":
            response1 = requests.get('http://haunter.kozow.com:8558/pet_deals_us.txt')
            response1=response1.text
         if testing ==1:
            data,data1,data2 = self.deals_manual(region2,OPTIONS)
            self.ui.textBrowser.append(data2)
            return
         self.ui.textBrowser.append(response1)
         return
      from scrapeoffline import tab5
      #print(choice1)
      if choice1=="server":
            self.ui.textBrowser.append(tab5.get_string(sortby="Server"))     
      if choice1=="pet":
            self.ui.textBrowser.append(tab5.get_string(sortby="Pet"))     
      #tab5.clear_rows()
      self.ui.pushButton.setEnabled(True)

    def deals_manual(self , region2, OPTIONS):
     ###pretty table load

      valuespin = self.ui.spinbox.value()
      tab4 = PrettyTable() #check for merge
      tab4.field_names = (["Server", "Pet", "Price" ])
      tab5=PrettyTable()
      tab5.field_names = (["Server", "Pet", "Price" ])
      tab6 = PrettyTable()
      tab6.field_names = (["Server", "Pet", "Price"  , "%"])
      tab3 = PrettyTable() #check for merge
      tab3.field_names = ["Server","Price", ]
     ###pretty table load
      server_name , server_code, region2 = define_list.define_list(region2)              
      #region2 = self.comboBox_2.currentText()
      if region2 =="EU":
         median_csv="http://haunter.mywire.org:8558/output_median.csv"
         outputfile="http://haunter.mywire.org:8558/output.csv"
      if region2 =="US":
         median_csv="http://haunter.mywire.org:8558/output_median_us.csv"
         outputfile="http://haunter.mywire.org:8558/output_us.csv"
      tab5.clear_rows()
      tab6.clear_rows()
      tab4.clear_rows()
      today = datetime.datetime.now()
      header1 = today.strftime('%d-%m-%Y %H:%S')
      data = pd.read_csv(outputfile)
      #vrisko olous tou server pou kano scrape kai ftiaxno mia lista
      server_csv = list(data.columns)
      server_csv.remove('Pet Name')
      #vrisko tis xamiloteres times kai ftiaxno dict
      data['Dmin'] = data[data != 0].min(axis=1)
      pet_min_dict=dict(zip(data['Pet Name'], data['Dmin']))
      #fortono tis times apo to median_csv
      df1 = pd.read_csv(median_csv)
      
##unused code for now /

      server_csv=server_name
      cheapname =[]
      cheapprice =[]
      cheapserver =[]
      for server in server_csv:
        pet_dict=dict(zip(data['Pet Name'], data[server]))
        for key, value in pet_min_dict.items():
          if pet_dict[key] == pet_min_dict[key]:
            tab4.add_row([server , key , pet_dict[key]])
            cheapname.append(key)
            cheapprice.append(server)
            cheapserver.append(pet_dict[key])
      cheap1_dict=dict(zip(cheapname,cheapprice)) #cheapest pets with  server
      cheap2_dict=dict(zip(cheapname,cheapserver))#cheapest pets with price
##unused code for now 
      df1['Median'] = df1[data != 0].min(axis=1)
      pet_med_dict=dict(zip(data['Pet Name'], df1['Median']))
      for cheappet in cheap1_dict:
        curcheapv = float(cheap2_dict[cheappet]) # current cheap price
        medianprice = float(pet_med_dict[cheappet])
        curcheapserver = cheap1_dict[cheappet]
        if curcheapv <= medianprice and curcheapv <10000 and curcheapv >100 and medianprice !=0 and cheappet in OPTIONS: ##0554 error
           tab5.add_row([curcheapserver , cheappet, curcheapv])
###fix , otan medianprice itan 0 den mporouse na dierethei kai kolage to programa      
        if medianprice ==0 and curcheapv !=0:
           medianprice = curcheapv
        if medianprice ==0 and curcheapv ==0:
           medianprice ==1
           curcheapv == 1  
        alert1 = float((medianprice-curcheapv)/medianprice)
        alert1= alert1*100
        #if alert1>39 and curcheapv>101: # itan 30
        if alert1>valuespin and curcheapv>101 and cheappet in OPTIONS: # itan 30
           alert2 = round(alert1)
           tab6.add_row([curcheapserver , cheappet, curcheapv ,alert2])
        if curcheapv>10 and alert1>90 and cheappet in OPTIONS:# itan <100 kai >80
           alert2 = round(alert1)
           tab6.add_row([curcheapserver , cheappet, curcheapv ,alert2])
        if alert1>70 and curcheapv>101 and cheappet in OPTIONS:
           alert2 = round(alert1)
      data = tab6.get_string(sortby="Price")
      data1=tab5.get_string(sortby="Server")
      data2=tab5.get_string(sortby="Pet")
      return data , data1 , data2

    def create_pet_list(self):
      kind = self.ui.pet_sort_kind.currentText()
      expa = self.ui.pet_sort_expa.currentText()        
      OPTIONS , pet1s, code = create_pet_list.create_pet_list(kind,expa) #0555
      self.ui.listWidget.clear()
      self.ui.listWidget.addItems(OPTIONS)#
      return OPTIONS

if __name__ == '__main__':
    if os.path.exists('file2.txt'):
       os.remove('file2.txt')    
    testing = 1
    kind = 'All'
    expa = 'All'
    OPTIONS , pet1s, code = create_pet_list.create_pet_list(kind,expa) #0555
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
