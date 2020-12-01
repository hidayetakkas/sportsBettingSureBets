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
import itertools
import sys,os

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

    # reset this global value -- but must think on should I create class 'gambler' to correctly initialise these kinds of vars and update per instance etc..(?)
    surebet_factor = 0.0

    #total_iverse_odds_sum = 0.0
    for odds in argv:
        if odds == 0:
            pass
        else:
            surebet_factor += 1/(odds)

    print('in get surebet function -- surebet = ' + str(surebet_factor))

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
DRIVER_PATH = r'./chromedriver' #the path where you have "chromedriver" file.
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://google.com')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

#remove?as done below for site's direct champ league url!
driver.get("https://france-pari.fr/")


## Class definitions :

# class ExtractorDataParser:
#     """Loads a CSV data file and provides functions for working with it"""

#     def __init__(self):
#         self.clear()

#     def clear(self):
#         # Records is a multidimensional dictionary of: records[frame_number][face_number][roi][signal] = value
#         self.records = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list))))
#         self.first_frame_number = sys.maxsize
#         self.last_frame_number = 0
#         self.number_frames = 0
#         self.meta_data = []
#         self.missing_records = []

#     def loadFile(self, filename):
#         self.clear()

#         if not (os.path.isfile(filename) and os.access(filename, os.R_OK)):
#             raise ValueError("Unable to read file '%s'" % filename )


    # def process_comment_record(self, record):
    #         # Ignore the pose information and the face rectangles
    #         if record[0].startswith( '#P:' ) or record[0].startswith( '#R:' ):
    #             return

    #         if record[0].startswith( '#M:'):
    #             record_number = int(record[0][3:])
    #             self.missing_records.append(record_number)
    #             return

    #         # Must be metadata, strip the leading #
    #         index = record[0].index(':')
    #         name = record[0][1:index]
    #         value = record[0][index+1:]
    #         metaString=name+" : "+value
    #         self.meta_data.append(metaString)

    #     def get_first_frame_number(self):
    #         """First frame number encountered when loading file"""
    #         return self.first_frame_number

    #     def get_last_frame_number(self):
    #         """Last frame number encountered when loading file"""
    #         return self.last_frame_number

    #     def get_number_frames(self):
    #         """Number of frames loaded from file."""
    #         return len(self.records)

    #     def get_missing_records(self):
    #         return self.missing_records

    #     def get_meta_data(self, key):
    #         try:
    #             return self.meta_data[key]
    #         except KeyError:
    #             return ""      


###  *********************************** CHAMPION'S LEAGUE lINKS *****************************
#list of website links (most general for football mathces-1st few are for champions league)
france_pari_champions_league_link =  "https://www.france-pari.fr/competition/6674-parier-sur-ligue-des-champions"
# d lads dont want this site as it's shite.
#vbet_champions_league_link        = "https://www.vbet.fr/paris-sportifs?btag=147238_l56803&AFFAGG=#/Soccer/Europe/566/17145852"
unibet_champions_league_link       = "https://www.unibet.fr/sport/football/ligue-des-champions/ligue-des-champions-matchs"
zebet_champions_league_link        = "https://www.zebet.fr/fr/competition/6674-ligue_des_champions"
winimax_champions_league_link      = "https://www.winamax.fr/en/sports-betting/sports/1/800000006"

#passionsports__champions_ligue_link = "" 
sportsbwin_champs_ligue_link       = "https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/europe-7/ligue-des-champions-0:3"

#betclic_champs_ligue_link         = ""
#pokerstarsSports_ligue1_link      = ""
#pasinoBet_ligue1_link             = ""

###  *********************************** LIGUE' 1  lINKS *****************************

betclic_ligue1_link       = "https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4"
france_pari_ligue1_link   = "https://www.france-pari.fr/competition/96-parier-sur-ligue-1-uber-eats"
unibet_ligue1_link        = "https://www.unibet.fr/sport/football/france-foot/ligue-1-ubereats-france"
zebet_ligue1_link         = "https://www.zebet.fr/en/competition/96-ligue_1_uber_eats"
winimax_ligue1_link       = "https://www.winamax.fr/en/sports-betting/sports/1/7/4"
passionsports_ligue1_link = "https://www.enligne.parionssport.fdj.fr/paris-football/france/ligue-1-uber-eats?filtre=22892"
sportsbwin_ligue1_link    = "https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/france-16/ligue-1-4131"

#betclic_ligue1_link       = ""
#pokerstarsSports_ligue1_link = ""
#pasinoBet_ligue1_link        = ""

###  *********************************** EUROPA LEAGUE lINKS *****************************
#list of website links (most general for football mathces-1st few are for champions league)
france_pari_europa_league_link   =  "https://www.france-pari.fr/competition/6674-parier-sur-europa-ligue"   #(?? - check this !!)
# d lads dont want this site as it's shite.
#vbet_champions_league_link        = "https://www.vbet.fr/paris-sportifs?btag=147238_l56803&AFFAGG=#/Soccer/Europe/566/17145852"
unibet_europa_league_link           =  "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
zebet_europa_league_link            =  "https://www.zebet.fr/en/competition/6675-europa_league"
winimax_europa_league_link          =  "https://www.winamax.fr/en/sports-betting/sports/1/800000007"
passionsports_europa_league_link    = "https://www.enligne.parionssport.fdj.fr/paris-football"
sportsbwin_europa_league_link       = "https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/europe-7/europa-league-0:5"    
betclic_europa_league_link          = "https://www.betclic.fr/football-s1/ligue-europa-c3453"

