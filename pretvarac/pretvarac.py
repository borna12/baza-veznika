import os
import io
from bs4 import BeautifulSoup
import re
import shutil
import datetime



adresa="/".join(os.getcwd().split(os.sep)[:-1])


abecedarij=""
broj=1
for file in sorted(os.listdir(adresa)):
    broj+=1
    if file.endswith(".html"):
        if  "%i" in str(file):
          os.rename(adresa+"/"+file,adresa+"/"+file.replace("%i",""))
          file=file.replace("%i","")
        f = io.open(adresa+"/"+file,'r+',encoding="utf-8", errors='ignore')
        lines1 = f.readlines() # read old content
        if(len(lines1)<=2):
          f.close()
          os.remove(adresa+"/"+file) 
          continue
        
        soup = BeautifulSoup("\n".join(lines1).replace('href="tlex://','class="audio_izgovor" href="https://rjecnik.hr/mreznik/wp-content/uploads/2021/mreznik_mediji/').replace(".mp3/",".mp3"), 'html.parser')
        paragraf = soup.find('p')
        paragraf.attrs['class'] = 'accordion'
        '''new_tag = soup.new_tag("div")'''
        paragraf.insert_after("<div class='panel'>")
        for x in paragraf:
          try: 
            x.attrs['class'] = 'accordion'
          except AttributeError:
            print() 
        tag = soup.find_all('span', {"class" : "vanjska_poveznica__poveznica"})
        for x in tag:
          try:
            x.name="a"
            x.attrs['href'] = x.string
            x.attrs['target'] = "_blank"
          except AttributeError:
            print() 
        span=soup.find('span', {"class" : "Lemma__LemmaSign"})
        if span==None:
          span=soup.find('span', {"class" : "Lemma_Djeca__natuknica"})
        if span==None:
          span=soup.find('span', {"class" : "Lemma_Stranci__natuknica"})
        span2=soup.find('span', {"class" : "Definicija__definicija"})
        try:
          natuknica=str(span.string.replace("%i",""))
          prvo_slovo=str(file[0])
          if str(file[-6]).isnumeric():
            abecedarij+='<a class="natuknica osnova" href="./'+natuknica+'">'+natuknica+ '<sup>'+str(file[-6])+'</sup></a>\n'
          else:
            abecedarij+='<a class="natuknica osnova" href="./'+natuknica+'">'+natuknica+'</a>\n'
        except AttributeError:
          try:
            natuknica=span.text
          except AttributeError:
            natuknica=""
        try:
          natuknica2=span2.string
        except AttributeError:
          natuknica2=""
        try:
          natuknica2=natuknica2.split("\n")
          natuknica2=natuknica2[0].lstrip().rstrip()
        except AttributeError:
          natuknica2=""
        razmak="\n"
        f.seek(0) # go back to the beginning of the file
        # osnovni
        tekst=str(soup).replace("&lt;","<").replace("&gt;",">").replace('span class="accordion"','span')
        
        f.write(tekst)  
        f.close()
        """try:
          if natuknica[0]=="ć":
            os.rename(adresa+"/"+file,adresa+"/ć/"+file)
          elif natuknica[0]=="č":
            os.rename(adresa+"/"+file,adresa+"/č/"+file)
          elif natuknica[0]=="đ":
            os.rename(adresa+"/"+file,adresa+"/đ/"+file)
          elif natuknica[0]=="š":
            os.rename(adresa+"/"+file,adresa+"/š/"+file)
          elif natuknica[0]=="ž":
            os.rename(adresa+"/"+file,adresa+"/ž/"+file)
        except IndexError:
          print()"""
parametri=["</","<p","<s"]

for file in sorted(os.listdir(adresa)):
    broj+=1
    if file.endswith(".html"):
        f = io.open(adresa+"/"+file,'r+',encoding="utf-8", errors='ignore')
        print (file)
        lines1 = f.readlines() # read old content
        if(lines1[-1][0:2] not in parametri):
          f.close()
          f = io.open(adresa+"/"+file,'w',encoding="utf-8", errors='ignore')
          lines1=lines1[0:-1]
          f.seek(0)
          f.write(str("".join(lines1)))
        f.write("</div>")
        f.close()
index = io.open(adresa+"/kazalo/index.html",'w',encoding="utf-8", errors='ignore')
for file in sorted(os.listdir(adresa)):
    broj+=1
    if file.endswith(".html"):  
      f = io.open(adresa+"/"+file,'r+',encoding="utf-8", errors='ignore')
      lines1 = f.readlines()
      index.write("".join(lines1))
      f.close()
index.close()
        