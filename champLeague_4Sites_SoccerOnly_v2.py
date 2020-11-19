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


DRIVER_PATH = r'C:\Users\MaaD\Downloads\chromedriver' #the path where you have "chromedriver" file.
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver.get('https://google.com')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
#driver.get("https://france-pari.fr/")


#list of website links (most general for football mathces)
france_pari_champions_league_link = "https://www.france-pari.fr/competition/6674-parier-sur-ligue-des-champions"
unibet_champions_league_link      = "https://www.unibet.fr/sport/football/ligue-des-champions/ligue-des-champions-matchs"
zebet_champions_league_link       = "https://www.zebet.fr/fr/competition/6674-ligue_des_champions"
vbet_champions_league_link        = "https://www.vbet.fr/paris-sportifs?btag=147238_l56803&AFFAGG=#/Soccer/Europe/566/17145852"

websites = [france_pari_champions_league_link, unibet_champions_league_link, zebet_champions_league_link, vbet_champions_league_link]

reference_champ_league_games_url = str(websites[0])

driver.get(reference_champ_league_games_url)

refernce_champ_league_gamesDict = {}


# now navigate using the driver and xpathFind to get to the matches section of Ref. site :
champ_league_games_pariFrance_list = driver.find_elements_by_xpath("/html/body/div[@id='main']/section[@id='colonne_centre']/div[@class='nb-middle-content']/div/div[@class='bloc-inside-small']/div[@id='nb-sport-switcher']/div[@class='item-content uk-active']/div[@class='odd-event uk-flex']")

if champ_league_games_pariFrance_list:
    print("At last one such element exists ! and its length =  " + str(len(champ_league_games_pariFrance_list))  + " :) ...")

else:
    print("NO SUch element exists ! :( ...")

for games in champ_league_games_pariFrance_list:

    team_names_element = games.find_element_by_xpath('//div[@class="odd-event-block snc-odds-date-lib uk-flex"]/span[@class="bet-libEvent') #/a') #.get_attribute("href")
    if team_names_element:
        print('game href names element block exists ! :) ...')
        team_names_string = team_names_element.get_attribute("href")
    else:
        print('NAAH --  game href names element block DOESN"t exist you fuckin wasp ! :( ... ')    

    
    odds_element = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@class="odd-without-actor",@labelnum="1"]/a/span[@class="odd"]') 
    if odds_element:
        print('game ODDS element block exists ! :) ...')
        odds_string = odds_element.text

    else:
        print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    



print('all good the find_elements_by_xpath Call worked GRAND !! :) ')
#login_form =  driver.find_element_by_id("PARIS SPORTIFS")


driver.quit()