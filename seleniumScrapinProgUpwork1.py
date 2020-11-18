import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import requests
from selenium.common.exceptions import NoSuchElementException

# define global init 'surebet' condition value (note by default any bet will not be a surebet given its > 1.0)
surebet_factor = 1.1


def check_is_surebet(odds_A, odds_B):

    if odds_A == 0 or odds_B == 0 :
        return False
        
    elif ( 1/(odds_A) + 1/(odds_B) < 1.0 ) :
        return True
        
    else:
        return False

def get_surebet_factor(odds_A, odds_B):

    global surebet_factor

    if odds_A == 0 or odds_B == 0 :
        pass
    else:
        surebet_factor = 1/(odds_A) + 1/(odds_B)

    return surebet_factor


def return_surebet_vals(odds_A, odds_B,stake):

    #surebetStakes = []
    if odds_A == 0 or surebet_factor == 0 :
        sureStakeA  = stake
    else:    
        sureStakeA = (1/surebet_factor)*(stake/odds_A)

    if odds_B == 0 or surebet_factor == 0 :    
        sureStakeB =  stake
    else:    
        sureStakeB = (1/surebet_factor)*(stake/odds_B)

    return [sureStakeA, sureStakeB]


def obtener(url):

    #page = requests.get(url, headers=headers).text
    #soup = BeautifulSoup(page, 'html.parser')

    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser');
    lista=[]
    
    #resulta = soup.find_all(); #re.compile('^bloclive')); #, {'class': 'puce_texte'})

    resulta = soup.findAll('div', attrs = {'class':'uk-flex'}) 

    print('   ****************************    length of soup results = ' + str(len(resulta)) + '  *************************  and abot to print each item in the results object... : ')

    print(soup.prettify())
    #for item in resulta:
        #text = item.text
        #print(str(text))
        
        #text=str(text).replace("Ã³","o")
        # text=str(text).replace("Ã­","i")
        # text=str(text).replace("Ã±","n")
        # text=str(text).replace("í","i")
        # text=str(text).replace("Â°","°")
        # text=str(text).replace("Ã©","e")    
        # text=str(text).replace("Ã¡","a")
        # text=str(text).replace("\' ","' ")
        # text=str(text).replace("<br/>","")
        # text=str(text).replace("\n","")
        # text=str(text).replace("Operativo","Operativo : si")
        # text=str(text).replace("Parque eolico onshore","Parque eolico onshore : si")
        # text=str(text).replace("Imágenes de Google Maps","Imágenes de Google Maps : si")
        
        #lista.append(text)
    return lista

DRIVER_PATH = r'C:\Users\MaaD\Downloads\chromedriver' #the path where you have "chromedriver" file.
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver.get('https://google.com')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://france-pari.fr/")

#url = "https://france-pari.fr/"
#obtener(url)
#print(driver.page_source) "):  #

soccerButton_out = driver.find_elements_by_xpath("/html/body/div[@id='main']/section[@id='colonne_gauche']/div[3]/div[@class='bloc-inside-small']/div[@class='uk-sticky-placeholder']/nav[@role='navigation']/ul/li")

if soccerButton_out:
    print("At last one such element exists ! and its length =  " + str(len(soccerButton_out))  + " :) ...")

else:
    print("NO SUch element exists ! :( ...")


soccerButn = driver.find_element_by_tag_name("ahref")    

#try:
#    login_form = driver.find_elements_by_xpath("/html/body//div[@id='main']//div[@id='colonne_gauche']") #//div[@class='bloc-inside-small']//div[@class='uk-sticky-placeholder']/nav[@role='navigation']/ul[0]/li[0]//div[@class='nonsense']",)  #//a[@href]")  # [contains(@class,'tabId')]//a[@href]")

#except NoSuchElementException:

#    print("Error caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")

print('all good the find_elements_by_xpath Call worked GRAND !! :) ')
#login_form =  driver.find_element_by_id("PARIS SPORTIFS")


driver.quit()