#pokerstarsSports_europa_league_link = ""
#pasinoBet_europa_league_link        = ""

#same order as data structures in their list
websites_champs_league_links = [france_pari_champions_league_link, unibet_champions_league_link, zebet_champions_league_link,winimax_champions_league_link, sportsbwin_champs_ligue_link]  # haS 5 LINKS NOW
websites_europa_league_links = [france_pari_europa_league_link, unibet_europa_league_link, zebet_europa_league_link,winimax_europa_league_link, sportsbwin_europa_league_link] # 7 links
websites_ligue1_links        = [france_pari_ligue1_link, unibet_ligue1_link, zebet_ligue1_link,winimax_ligue1_link, sportsbwin_ligue1_link] #,passionsports_ligue1_link] # 7 links m       # betclic_ligue1_link is empty for now

reference_champ_league_games_url = str(websites_champs_league_links[0])
driver.get(reference_champ_league_games_url)

# some vars for parsing the games data - strings.
#initialize data with todays date - better than empty string
date = '2 Decembre'
compettition = 'Ligue des Champions'    

# TODO :rename like actual sites 

# refernce_champ_league_gamesDict = defaultdict(list) # pari-france site
# #site_unibet_champ_league_gamse  = defaultdict(list)
# sites_zebetchamp_league_gamse   = defaultdict(list)
# unnibet_champ_league_gamse      = defaultdict(list)
# winimax_champ_league_gamse      = defaultdict(list)


# sportsbwin_champ_league_gamse   = {}
# site7s_champ_league_gamse       = {}
# site8s_champ_league_gamse       = {}    
# site9s_champ_league_gamse       = {}
# site10s_champ_league_gamse      = {}
# site11s_champ_league_gamse      = {}
# site12s_champ_league_gamse      = {}

full_all_bookies_allLeagues_match_data = defaultdict(list)
all_split_sites_data = []

#all_srpaed_sites_data = [refernce_champ_league_gamesDict, winimax_champ_league_gamse, sites_zebetchamp_league_gamse, unnibet_champ_league_gamse] #, site5s_champ_league_gamse]

#bookie 'nicknames'
zebet = 'zebet'
unibet = 'unibet'
winimax = 'winamax'
betclic = 'betclic'
france_pari = 'pari'
sports_bwin = 'sports.bwin'
pasinobet = 'pasinobet'

def odds_alert_system(oddType=1,expect_oddValue=1.0,teamA='Liverpool',teamB='barcelone',date='Mercredi 25 Novembre',competition='Ligue des Champions',Bookie1_used='winimax',Bookie2_used=''):

    #global refernce_champ_league_gamesDict, site_unibet_champ_league_gamse, sites_zebetchamp_league_gamse, site4s_champ_league_gamse, site5s_champ_league_gamse

    global full_all_bookies_allLeagues_match_data, all_split_sites_data # ,all_srpaed_sites_data
        
    #justParsed = False
    #remove bookies uused:
    #all_srpaed_sites_data.remove(Bookie1_used)
    #if(Bookie2_used):
    #    all_srpaed_sites_data.remove(Bookie2_used)
  
    Bookie1_used = Bookie1_used.lower()
    sub_strs_in_key = [date.lower(),competition.lower(),teamA.lower(),teamB.lower()]
    # search for game (and competition and date to ensure uniqueness) on ref. site:
    while(True):

        # intro randomness to not get caught ! - lol
        wait_time = random.randint(1,4)

        time.sleep(wait_time)
        print('Click on the "esc" key @ any time to terminate this program and can then restart again any time you wish :) ......')

        # waitr a delay time to refresh sites parsings....
        if  (not justParsed) :

            if parseSites(): #all_srpaed_sites_data):
                pass

        ## !!! THIS PIECE OF CODE SEEMS TO BE BREAKING THE PROGRAM - CAUSING IT TO HAVE VERY UNDEFINED RUNTIME BEHAVIOUT ???     
        # if msvcrt.getch() == 'esc':
        #     print('Esc key pressed , stopping and exiting the constant Alert with odds function ....')
        #     break TODO
        for site_data in all_split_sites_data:

            for key in site_data.keys():
                if Bookie1_used in key:
                    continue
                
                # store the bookie's name so as to send onto Paul et al to double check & place the bet...
                bookie_name = key.split('_')[1]  

                # check exact match for event -> i.e date,competition and two teams - in home/away order also for the necessary unique 'hit'
                if all(x in key for x in sub_strs_in_key) :

                    if oddType == 0 and float(site_data[key][oddType]) > expect_oddValue:
                        send_mail_alert_odds_thresh(expect_oddValue, site_data[key][0], teamA, teamB, date, competition, bookie_name)
                    elif oddType and float(site_data[key][oddType]) > expect_oddValue:
                        send_mail_alert_odds_thresh(expect_oddValue, site_data[key][oddType], teamA, teamB, date, competition, bookie_name)  
                    else:
                        print('issue with finding /checking the expected odd across all data and sites...')
                        return False
   
    return True


