import msvcrt
import random
#from bs4 import BeautifulSoup
import re
import smtplib
import time
import timeit
from collections import defaultdict
from smtplib import SMTPException

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# define global init 'surebet' condition value (note by default any bet will not be a surebet given its > 1.0)
surebet_factor = 0.0
#cibstant initialised to False - for determining if they customer's expected odds are retrieved for alert system...
odd_are_found = False

def check_is_surebet(*args): #odds_A, odds_B):

    total_iverse_odds_sum = 0.0
    for odds in args:
        if odds == 0:
            pass
        else:
            total_iverse_odds_sum += 1/(odds)

    if total_iverse_odds_sum < 1.0 and total_iverse_odds_sum > 0.0:
        return True

    return False    

def get_surebet_factor(*argv): #  odds_A, odds_B):

    global surebet_factor

    #total_iverse_odds_sum = 0.0
    for odds in argv:
        if odds == 0:
            pass
        else:
            surebet_factor += 1/(odds)

    return surebet_factor


def return_surebet_vals(*argv, stake):  #odds_A, odds_B,stake):

    surebetStakes = []

    for i,odds in enumerate(argv):

        if odds == 0.0 or surebet_factor == 0.0 :
            surebetStakes[i]  = stake
        else:    
            surebetStakes[i] = (1/surebet_factor)*(stake/odds)
                                                                                       
    return surebetStakes


## TODO : must generalize this and add file to code bundle
DRIVER_PATH = r'.\chromedriver' #the path where you have "chromedriver" file.
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver.get('https://google.com')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#remove?as done below for site's direct champ league url!
#driver.get("https://france-pari.fr/")

#list of website links (most general for football mathces-1st few are for champions league)
france_pari_champions_league_link = "https://www.france-pari.fr/competition/6674-parier-sur-ligue-des-champions"
vbet_champions_league_link        = "https://www.vbet.fr/paris-sportifs?btag=147238_l56803&AFFAGG=#/Soccer/Europe/566/17145852"
unibet_champions_league_link      = "https://www.unibet.fr/sport/football/ligue-des-champions/ligue-des-champions-matchs"
zebet_champions_league_link       = "https://www.zebet.fr/fr/competition/6674-ligue_des_champions"

#same order as data structures in their list
websites = [france_pari_champions_league_link, unibet_champions_league_link, zebet_champions_league_link]

reference_champ_league_games_url = str(websites[0])
driver.get(reference_champ_league_games_url)

# some vars for parsing the games data - strings.
#initialize data with todays date - better than empty string
date = '25 Novembre'
compettition = 'Ligue des Champions'    

# TODO :rename like actual sites 
refernce_champ_league_gamesDict = defaultdict(list) # pari-france site
site_unibet_champ_league_gamse  = defaultdict(list)
sites_zebetchamp_league_gamse   = defaultdict(list)
site4s_champ_league_gamse       = defaultdict(list)
site5s_champ_league_gamse       = defaultdict(list)
site6s_champ_league_gamse       = {}
site7s_champ_league_gamse       = {}
site8s_champ_league_gamse       = {}    
site9s_champ_league_gamse       = {}
site10s_champ_league_gamse      = {}
site11s_champ_league_gamse      = {}
site12s_champ_league_gamse      = {}

all_srpaed_sites_data = [refernce_champ_league_gamesDict, site_unibet_champ_league_gamse, sites_zebetchamp_league_gamse, site4s_champ_league_gamse, site5s_champ_league_gamse]

def odds_alert_system(oddType=1,expect_oddValue=1.0,teamA='Liverpool',teamB='barcelone',date='Mercredi 25 Novembre',competition='Ligue des Champions',Bookie1_used='Winimax',Bookie2_used=''):

    global refernce_champ_league_gamesDict, site_unibet_champ_league_gamse, sites_zebetchamp_league_gamse, site4s_champ_league_gamse, site5s_champ_league_gamse

    global all_srpaed_sites_data

    #remove bookies uused:
    
    #all_srpaed_sites_data.remove(Bookie1_used)
    #if(Bookie2_used):
    #    all_srpaed_sites_data.remove(Bookie2_used)

    sub_strs_in_key = [date.lower(),competition.lower(),teamA.lower(),teamB.lower()]

    # search for game (and competition and date to ensure uniqueness) on ref. site:
    while(True):

        #time.sleep(1)
        print('Click on the "esc" key @ any time to terminate this program and can then restart again any time you wish :) ......')

        # waitr a delay time to refresh sites parsings....
        if parseSites(all_srpaed_sites_data): #all_srpaed_sites_data):
            pass
        
        ## !!! THIS PIECE OF CODE SEEMS TO BE BREAKING THE PROGRAM - CAUSING IT TO HAVE VERY UNDEFINED RUNTIME BEHAVIOUT ???     
        # if msvcrt.getch() == 'esc':
        #     print('Esc key pressed , stopping and exiting the constant Alert with odds function ....')
        #     break
        for site_data in all_srpaed_sites_data:

            for key in site_data.keys():
                bookie_name = key.split('_')[1]  

                if all(x in key for x in sub_strs_in_key):

                    if oddType == 0 and float(site_data[key][oddType]) > expect_oddValue:
                        send_mail_alert(1.0,site_data[key][0], teamA, teamB, date, competition, bookie_name)
                    elif oddType and float(site_data[key][oddType]) > expect_oddValue:
                        send_mail_alert(1.0,site_data[key][oddType], teamA, teamB, date, competition, bookie_name)  
                    else:
                        print('issue with finding /checking the expected odd across all data and sites...')
                        return False
   
    return True

