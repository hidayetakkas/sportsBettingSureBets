import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import requests
from selenium.common.exceptions import NoSuchElementException
import smtplib
from smtplib import SMTPException

# define global init 'surebet' condition value (note by default any bet will not be a surebet given its > 1.0)
surebet_factor = 1.1

#cibstant initialised to False - for determining if they customer's expected odds are retrieved for alert system...
odd_are_found = False


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


def odds_alert_system(init_oddA,expect_oddB,teamA,teamB,date,competition):

    # search for game on ref. site:
    #blacvh_code_her();
    while(True):

        #search all other sites repeatedly until the expected odds are found
        x = 1
        #search_func(expect_oddB,teamA,teamB,date,competition)

        if odd_are_found:
            break
        else:
             #go_to_aert_func()
            continue   
    
    return True

DRIVER_PATH = r'C:\Users\MaaD\Downloads\chromedriver' #the path where you have "chromedriver" file.
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver.get('https://google.com')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
#driver.get("https://france-pari.fr/")

#list of website links (most general for football mathces-1st few are for champions league)
france_pari_champions_league_link = "https://www.france-pari.fr/competition/6674-parier-sur-ligue-des-champions"
unibet_champions_league_link      = "https://www.unibet.fr/sport/football/ligue-des-champions/ligue-des-champions-matchs"
zebet_champions_league_link       = "https://www.zebet.fr/fr/competition/6674-ligue_des_champions"
vbet_champions_league_link        = "https://www.vbet.fr/paris-sportifs?btag=147238_l56803&AFFAGG=#/Soccer/Europe/566/17145852"

websites = [france_pari_champions_league_link, unibet_champions_league_link, zebet_champions_league_link, vbet_champions_league_link]

reference_champ_league_games_url = str(websites[0])
driver.get(reference_champ_league_games_url)
refernce_champ_league_gamesDict = {}

# some vars for parsing the games data - strings.
#initialize data with todays date - better than empty string
date = ''
competition = 'champions_league'

# def try_catch_function():

#     exceptionBool = False


#     return exceptionBool

#if only soing 2 - way sure bet , then oddDraw can be set to -1 and used as such when read in here
def send_mail_alert(teamA,teamB,oddsExpecTeamBwin,oddsTeamAWin,OddsDraw,bookiesNameA,bookiesNameEventB,bookiesNameEventA,bookiesNameEventDraw,competition):

    successFlag = False
    sender = 'godlikester@gmail.com'
    receivers = ['crowledj@tcd.ie']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    The is an Alert to tell you that the bookmaker - 
    """ + str(bookiesNameEventB) + """ has its odd's on team B - """
    + str(teamB) + """ to win the event against """ + str(teamA) + """
    in the competition """ + str(competition) +
    """ reach a value of """ + str(oddsExpecTeamBwin) +  """ at approx
    hh:mm:ss o clock on zz day of MM / 20YY """

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.gmail.com",465)
        smtpObj.login("godlikester@gmail.com", "Elnino_9")
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
        successFlag = True
    except SMTPException:
        print("Error: unable to send email")
        pass

    return successFlag


# now navigate using the driver and xpathFind to get to the matches section of Ref. site :
try:
    champ_league_games_pariFrance_meta_info = driver.find_elements_by_xpath("/html/body/div[@id='main']/section[@id='colonne_centre']/div[@class='nb-middle-content']/div/div[@class='bloc-inside-small']/div[@id='nb-sport-switcher']/div[@class='item-content uk-active']") #/div[@class='odd-event uk-flex']")
except err as NoSuchElementException:

    print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    pass
    #continue
# pick up date and competetion 1st beofre list of games:

date_element = driver.find_element_by_xpath('//p[@class="date soccer"]')

if date_element:
    print('game DATE names element block exists ! :) ...')
    
    try:
        date = date_element.text
        
    except err as NoSuchElementException:

        print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        pass
else:
    print('NAAH --  game href DATE element block DOESN"t exist you fuckin wasp ! :( ... ')    

#.text
competition = driver.find_element_by_xpath('//h2[@class="competition soccer"]').text

#driver.back()
champ_league_games_pariFrance_list = driver.find_elements_by_xpath("//div[@class='odd-event uk-flex']")


if champ_league_games_pariFrance_list:
    print("At last one such element exists ! and its length =  " + str(len(champ_league_games_pariFrance_list))  + " :) ...")
else:
    print("NO SUch element exists ! :( ...")