def check_for_sure_bets():

    #global refernce_champ_league_gamesDict, site_unibet_champ_league_gamse, sites_zebetchamp_league_gamse, site4s_champ_league_gamse, site5s_champ_league_gamse

    global all_split_sites_data, DEBUG_OUTPUT

    #remove bookies uused:
    
    #all_srpaed_sites_data.remove(Bookie1_used)
    #if(Bookie2_used):
    #    all_srpaed_sites_data.remove(Bookie2_used)

    #sub_strs_in_key = [date.lower(),competition.lower(),teamA.lower(),teamB.lower()]

    # search for game (and competition and date to ensure uniqueness) on ref. site:
    while(True):

        # intro randomness to not get caught ! - lol
        wait_time = random.randint(1,4)
        time.sleep(wait_time)
        
        #print('Click on the "esc" key @ any time to terminate this program and can then restart again any time you wish :) ......')

        # waitr a delay time to refresh sites parsings....
        if parseSites(): #all_srpaed_sites_data):
            pass
        else:
            print("Error i parsing function...retring... But needs diagnostics and/or a fix ! ...")
            continue
        
        ## !!! THIS PIECE OF CODE SEEMS TO BE BREAKING THE PROGRAM - CAUSING IT TO HAVE VERY UNDEFINED RUNTIME BEHAVIOUT ???     
        # if msvcrt.getch() == 'esc':
        #     print('Esc key pressed , stopping and exiting the constant Alert with odds function ....')
        #     break

        # for site_data in all_srpaed_sites_data:
        #     # fix one and find other combos of remaining 2...

        #     rmv_all_srpaed_sites_data = all_srpaed_sites_data.remove(site_data)
        #     #for key in site_data.keys():
            #for site_1,site_2 in all_srpaed_sites_data
                #bookie_name = key.split('_')[1]  

        ## removed - commented out old version fpr now ..        
        # for site_data in full_all_bookies_allLeagues_match_data:
        # # fix one and find other combos of remaining 2...
        #     rmvRef_all_srpaed_sites_data = full_all_bookies_allLeagues_match_data.pop(site_data)
 
    ## TODO  - a biggg TODO  -- convert this to just the combos of 3 and exclude this loop above ...09
    for subset in itertools.combinations(all_split_sites_data, 3):  
        #filter unique games across dicts/sites using the key from a fixed one ....   
            
        subsetList = list(subset)               
        if DEBUG_OUTPUT :
            print('subset[0] = ' + str(subset[0])) 
            print('subset[1] = ' + str(subset[1])) 

        bookie_1 = key.split('_')[0]
        for key in site_data.keys():

            if DEBUG_OUTPUT :
                print('site_data key = ' + str(key)) 

            if key in subsetList[0] and key in subsetList[1]:

                # parse key for teams, date and competition:
                ##  ??  parse code her ??\ ---  m ads MUST CHECk you are seaching the exact same UIQUE match.
                bookie_2 = key.split('_')[0]
                bookie_3 = key.split('_')[0]

                if check_is_surebet(site_data[key][0],subsetList[0][1],subsetList[1][2]):  # encode bookie outcomes as 'W','D','L' wrt to the 1st team in the match descrpt. , i.e The 'hometeam'    
                    send_mail_alert_gen_socer_surebet(site_data.split('_')[1],subsetList[0].split('_')[1],subsetList[1].split('_')[1] ,'L', 'W','marseilles','nantes','smaedi 28 novembre','ligue 1')

                if check_is_surebet(site_data[key][0],subsetList[0][2],subsetList[1][1]):
                    send_mail_alert_gen_socer_surebet(bookie_1 ,bookie_2 ,bookie_3 ,bookie_one_outcome ,bookie_2_outcome ,teamA ,teamB ,date ,competition)

                if check_is_surebet(site_data[key][1],subsetList[0][0],subsetList[1][2]):
                    send_mail_alert_gen_socer_surebet(bookie_1,bookie_2,bookie_3,bookie_one_outcome, bookie_2_outcome,teamA,teamB,date,competition) 

                if check_is_surebet(site_data[key][1],subsetList[0][2],subsetList[1][0]):
                    send_mail_alert_gen_socer_surebet(bookie_1,bookie_2,bookie_3,bookie_one_outcome, bookie_2_outcome,teamA,teamB,date,competition) 

                if check_is_surebet(site_data[key][2],subsetList[0][1],subsetList[1][0]):
                    send_mail_alert_gen_socer_surebet(bookie_1,bookie_2,bookie_3,bookie_one_outcome, bookie_2_outcome,teamA,teamB,date,competition)                            

                if check_is_surebet(site_data[key][2],subsetList[0][0],subsetList[1][1]):
                    send_mail_alert_gen_socer_surebet(bookie_1,bookie_2,bookie_3,bookie_one_outcome, bookie_2_outcome,teamA,teamB,date,competition)                            

    ## can't recall purpose of this shite... ??
    #print(subset)  
    #site_data[key][oddType]

    return True