## TODO :
# def try_catch_function():
#     exceptionBool = False

#     return exceptionBool

#if only soing 2 - way sure bet , then oddDraw can be set to -1 and used as such when read in here
def send_mail_alert(init_oddA,expect_oddB,teamA,teamB,date,competition,bookiesNameEventB):

    successFlag = False
    sender = 'godlikester@gmail.com'
    receivers = ['crowledj@tcd.ie']#'pauldarmas@gmail.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    The is an Alert to tell you that the bookmaker - 
    """ + str(bookiesNameEventB) + """ has its odd's on team B - """ + str(teamB) + """ to win the event against """ + str(teamA) + """ \
    in the competition """ + str(competition) + """ reach a value of """ + str(expect_oddB) +  """ at approxs
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


def parseSites(all_crapedSites_data): 

    global websites, compettition, date  #, refernce_champ_league_gamesDict

    any_errors = True

    # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
    try:
        driver.find_elements_by_xpath("/html/body/div[@id='main']/section[@id='colonne_centre']/div[@class='nb-middle-content']/div/div[@class='bloc-inside-small']/div[@id='nb-sport-switcher']/div[@class='item-content uk-active']") #/div[@class='odd-event uk-flex']")
    
    except: # err as NoSuchElementException:

        print("Error  -> caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
        any_errors = False
        pass
        #continue
    # pick up date and competetion 1st beofre list of games:

    date_element = driver.find_element_by_xpath('//p[@class="date soccer"]')

    if date_element:
        print('game DATE names element block exists ! :) ...')
        
        try:
            Date = date_element.text
            # update global date hetre as this site has it reliably - (for others)
            date = Date
        except: # err as NoSuchElementException:
            any_errors = False
            print("Error  -> caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
            pass
    else:
        print('NAAH --  game href DATE element block DOESN"t exist :( ... ')    

    #.text
    competition = driver.find_element_by_xpath('//h2[@class="competition soccer"]').text
    #driver.back()
    champ_league_games_pariFrance_list = driver.find_elements_by_xpath("//div[@class='odd-event uk-flex']")

    if champ_league_games_pariFrance_list:
        print("At last one such element exists ! and its length =  " + str(len(champ_league_games_pariFrance_list))  + " :) ...")
    else:
        any_errors = False
        print("NO SUch element exists ! :( ...")

    #now loop thru all champ league games on france-pari site
    for j,games in enumerate(champ_league_games_pariFrance_list):

        team_names_element = False
        try:
            team_names_element = games.find_element_by_tag_name('a')  #//span[@class="bet-libEvent]') #/a') #.get_attribute("href")
            #div[@class="odd-event-block snc-odds-date-lib uk-flex"]/span/
        except: # err as NoSuchElementException:
            any_errors = False
            print("Error  -> caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
            pass

        if team_names_element:
            print('game href names element block exists ! :) ...')
            
            try:
                team_names_string = team_names_element.get_attribute("href")
            
            except: # err as NoSuchElementException:
                any_errors = False
                print("Error  -> caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                pass
        else:
            print('NAAH --  game href names element block DOESN"t exist ! :( ... ')    


        split_game_data_str = games.text.split('\n') 

        odds_string_teamA = split_game_data_str[3].replace(',','.')
        odds_string_teamB = split_game_data_str[7].replace(',','.')
        odds_string_draw = split_game_data_str[5].replace(',','.')

        #test: leave orig. version here for now , but replace with the default dict loist way a few lines ahead...
        #refernce_champ_league_gamesDict[date + '_' + competition + '_' + team_names_string] = odds_string_teamA + '_' + odds_string_draw + '_' + odds_string_teamB
        refernce_champ_league_gamesDict[date.lower() + '_' + competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_teamA) 
        refernce_champ_league_gamesDict[date.lower() + '_' +  competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_draw)
        refernce_champ_league_gamesDict[date.lower() + '_' +  competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_teamB)


    print('all good the find_elements_by_xpath Call worked GRAND !! :) --- full champ league games data struct = ')
    print(refernce_champ_league_gamesDict)
    #login_form =  driver.find_element_by_id("PARIS SPORTIFS")

    #############################     TEST ALERT - send to Paul darmas    #############################

    #send Alert to paul's mail:
    #send_mail_alert(2.5,3.25,'Liverpool','Barcelona','01/04/2021','Champions League','Unibet')

    #############################     TEST ALERT - send to Paul darmas    #############################

    # #Next loop thru all other SITE's champ league games besides  france-pari site as its the reference to compare to...
    for i,sites in enumerate(websites[1:]):

        #begin = timeit.timeit()  
        driver.get(sites)
        #finish = timeit.timeit()

        if sites.startswith('unibet',12) or sites.startswith('unibet',11) :
        # unibet tree struct to games elements:

            # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
            try:
                #start = timeit.timeit()
                champ_league_games_nested_gamesinfo_unibet = driver.find_elements_by_xpath('/html/body/div[@id="container"]/div[@id="wrapper"]/div[@id="content-container"]/div[@id="content"]/section/div[@id="main"] \
                /section[@id="view-main-container"]/div[@id="view-main"]/section[@id="page__competitionview"]/div[@class="view view-eventpath"]/div[@class="page-wrap"] \
                /div[@class="scroller"]/div[@class="ui-splitview"]/div[@class="ui-splitview-item ui-splitview-left"]/div[@class="i-splitview-item-inner"]/div[@class="c-eventpathlist bettingbox"] \
                /div[@class="ui-mainview-block eventpath-wrapper"]/div[@class="bettingbox-item box"]/div[@class="bettingbox-content oddsbox-hide-marketname bettingbox-wide"]/div[@class="ui-touchlink had-market inline-market calendar-event cell"]') 
                #end = timeit.timeit()
                #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

                for matches in  champ_league_games_nested_gamesinfo_unibet:
                    #print(matches.text)
                    split_match_data_str = matches.text.split('\n') 
                    teams = split_match_data_str[0]
                    competition =  split_match_data_str[1]
                    teamAWinOdds = split_match_data_str[2]
                    teamBWinOdds = split_match_data_str[6]
                    draw_odds    = split_match_data_str[4]

                    all_crapedSites_data[i+1][date.lower() + '_' + competition.lower() + '_' + teams].append(teamAWinOdds.split(' ')[1].replace(',','.').lower())  #=   teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    all_crapedSites_data[i+1][date.lower() + '_' + competition.lower() + '_' + teams].append(draw_odds.split(' ')[1].replace(',','.').lower())
                    all_crapedSites_data[i+1][date.lower() + '_' + competition.lower() + '_' + teams].append(teamBWinOdds.split(' ')[1].replace(',','.').lower())    
                    #check = 1


            except: #  NoSuchElementException:
                any_errors = False
                print("Error  ->  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue
            #check = 1

        
        if sites.startswith('zebet',12) or sites.startswith('zebet',11) :
        # unibet tree struct to games elements:

            try:
                #start = timeit.timeit()
                champ_league_games_nested_gamesinfo_zebet = driver.find_elements_by_xpath('/html/body/div[@id="global"]/div[@id="content"]/main[@class="uk-flex-item-1 uk-width-7-12"]/section/ \
                div[@class="uk-block-20-20 uk-block-small-10-10"]/div[@id="event"]/article[@class="item"]/div[@class="uk-accordion uk-accordion-block item"]/ \
                div[@class="uk-accordion-wrapper item-bloc item"]/div/div[@class="uk-accordion-content uk-padding-remove uk-active"]/div/div[@class="item-content catcomp item-bloc-type-1"]')
                    #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
                #end = timeit.time
                #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

                for matches in  champ_league_games_nested_gamesinfo_zebet:
                    print(matches.text)
                    split_match_data_str = matches.text.split('\n') 
                    date = split_match_data_str[0]
                    teams = split_match_data_str[2] + '_' + split_match_data_str[6]
                    competition =  compettition #split_match_data_str[1]    
                    teamAWinOdds = split_match_data_str[1].replace(',','.')
                    teamBWinOdds = split_match_data_str[3].replace(',','.')
                    draw_odds    = split_match_data_str[5].replace(',','.')

                    all_crapedSites_data[i+1][date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    all_crapedSites_data[i+1][date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
                    all_crapedSites_data[i+1][date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            except NoSuchElementException:
                any_errors = False
                print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue


#             0: "html.uk-notouch"
# 1: "body"
# 2: "div#global"
# 3: "div#content"
# 4: "main.uk-flex-item-1.uk-width-7-12"
# 5: "section"
# 6: "div.uk-block-20-20.uk-block-small-10-10"
# 7: "div#event"
# 8: "article.item"
# 9: "div.uk-accordion.uk-accordion-block.item"
# 10: "div.uk-accordion-wrapper.item-bloc.item"
# 11: "div"
# 12: "div.uk-accordion-content.uk-padding-remove.uk-active"
# 13: "div"
# 14: "div.item-content.catcomp.item-bloc-type-1"

    driver.quit()
    return any_errors

if __name__ == '__main__':

    #print('Running unit tests on sportsbetting applicationb version 1....')
    #unittest.main()

     retVal = odds_alert_system(oddType=2,expect_oddValue=2.35,teamA='liverpool',teamB='atalanta',date='Mercredi 25 Novembre',competition='Ligue des Champions',Bookie1_used='Winimax',Bookie2_used='')

     debug = -1