#now loop thru all champ league games on france-pari site
for games in champ_league_games_pariFrance_list:

    team_names_element = False
    try:
        team_names_element = games.find_element_by_tag_name('a')  #//span[@class="bet-libEvent]') #/a') #.get_attribute("href")
        #div[@class="odd-event-block snc-odds-date-lib uk-flex"]/span/
    except err as NoSuchElementException:
        print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        pass

    if team_names_element:
        print('game href names element block exists ! :) ...')
        
        try:
            team_names_string = team_names_element.get_attribute("href")
           
        except err as NoSuchElementException:

            print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
            pass
    else:
        print('NAAH --  game href names element block DOESN"t exist you fuckin wasp ! :( ... ')    

    odds_elementA = False
    try:
        odds_elementA = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="1"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
    except err as NoSuchElementException:

        print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        pass
 
    if odds_elementA:
        print('game ODDS element block exists ! :) ...')
        odds_string_teamA = odds_elementA.text

    else:
        print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    
    
    odds_element_draw = False
    try:
        odds_element_draw = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="N"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
    except err as NoSuchElementException:

        print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        pass   
    
    if odds_element_draw:
        print('game ODDS element block exists ! :) ...')
        odds_string_draw = odds_element_draw.text

    else:
        print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    
    
    odds_elementB = False
    try:
        odds_elementB = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="2"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
    except err as NoSuchElementException:

        print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        #continue 
        pass   

    if odds_elementB:
        print('game ODDS element block exists ! :) ...')
        odds_string_teamB = odds_elementB.text

    else:
        print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    

    refernce_champ_league_gamesDict[date + '_' + competition + '_' + team_names_string] = odds_string_teamA + '_' + odds_string_draw + '_' + odds_string_teamB

print('all good the find_elements_by_xpath Call worked GRAND !! :) --- full champ league games data struct = ')
print(refernce_champ_league_gamesDict)
#login_form =  driver.find_element_by_id("PARIS SPORTIFS")


# TODO :rename like actual sites 
site2s_champ_league_gamse = {}
site3s_champ_league_gamse = {}
site4s_champ_league_gamse = {}

# #Next loop thru all other SITE's champ league games besides  france-pari site as its the reference to compare to...
# for sites in websites[1:]:

#     driver.get(sites)
    
#     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
#     try:
#         champ_league_games_pariFrance_list = driver.find_elements_by_xpath("/html/body/div[@id='main']/section[@id='colonne_centre']/div[@class='nb-middle-content']/div/div[@class='bloc-inside-small']/div[@id='nb-sport-switcher']/div[@class='item-content uk-active']/div[@class='odd-event uk-flex']")
#     except err as NoSuchElementException:

#         print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#         continue

#     if champ_league_games_pariFrance_list:
#         print("At last one such element exists ! and its length =  " + str(len(champ_league_games_pariFrance_list))  + " :) ...")
#     else:
#         print("NO SUch element exists ! :( ...")

#     #now loop thru all champ league games on france-pari site
#     for games in champ_league_games_pariFrance_list:

#         team_names_element = False
#         try:
#             team_names_element = games.find_element_by_tag_name('a')  #//span[@class="bet-libEvent]') #/a') #.get_attribute("href")
#             #div[@class="odd-event-block snc-odds-date-lib uk-flex"]/span/
#         except err as NoSuchElementException:
#             print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#             continue

#         if team_names_element:
#             print('game href names element block exists ! :) ...')
            
#             try:
#                 team_names_string = team_names_element.get_attribute("href")
#             except err as NoSuchElementException:

#                 print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#                 continue
#         else:
#             print('NAAH --  game href names element block DOESN"t exist you fuckin wasp ! :( ... ')    

#         odds_elementA = False
#         try:
#             odds_elementA = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="1"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
#         except err as NoSuchElementException:

#             print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#             continue
    
#         if odds_elementA:
#             print('game ODDS element block exists ! :) ...')
#             odds_string_teamA = odds_elementA.text

#         else:
#             print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    
        
#         odds_element_draw = False
#         try:
#             odds_element_draw = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="N"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
#         except err as NoSuchElementException:

#             print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#             continue   
        
#         if odds_element_draw:
#             print('game ODDS element block exists ! :) ...')
#             odds_string_draw = odds_element_draw.text

#         else:
#             print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    
        
#         odds_elementB = False
#         try:
#             odds_elementB = games.find_element_by_xpath('//div[@class="odd-event-block uk-flex"]/div[@labelnum="2"]/a/span[@class="odd"]') #@class="odd-without-actor",  tag_name('#span[@class="odd"]')
#         except err as NoSuchElementException:

#             print("Error  ->" + str(err) + "caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
#             continue    

#         if odds_elementB:
#             print('game ODDS element block exists ! :) ...')
#             odds_string_teamB = odds_elementB.text

#         else:
#             print('NAAH --  game ODDS element block DOESN"t exist you fuckin wassy ! :( ... ')    



driver.quit()