## TODO :
# def try_catch_function():
#     exceptionBool = False

#     return exceptionBool

#if only soing 2 - way sure bet , then oddDraw can be set to -1 and used as such when read in here
def send_mail_alert_odds_thresh(init_oddA,expect_oddB,teamA,teamB,date,competition,bookiesNameEventB):

    global DEBUG_OUTPUT
    successFlag = False
    sender = 'godlikester@gmail.com'
    receivers = ['crowledj@tcd.ie']#'pauldarmas@gmail.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    The is an Alert to tell you that the bookmaker - 
    """ +  "\033[1m" + str(bookiesNameEventB) + """ has its odd's on team B - """ +  "\033[1m" + str(teamB) + """ to win the event against """ +  "\033[1m" + str(teamA) + """ \
    in the competition """ +  "\033[1m" + str(competition) + """ reach a value of """ +  "\033[1m" + str(expect_oddB) +  """ at approxs
    hh:mm:ss o clock on zz day of MM / 20YY """ 

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.gmail.com",465)
        smtpObj.login("godlikester@gmail.com", "Elnino_9")
        smtpObj.sendmail(sender, receivers, message)     

        if DEBUG_OUTPUT :
            print("Successfully sent email")

        successFlag = True
    except SMTPException:
        print("Error: unable to send email")
        pass

    return successFlag


def send_mail_alert_gen_socer_surebet(bookie_1,bookie_2,bookie_3,bookie_one_outcome, bookie_2_outcome,teamA,teamB,date,competition):

    global DEBUG_OUTPUT
    successFlag = False
    sender = 'godlikester@gmail.com'
    receivers = ['crowledj@tcd.ie']#'pauldarmas@gmail.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    The is an Alert to tell you that a three-way soccer sure bet exists between --""" + str(teamA) + """ and  """ + str(teamB) + """  in the event """ + str(competition) + """  \
    on the date  """ + str(date) + """  the bet will involve placing a bet on """ + str(bookie_one_outcome) + """  in the bookies - """ + str(bookie_1) + """ and on the outcome """ \
    + str(bookie_2_outcome) + """ in the """ + str(bookie_2) +  """ bookie and final 3rd bet left in  """ + str(bookie_3)

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


