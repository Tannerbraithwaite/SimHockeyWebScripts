import requests
from bs4 import BeautifulSoup
import selenium
from datetime import date
import json
#substantiate the page to scrap data for constructing URLs
URL = 'https://frozenpool.dobbersports.com/frozenpool_linecombo.php'
page = requests.get(URL)
#substantiate the lists that will be deconstructed into URLs
list_of_teams=[]
list_of_player_first_name = []
list_of_player_last_name= []
list_of_player_value = []
list_of_teams_defense=[]
list_of_player_first_name_defense = []
list_of_player_last_name_defense= []
list_of_player_value_defense = []
list_of_URLs = []
data = {}
data = []
#URL for forwards and defenceman
begginning_url_string = 'https://frozenpool.dobbersports.com/frozenpool_linecombo.php?select=F&forward='
begginning_url_string_defence = 'https://frozenpool.dobbersports.com/frozenpool_linecombo.php?select=D&defenseman='
#create a Beautiful Soup Object
soup = BeautifulSoup(page.content, 'html.parser')
#get the list of forwards for parsing the data
results = soup.find(id='forward')
forwards = results.find_all('option')
#first result is the empty search
forwards.pop(0)

##Scrap data for teams, player first name, and player last name, and value
for player in forwards:
    if None in (player): ##check for None player types
        continue
    if player.text:
        if player.text[player.text.find("(")+1:player.text.find(")")] == '': ##check is the player had a team in the current year
            continue
        else:
            list_of_teams.append(player.text[player.text.find("(")+1:player.text.find(")")]) #find text for team in a string and append to the list of team
        if ' ' in player.text.split(',', 1)[0]:
            list_of_player_last_name.append(player.text.split(',', 1)[0].replace(' ', '+')) ## if last name has a space in it, replace with a + sign and append
        else:
            list_of_player_last_name.append(player.text.split(',', 1)[0]) ## if player last name does not have a space append the text for last name
        first_strip=player.text.split(', ', 1)[1] #find and append the players first name
        list_of_player_first_name.append(first_strip.split(" (", 1)[0])#find and append the players first name
        value_strip= player.attrs.get('value').split(":", 1)[1]
        list_of_player_value.append(value_strip.split(":", 1)[0])#find and append the players value

#get the list of defenseman for parsing the data
results_defence = soup.find(id='defenseman')
defensemans = results_defence.find_all('option')
defensemans.pop(0)

##checks players for the amount of spaces in their name
def space_counter(player_name):
    count=0
    for a in player_name:
        if (a.isspace()):
            count+=1
    return count

##Scrap data for teams, player first name, and player last name, and value for defenseman
for player in defensemans:
    if None in (player):##check for None player types
        continue
    if player.text:
        if player.text[player.text.find("(")+1:player.text.find(")")] == '': ## finds if the player had an active team this season
            continue
        else:
            list_of_teams_defense.append(player.text[player.text.find("(")+1:player.text.find(")")]) ##find the team and append to team list
        if space_counter(player.text)==3: ## handles players with two last names eg. Trevor Van Reimsdyk
            first_strip = player.text.split(' ')[1]+' '+player.text.split(' ')[2]
            list_of_player_last_name_defense.append(first_strip.replace(' ', '+')) ##append those players to a list of players last names
        else: ##handles players with less than 2 last names
            first_strip = player.text.split(' ')[1]
            list_of_player_last_name_defense.append(first_strip.split(' ', 1)[0]) ##appends players last names to the list of last names
        list_of_player_first_name_defense.append(player.text.split(' ', 1)[0]) ##append the players first name
        value_strip= player.attrs.get('value').split(":", 1)[1]
        list_of_player_value_defense.append(value_strip.split(":", 1)[0]) ##append the player value
        # else:
        #     list_of_player_last_name.append(player.text.split(',', 1)[0])
        # first_strip=player.text.split(', ', 1)[1]
        # list_of_player_first_name.append(first_strip.split(" (", 1)[0])
        # value_strip= player.attrs.get('value').split(":", 1)[1]
        # list_of_player_value.append(value_strip.split(":", 1)[0])

