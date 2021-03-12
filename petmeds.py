
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import win32com.client
import pypandoc

mainUrl="https://www.1800petmeds.com"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome("C:\CURSOS\pyhton raspa tela telegram bot\chromedriver.exe", options=options)






class HTML(object):
    text = ""
    # The class "constructor" - It's actually an initializer 
    def __init__(self, text):
        self.text = text

    def as_dict(self):
        return {'text': self.text}

    def addText(self,texto):
        self.text+=texto

    def printWord(self):
        output = pypandoc.convert_text(self.text, format='html', to='docx', outputfile='output.docx', extra_args=['-RTS'])




def getLinksPets():
    #getting the links for each page so we can access it later
    page = requests.get('https://www.1800petmeds.com/education')    
    soup = BeautifulSoup(page.text, 'html.parser')    
    links =soup.find_all("a", class_="link education-folder-link")
    return links

def accessLinksPets(listaPets):
    #with the links now we can acces each one of the pages
  
    for a in listaPets:
        concatenatedUrl=mainUrl + a['href']     
        driver.get(concatenatedUrl)         
        getPetData()
    

def getPetData():
    #here we are going to get the data from the paragraphs we need
    #getting the first paragraph
    summary=driver.find_element_by_xpath("//div[@class='container content-container']//div[@class='content-asset']").get_attribute('outerHTML')
    fullHTML.addText(summary)
   

    #this try except is used because there are some links that dont have tabs
    try: 
        #now to click on the other 3 tabs and get the other paragraphs is needed to close an ad 
        #(try opening without 'options.add_argument('--headless')' and you will see it is blocking the buttons we need to click)
        driver.find_element_by_xpath("//div[@class='modal-content form-wrapper']//button").click()

        #with the ad closed we click on the other tabs and get the content inside them
        driver.find_element_by_link_text("Symptoms & Diagnosis").click()
        Symptoms=driver.find_element_by_xpath("//div[@class='container content-container']//div[@class='content-asset']").get_attribute('outerHTML')
    
        driver.find_element_by_link_text("Treatment").click()
        Treatment=driver.find_element_by_xpath("//div[@class='container content-container']//div[@class='content-asset']").get_attribute('outerHTML')
        #adding text to the fullHTML who is going to be the one we are going to output to word in the end 
        fullHTML.addText(Symptoms)
        fullHTML.addText(Treatment)
    except:
        print("doesn't have other tabs")
        

    

    
    



#creating a object fullHTML who is going to receive all of the text from the pages
fullHTML=HTML("")
accessLinksPets(getLinksPets())
fullHTML.printWord()

driver.quit()