def parseSites(): 

    global websites_champs_league_links, compettition, date, refernce_champ_league_gamesDict, full_all_bookies_allLeagues_match_data, DEBUG_OUTPUT

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

            if DEBUG_OUTPUT:
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
        full_all_bookies_allLeagues_match_data[ france_pari + '_' + date.lower() + '_' + competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_teamA) 
        full_all_bookies_allLeagues_match_data[ france_pari + '_' + date.lower() + '_' +  competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_draw)
        full_all_bookies_allLeagues_match_data[ france_pari + '_' + date.lower() + '_' +  competition.lower() + '_' + team_names_string.split('parier-sur-')[1].lower()].append(odds_string_teamB)

    if DEBUG_OUTPUT:
        print('all good the find_elements_by_xpath Call worked GRAND !! :) --- full champ league games data struct = ')
        print(refernce_champ_league_gamesDict)
    #login_form =  driver.find_element_by_id("PARIS SPORTIFS")

    #############################     TEST ALERT - send to Paul darmas    #############################

    #send Alert to paul's mail:
    #send_mail_alert(2.5,3.25,'Liverpool','Barcelona','01/04/2021','Champions League','Unibet')

    #############################     TEST ALERT - send to Paul darmas    #############################

    # #Next loop thru all other SITE's champ league games besides  france-pari site as its the reference to compare to...
    for i,sites in enumerate(websites_champs_league_links[1:]):

        #begin = timeit.timeit()  
        driver.get(sites)
        #finish = timeit.timeit()

        if  unibet in sites :
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

                    full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(teamAWinOdds.split(' ')[1].replace(',','.').lower())  #=   teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(draw_odds.split(' ')[1].replace(',','.').lower())
                    full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(teamBWinOdds.split(' ')[1].replace(',','.').lower())    
                    #check = 1


            except: #  NoSuchElementException:
                any_errors = False
                print("Error  ->  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue
            #check = 1

        
        if  zebet in sites :
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
                    #print(matches.text)
                    split_match_data_str = matches.text.split('\n') 
                    date = split_match_data_str[0]
                    teams = split_match_data_str[2] + '_' + split_match_data_str[6]
                    competition =  compettition #split_match_data_str[1]    
                    teamAWinOdds = split_match_data_str[1].replace(',','.')
                    teamBWinOdds = split_match_data_str[3].replace(',','.')
                    draw_odds    = split_match_data_str[5].replace(',','.')

                    full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
                    full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            except NoSuchElementException:
                any_errors = False
                print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue


        if winimax in sites :
        # unibet tree struct to games elements:

            try:
                #start = timeit.timeit()
                champ_league_games_nested_gamesinfo_winimax = driver.find_elements_by_xpath('/html/body/div[@id="global"]/div[@id="content"]/main[@class="uk-flex-item-1 uk-width-7-12"]/section/ \
                div[@class="uk-block-20-20 uk-block-small-10-10"]/div[@id="event"]/article[@class="item"]/div[@class="uk-accordion uk-accordion-block item"]/ \
                div[@class="uk-accordion-wrapper item-bloc item"]/div/div[@class="uk-accordion-content uk-padding-remove uk-active"]/div/div[@class="item-content catcomp item-bloc-type-1"]')
                    #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
                #end = timeit.time
                #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

                for matches in  champ_league_games_nested_gamesinfo_winimax:
                    #print(matches.text)
                    split_match_data_str = matches.text.split('\n') 
                    date = split_match_data_str[0]
                    teams = split_match_data_str[2] + '_' + split_match_data_str[6]
                    competition =  compettition #split_match_data_str[1]    
                    teamAWinOdds = split_match_data_str[1].replace(',','.')
                    teamBWinOdds = split_match_data_str[3].replace(',','.')
                    draw_odds    = split_match_data_str[5].replace(',','.')

                    full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
                    full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            except NoSuchElementException:
                any_errors = False
                print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue

        if sports_bwin in sites :
        # unibet tree struct to games elements:

            try:
                #start = timeit.timeit()
                champ_league_games_nested_gamesinfo_sportsbwin = driver.find_elements_by_xpath('/html/body/div[@id="global"]/div[@id="content"]/main[@class="uk-flex-item-1 uk-width-7-12"]/section/ \
                div[@class="uk-block-20-20 uk-block-small-10-10"]/div[@id="event"]/article[@class="item"]/div[@class="uk-accordion uk-accordion-block item"]/ \
                div[@class="uk-accordion-wrapper item-bloc item"]/div/div[@class="uk-accordion-content uk-padding-remove uk-active"]/div/div[@class="item-content catcomp item-bloc-type-1"]')
                    #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
                #end = timeit.time
                #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

                for matches in  champ_league_games_nested_gamesinfo_sportsbwin:
                    #print(matches.text)
                    split_match_data_str = matches.text.split('\n') 
                    date = split_match_data_str[0]
                    teams = split_match_data_str[2] + '_' + split_match_data_str[6]
                    competition =  compettition #split_match_data_str[1]    
                    teamAWinOdds = split_match_data_str[1].replace(',','.')
                    teamBWinOdds = split_match_data_str[3].replace(',','.')
                    draw_odds    = split_match_data_str[5].replace(',','.')

                    full_all_bookies_allLeagues_match_data[ sports_bwin + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                    full_all_bookies_allLeagues_match_data[ sports_bwin + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
                    full_all_bookies_allLeagues_match_data[ sports_bwin + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            except NoSuchElementException:
                any_errors = False
                print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                continue


    # for i,sites in enumerate(websites_europa_league_links):

    #         #begin = timeit.timeit()  
    #         driver.get(sites)
    #         #finish = timeit.timeit()

    #         if sites.startswith('france-pari',12) or sites.startswith('france-pari',11) :
    #         # unibet tree struct to games elements:

    #             # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
    #             try:
    #                 #start = timeit.timeit()
    #                 europa_league_games_nested_gamesinfo_unibet = driver.find_elements_by_xpath('/html/body/div[@id="container"]/div[@id="wrapper"]/div[@id="content-container"]/div[@id="content"]/section/div[@id="main"] \
    #                 /section[@id="view-main-container"]/div[@id="view-main"]/section[@id="page__competitionview"]/div[@class="view view-eventpath"]/div[@class="page-wrap"] \
    #                 /div[@class="scroller"]/div[@class="ui-splitview"]/div[@class="ui-splitview-item ui-splitview-left"]/div[@class="i-splitview-item-inner"]/div[@class="c-eventpathlist bettingbox"] \
    #                 /div[@class="ui-mainview-block eventpath-wrapper"]/div[@class="bettingbox-item box"]/div[@class="bettingbox-content oddsbox-hide-marketname bettingbox-wide"]/div[@class="ui-touchlink had-market inline-market calendar-event cell"]') 
    #                 #end = timeit.timeit()
    #                 #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

    #                 for matches in  europa_league_games_nested_gamesinfo_unibet:
    #                     #print(matches.text)
    #                     split_match_data_str = matches.text.split('\n') 
    #                     teams = split_match_data_str[0]
    #                     competition =  split_match_data_str[1]
    #                     teamAWinOdds = split_match_data_str[2]
    #                     teamBWinOdds = split_match_data_str[6]
    #                     draw_odds    = split_match_data_str[4]

    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(teamAWinOdds.split(' ')[1].replace(',','.').lower())  #=   teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(draw_odds.split(' ')[1].replace(',','.').lower())
    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(teamBWinOdds.split(' ')[1].replace(',','.').lower())    
    #                     #check = 1


    #             except: #  NoSuchElementException:
    #                 any_errors = False
    #                 print("Error  ->  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    #                 continue


    #         if sites.startswith('unibet',12) or sites.startswith('unibet',11) :
    #         # unibet tree struct to games elements:

    #             # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
    #             try:
    #                 #start = timeit.timeit()
    #                 europa_league_games_nested_gamesinfo_unibet = driver.find_elements_by_xpath('/html/body/div[@id="container"]/div[@id="wrapper"]/div[@id="content-container"]/div[@id="content"]/section/div[@id="main"] \
    #                 /section[@id="view-main-container"]/div[@id="view-main"]/section[@id="page__competitionview"]/div[@class="view view-eventpath"]/div[@class="page-wrap"] \
    #                 /div[@class="scroller"]/div[@class="ui-splitview"]/div[@class="ui-splitview-item ui-splitview-left"]/div[@class="i-splitview-item-inner"]/div[@class="c-eventpathlist bettingbox"] \
    #                 /div[@class="ui-mainview-block eventpath-wrapper"]/div[@class="bettingbox-item box"]/div[@class="bettingbox-content oddsbox-hide-marketname bettingbox-wide"]/div[@class="ui-touchlink had-market inline-market calendar-event cell"]') 
    #                 #end = timeit.timeit()
    #                 #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

    #                 for matches in  europa_league_games_nested_gamesinfo_unibet:
    #                     #print(matches.text)
    #                     split_match_data_str = matches.text.split('\n') 
    #                     teams = split_match_data_str[0]
    #                     competition =  split_match_data_str[1]
    #                     teamAWinOdds = split_match_data_str[2]
    #                     teamBWinOdds = split_match_data_str[6]
    #                     draw_odds    = split_match_data_str[4]

    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(teamAWinOdds.split(' ')[1].replace(',','.').lower())  #=   teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(draw_odds.split(' ')[1].replace(',','.').lower())
    #                     all_crapedSites_data[i][date.lower() + '_' + competition.lower() + '_' + teams].append(teamBWinOdds.split(' ')[1].replace(',','.').lower())    
    #                     #check = 1


    #             except: #  NoSuchElementException:
    #                 any_errors = False
    #                 print("Error  ->  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    #                 continue
    #             #check = 1

            
    #         if sites.startswith('zebet',12) or sites.startswith('zebet',11) :
    #         # unibet tree struct to games elements:

    #             try:
    #                 #start = timeit.timeit()
    #                 europa_league_games_nested_gamesinfo_zebet = driver.find_elements_by_xpath('/html/body/div[@id="global"]/div[@id="content"]/main[@class="uk-flex-item-1 uk-width-7-12"]/section/ \
    #                 div[@class="uk-block-20-20 uk-block-small-10-10"]/div[@id="event"]/article[@class="item"]/div[@class="uk-accordion uk-accordion-block item"]/ \
    #                 div[@class="uk-accordion-wrapper item-bloc item"]/div/div[@class="uk-accordion-content uk-padding-remove uk-active"]/div/div[@class="item-content catcomp item-bloc-type-1"]')
    #                     #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
    #                 #end = timeit.time
    #                 #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

    #                 for matches in  europa_league_games_nested_gamesinfo_zebet:
    #                     print(matches.text)
    #                     split_match_data_str = matches.text.split('\n') 
    #                     date = split_match_data_str[0]
    #                     teams = split_match_data_str[2] + '_' + split_match_data_str[6]
    #                     competition =  compettition #split_match_data_str[1]    
    #                     teamAWinOdds = split_match_data_str[1].replace(',','.')
    #                     teamBWinOdds = split_match_data_str[3].replace(',','.')
    #                     draw_odds    = split_match_data_str[5].replace(',','.')

    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

    #             except NoSuchElementException:
    #                 any_errors = False
    #                 print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    #                 continue


    #         if sites.startswith('winimax',12) or sites.startswith('winimax',11) :
    #         # unibet tree struct to games elements:

    #             try:
    #                 #start = timeit.timeit()
    #                 europa_league_gamesinfo_winimax = driver.find_elements_by_xpath('//*[@id="app-inner"]/span/div/div[2]/div/section/div/div[1]/div/div/div') #'/html/body/div[3]/div/div/section/div/div[1]/div/span/div/div[2]/div/section/div/div[1]/div/div/div[2]')
                                                 
    #                 for matches in  europa_league_gamesinfo_winimax:

    #                     team_names = matches.find_element_by_xpath('//div/a/div/div').text.split('vs')
    #                     team_nameA = team_names[0]
    #                     team_nameB = team_names[1].split('\n')[0]
    #                     teams = team_nameA + team_nameB

    #                     competition =  compettition #split_match_data_str[1] 

    #                     team_odds = matches.find_element_by_xpath('//div/div/div/div/button/span')

    #                     #for odds in team_odds:
    #                     teamAWinOdds = team_odds[0]
    #                     draw_odds    = team_odds[1]
    #                     teamBWinOdds = team_odds[2]

    #                     teamAWinOdds = split_match_data_str[1].replace(',','.')
    #                     teamBWinOdds = split_match_data_str[3].replace(',','.')
    #                     draw_odds    = split_match_data_str[5].replace(',','.')

    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

    #             except NoSuchElementException:
    #                 any_errors = False
    #                 print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    #                 continue

    #         if sites.startswith('sports.bwin',8) or sites.startswith('sports.bwin'9) :
    #         # unibet tree struct to games elements:

    #             try:
    #                 #start = timeit.timeit()
    #                 europa_league_games_nested_gamesinfo_zebet = driver.find_elements_by_xpath('/html/body/div[@id="global"]/div[@id="content"]/main[@class="uk-flex-item-1 uk-width-7-12"]/section/ \
    #                 div[@class="uk-block-20-20 uk-block-small-10-10"]/div[@id="event"]/article[@class="item"]/div[@class="uk-accordion uk-accordion-block item"]/ \
    #                 div[@class="uk-accordion-wrapper item-bloc item"]/div/div[@class="uk-accordion-content uk-padding-remove uk-active"]/div/div[@class="item-content catcomp item-bloc-type-1"]')
    #                     #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
    #                 #end = timeit.time
    #                 #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

    #                 for matches in  europa_league_games_nested_gamesinfo_zebet:
    #                     print(matches.text)
    #                     split_match_data_str = matches.text.split('\n') 
    #                     date = split_match_data_str[0]
    #                     teams = split_match_data_str[2] + '_' + split_match_data_str[6]
    #                     competition =  compettition #split_match_data_str[1]    
    #                     teamAWinOdds = split_match_data_str[1].replace(',','.')
    #                     teamBWinOdds = split_match_data_str[3].replace(',','.')
    #                     draw_odds    = split_match_data_str[5].replace(',','.')

    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
    #                     all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

    #             except NoSuchElementException:
    #                 any_errors = False
    #                 print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
    #                 continue            



    for i,sites in enumerate(websites_ligue1_links):

            #begin = timeit.timeit()  
            driver.get(sites)
            #finish = timeit.timeit()
            compettition_ = 'ligue1'

            if  unibet in sites :
            # unibet tree struct to games elements:

                # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
                try:
 
                    ligue1_games_nested_gamesinfo_unibet =  driver.find_elements_by_xpath('//*[@id="page__competitionview"]/div/div[1]/div[2]/div/div/div/div[3]/div[2]')
                    #end = timeit.timeit()
                    #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

                    for matches in  ligue1_games_nested_gamesinfo_unibet:

                        date = driver.find_element_by_xpath('//div[2]/h2/span').text
                        competition =  compettition_
                        teams = driver.find_element_by_xpath('//div[2]/div[1]/div/div/div/div/div/div[1]/div').text.split('\n')[0]
                        teamAWinOdds = driver.find_element_by_xpath('//div[1]/div/div/div[2]/div/section/div/div/span/span/span[@class="ui-touchlink-needsclick price odd-price"]').text
                        #//*[@id="71b4da2a-b84f-4d3d-8fc3-76e13b09355f"]/div/span[1]/span[1]/span[4]
                        draw_odds = driver.find_element_by_xpath('//div[1]/div/div/div[2]/div/section/div/div/span[2]/span/span[@class="ui-touchlink-needsclick price odd-price"]').text
                        teamBWinOdds = driver.find_element_by_xpath('//div[1]/div/div/div[2]/div/section/div/div/span[3]/span/span[@class="ui-touchlink-needsclick price odd-price"]').text

                        full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(teamAWinOdds.split(' ')[1].replace(',','.').lower())  #=   teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                        full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(draw_odds.split(' ')[1].replace(',','.').lower())
                        full_all_bookies_allLeagues_match_data[ unibet + '_' + date.lower() + '_' + competition.lower() + '_' + teams].append(teamBWinOdds.split(' ')[1].replace(',','.').lower())    
                        #check = 1

                except: #  NoSuchElementException:
                    any_errors = False
                    print("Error  ->  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                    continue
                #check = 1
        
            # if  zebet in sites :
            # # unibet tree struct to games elements:                                                     

            #     try:

            #         # TODO : need to actually make call into zebet champ league page to get champ_league_games_nested_gamesinfo_zebet:

            #         for matches in  champ_league_games_nested_gamesinfo_zebet:
            #             print(matches.text)
            #             split_match_data_str = matches.text.split('\n') 
            #             date = split_match_data_str[0]
            #             teams = split_match_data_str[2] + '_' + split_match_data_str[6]
            #             competition =  compettition #split_match_data_str[1]    
            #             teamAWinOdds = split_match_data_str[1].replace(',','.')
            #             teamBWinOdds = split_match_data_str[3].replace(',','.')
            #             draw_odds    = split_match_data_str[5].replace(',','.')

            #             full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
            #             full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
            #             full_all_bookies_allLeagues_match_data[ zebet + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            #     except NoSuchElementException:
            #         any_errors = False
            #         print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
            #         continue

            # full path copied from sourcecode tool       
            #/html/body/div[3]/div/div/section/div/div[1]/div/span/div/div[2]/div/section/div/div[1]/div/div/div[2]


            if winimax in sites :
            # unibet tree struct to games elements:
                try:

                    ligue1_games_nested_gamesinfo_winimax = driver.find_elements_by_xpath('//*[@id="app-inner"]/span/div/div[2]/div/section/div/div[1]/div/div/div') #'/html/body/div[3]/div/div/section/div/div[1]/div/span/div/div[2]/div/section/div/div[1]/div/div/div[2]')
                                                 
                    for matches in  ligue1_games_nested_gamesinfo_winimax:

                        team_names = matches.find_element_by_xpath('//div/a/div/div').text.split('vs')
                        team_nameA = team_names[0]
                        team_nameB = team_names[1].split('\n')[0]
                        teams = team_nameA + team_nameB

                        competition =  compettition #split_match_data_str[1] 
                        team_odds = matches.find_element_by_xpath('//div/div/div/div/button/span')

                        #for odds in team_odds:
                        teamAWinOdds = team_odds[0]
                        draw_odds    = team_odds[1]
                        teamBWinOdds = team_odds[2]

                        teamAWinOdds = split_match_data_str[1].replace(',','.')
                        teamBWinOdds = split_match_data_str[3].replace(',','.')
                        draw_odds    = split_match_data_str[5].replace(',','.')

                        full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
                        full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
                        full_all_bookies_allLeagues_match_data[ winimax + '_' + date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

                except NoSuchElementException:
                    any_errors = False
                    print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
                    continue

            # if sites.startswith('sports.bwin',8) or sites.startswith('sports.bwin'9) :
            # # unibet tree struct to games elements:
            #     try:

            #         #     # now navigate using the driver and xpathFind to get to the matches section of Ref. site :
            #         #end = timeit.time
            #         #print('Time taken to scrape unibets champ league shit was = ' + str(end - start)) 

            #         for matches in  champ_league_games_nested_gamesinfo_zebet:
            #             print(matches.text)
            #             split_match_data_str = matches.text.split('\n') 
            #             date = split_match_data_str[0]
            #             teams = split_match_data_str[2] + '_' + split_match_data_str[6]
            #             competition =  compettition #split_match_data_str[1]    
            #             teamAWinOdds = split_match_data_str[1].replace(',','.')
            #             teamBWinOdds = split_match_data_str[3].replace(',','.')
            #             draw_odds    = split_match_data_str[5].replace(',','.')

            #             all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamAWinOdds) #= teamAWinOdds + '_' + draw_odds + '_' + teamBWinOdds
            #             all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(draw_odds)
            #             all_crapedSites_data[i][date.lower() + competition.lower() + '_' + teams.lower()].append(teamBWinOdds)

            #     except NoSuchElementException:
            #         any_errors = False
            #         print("Error  caught in your find_elements_by_xpath() call -- NoSuchElementException ! :( ")
            #         continue            


    ## create sepaarate dicts for each bookies :
    unibet_dict      = defaultdict(list)
    betclic_dict     = defaultdict(list)
    winimax_dict     = defaultdict(list)
    zebet_dict       = defaultdict(list)
    sports_bwin_dict = defaultdict(list)
    france_pari_dict = defaultdict(list)
    pasinobet_dict   = defaultdict(list)
    pasinobet_dict   = defaultdict(list)

    all_split_sites_data = []
    
    if len(full_all_bookies_allLeagues_match_data) == 0:
        print("Empty full_data dict encountered -- fix !")
        return False 
        

    items = full_all_bookies_allLeagues_match_data.items() 
    for item in items: 

        try:
            keys = item[0]
            values = item[1]

        except KeyError:        
            print("Error -- key value does not exist in the full_data dict. ! -- return False as a failure from the parsing function...")
            return False    
        
        if unibet in keys:
            unibet_dict[keys] = values
            all_split_sites_data.append(unibet_dict)

        if betclic in keys:
            betclic_dict[keys] = values
            all_split_sites_data.append(betclic_dict)

        if winimax in keys:
            winimax_dict[keys] = values
            all_split_sites_data.append(winimax_dict)

        if zebet in keys:
            zebet_dict[keys] = values
            all_split_sites_data.append(zebet_dict)

        if sports_bwin in keys:
            sports_bwin_dict[keys] = values
            all_split_sites_data.append(sports_bwin_dict)

        if france_pari in keys:
            france_pari_dict[keys] = values
            all_split_sites_data.append(france_pari_dict)

        if pasinobet in keys:
            pasinobet_dict[keys] = values
            all_split_sites_data.append(pasinobet_dict)

    driver.quit()
    return any_errors

if __name__ == '__main__':

    argv = sys.argv
    DEBUG_OUTPUT  = False

    # if len(argv) < 1 :
    #     print("usage:  please indicate with  0 or a 1 in the first cmd line argument to the program wherether you wish to include debugging output prints in it's run or not; 0/1 corresponding to no/yes....")
    # else:    
    #     DEBUG_OUTPUT = bool(int(argv[1]))


    #print('Running unit tests on sportsbetting applicationb version 1....')
    #unittest.main()


    #retVal = odds_alert_system(oddType=2,expect_oddValue=2.35,teamA='liverpool',teamB='atalanta',date='Mercredi 25 Novembre',competition='Ligue des Champions',Bookie1_used='Winimax',Bookie2_used='')


    retval2 = check_for_sure_bets() #'unibet','zebet','winimaxc','W', 'D','marseilles','nantes','28/11/2020','ligue 1 UberEats')

    debug = -10