n=0
while n < len(list_of_player_first_name):
    ##check all lists are the same size
    assert len(list_of_player_value) == len(list_of_teams) == len(list_of_player_last_name) == len(list_of_player_first_name)
    ##reconstruct the URL
    URL = begginning_url_string+list_of_teams[n]+'%3A'+list_of_player_value[n]+'%3A'+list_of_player_first_name[n]+'%3A'+list_of_player_last_name[n] + '&games=2019-2020%3AR%3A99&period=ALL&situation=ALL'
    list_of_URLs.append(URL) ##Append the URL to the list of URL's
    n=n+1

n=0
while n < len(list_of_player_first_name_defense):
    ##check all lists are the same size
    assert len(list_of_player_value_defense) == len(list_of_teams_defense) == len(list_of_player_last_name_defense) == len(list_of_player_first_name_defense)
    ##Reconstruct the URL
    URL = begginning_url_string_defence+list_of_teams_defense[n]+'%3A'+list_of_player_value_defense[n]+'%3A'+list_of_player_first_name_defense[n]+'%3A'+list_of_player_last_name_defense[n] + '&games='+str(date.today().year - 1)+'-'+str(date.today().year)+'%3AR%3A99&period=ALL&situation=ALL'
    list_of_URLs.append(URL) ##Append the URL to the list of Url's
    n=n+1
##splits the string of players names and creates a list of players names to be parsed
def split_list(row):
    teammates = row[2]
    players = teammates.split('-')##Deliminate by - sign and create a list
    player = players[0]
    ##remove the players own name
    players.pop(0)
    for player in players:
        player_names = player.strip() ##remove white space
        team_mate_list.append(player_names) ## add to the list of teammates

# n=0
n=0
for URL in list_of_URLs:
    ##For testing purposes, as to not overload the database while developing, and see results quickly
    if n == 30:
        break
    n+=1
    ##Get page URL and create a Beautiful soup object with specific URLs
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')##find the table
    table_rows = table.find_all('tr')
    team_mate_list = []##create a list of an individual players teams mates

    if len(table_rows) == 0:##If player has no team mates, he didn't play, skip him
        print('player is not available')
        continue
    else:
        ##Parse through the row in a players team mates and create a list
        print('player is available')
        for tr in table_rows:
            td = tr.find_all('td') ##find table data
            row = [i.text for i in td] ##extract text
            split_list(row)
            teammates = row[2]
            players = teammates.split('-')
            player = players[0] ##get players name to dump into data
    team_mate_list=list(set(team_mate_list)) ##remove duplicates from the team mate list
    for team_mate in team_mate_list: ##For each team mate establish initial condition
        print('lets find the time it takes to do one teammate')
        total_chemistry=0.0
        EV_chemistry=0.0
        SH_chemistry=0.0
        PP_chemistry=0.0
        for tr in table_rows: ##for each row establish the text to be checked
            td = tr.find_all('td')
            row = [i.text for i in td]
            if team_mate in row[2]: ##Check if the teammate being parsed is in the row
                if row[1]=='SH': ## if the player data being compared is short handed Data, add the data to the total data Column and the short handed data column
                    total_chemistry+=float(row[0][:-1])
                    SH_chemistry+=float(row[0][:-1])
                if row[1]=='EV': ##If the data being compared is even strength data, add the data to the total data, and the even strength data
                    total_chemistry+=float(row[0][:-1])
                    EV_chemistry+=float(row[0][:-1])
                if row[1]=='PP': ## if the total data being compared is PP data, add the data to the total data, and the PP data
                    total_chemistry+=float(row[0][:-1])
                    PP_chemistry+=float(row[0][:-1])


        data.append({ ##Create a JSON object to input player data
            'player name': player,
            'teammate': team_mate,
            'Even strength chemistry': EV_chemistry,
            'Powerplay chemistry': PP_chemistry,
            'Total Chemistry': total_chemistry
            })
        with open('data.json', 'w') as outfile: ## write data to the Jason file
            json.dump(data, outfile)
