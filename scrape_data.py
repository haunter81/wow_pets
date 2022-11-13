from bs4 import BeautifulSoup
import requests


def scrapepetinfo(choice):
        global pdict
        pdict={}
        global apperancerating
        global battlerating
        global finaltext
        #1fp = open("shared.txt","r")
        #1pet_s = fp.read()
        #1fp.close()
        finaltext=""
        notvalues= ['Yes' ,'Vocalizations (on-click)' ,'None','Looks around.','Vocalizations']
        values=[]
        #pet_s=input("Pet Name:")
        headers = {'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}
        #1site = 'https://www.google.com/search?q=warcraftpets.com+'+pet_s
        #site = 'https://www.google.com/search?q=warcraftpets.com+'+choice
        #html = requests.get(site,headers=headers).text
        #soup = BeautifulSoup(html, 'lxml')
        #summary = []
        #for container in soup.findAll('div', class_='tF2Cxc'):
        #    link = container.find('a')['href']
        #    #print (link)
        #    break
        link="http://www.warcraftpets.com/search/?q="+choice
        if choice=="Abyssal Eel" or choice=="Froglet":
           link="https://www.warcraftpets.com/wow-pets/aquatic/eels/abyssal-eel/"
        html = requests.get(link,headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        l=[]
        mydivs2 = soup.find_all("div", {"class": "voteddetails"})
        for i in mydivs2:
            l.append(i.text)
        a = l[0]
        apperancerating=a.replace('Appearance','Appearance ')
        b= l[1]
        battlerating=b.replace('Battle','Battle ')
        #print (apperancerating)
        #print (battlerating)
        mydivs2 = soup.find_all("div", {"class": "value"})
        for value in mydivs2:
            a = value.text
            try:
               values.append(a.strip())
            except AttributeError:
                pass
        for i in range(0,10):
            if values[i] in notvalues:
                 pass
            else:
               finaltext = finaltext+values[i]+","
        #print(finaltext)
        #site2 = 'https://www.google.com/search?q=wow-pets.com+'+pet_s
        site2 = 'https://www.google.com/search?q=wow-pets.com+'+choice
        html = requests.get(site2,headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        #summary = []
        for container in soup.findAll('div', class_='tF2Cxc'):
            link = container.find('a')['href']
            #print (link)
            break
        html1 = requests.get(link, headers=headers).text
        soup = BeautifulSoup(html1, 'lxml')
        #print (soup)
        test1 = soup.find_all("div", {"class": "info-box"})
        #print(test1)
        for val in test1:
            val1 = val.find('h3').text
            val2 = val.find('span').text
            #print(val1,":",val2)
            pdict[val1]=val2
        #print(pdict)   
        #return finaltext 
        #return apperancerating
        #return battlerating


