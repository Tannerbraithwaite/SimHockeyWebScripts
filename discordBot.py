# bot.py
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
import json
import requests
import discord
from datetime import date


##Load data from an env file
load_dotenv()

#get the token
TOKEN = os.getenv('DISCORD_TOKEN')

#set the header for the server
api_key = os.getenv('X-API-Key')

#BaseURL for the API data
api_url_base = 'https://api.simhockey.ca/'

#create a header to send
headers = {'X-API-Key': api_key}

#Establish the default date variable
today=date.today()


#Get the scores from the api and return a formatted string
def get_scores(date=str(today)):
    appended_date='{0}scores/'+str(date) ##Create substring for the URL
    api_url = appended_date.format(api_url_base) ##format the API URL
    response = requests.get(api_url, headers=headers) ## Get the response from the URL
    if response.status_code == 200: ## If Response is successful do this
        score_info_json = json.loads(response.content.decode('utf-8')) ##Create a score info JSON object
        game_score=''
        teams=''
        if score_info_json['code'] == 404: ##Return None is response wasn't successful
            return None
        for score in score_info_json['data']: ## Sort through the teams in the data and append their data to the game scores object
            game_score = game_score  + f"{score['home']}" + f"{score['home_score']}".rjust(20-len(score['home'])) +'\n'+  f"{score['away']}" + f"{score['away_score']}".rjust(20-len(score['away']))+'\n' + '\n'
        return game_score ## Return the game scores to the command function
    else:
        return None


#Bot command to get the requested info uses the $ sign
bot = commands.Bot(command_prefix='$')

#Command for getting the scores by the date
@bot.command(name='scores', help="type /scores followed by the date(ie. /score 2020-03-29) to get the scores for a specific date")
async def scoredate(ctx, date=str(today)): ##Use today if no date is provided
    scores= get_scores(date) ##Call the API
    no_data_message = "We could not find any games for that date"
    if scores == None: ##If the API Returns an unsuccessful method, send the no_data_message response
        await ctx.send(no_data_message)
    else:
        title_score = "the scores for " + str(date) ##Create a title
        scores_formatted = "```" + scores + "```" ##format for embedding into discord
        embed = discord.Embed(title=title_score, color=0xeee657) ##create an embedded object
        embed.add_field(name="Scores", value=scores_formatted) #Embed the value into the Embedded object
        await ctx.send(embed=embed) ##Send the object to Discord

##Get scores for a specific team
def get_scores_by_team(team):
    appended_team='{0}scores/'+team ##Create the string for the URL
    api_url = appended_team.format(api_url_base) ##Format the URL of the API
    response = requests.get(api_url, headers=headers) ##Get a response from the API
    if response.status_code == 200: ##If the response if successful do this
        score_info_json = json.loads(response.content.decode('utf-8')) ##Get the score information as a JSON Object
        game_score=''
        if score_info_json['code'] == 404: ##Return None if the API is not found(Invalid team)
            return None
        for score in score_info_json['data']: ##Cycle through the list of data in the JSON object and append the formatted information for the game_score object
            game_score = game_score  + f"{score['home']}" + f"{score['home_score']}".rjust(20-len(score['home'])) +'\n'+  f"{score['away']}" + f"{score['away_score']}".rjust(20-len(score['away']))+'\n' + '\n'
        return game_score ## Return the Game score to the Discord call
    else:
        return None ##IF call wasn't successful return None.

##Bot Command for getting the scores for a team by name
@bot.command(name='scores_for', help="type /scores followed by the team(ie. van, cgy, edm) to get the scores for a specific team")
async def scoreteam(ctx, team):
    no_data_message = "We could not find any games for that team, "
    scores= get_scores_by_team(team) ## Get the scores form the API call function
    if scores == None: ## Send the No_data_message if the functions returns None
        await ctx.send(no_data_message)
    else: ##If function was successful create an embed object
        title_team = "the scores for " + team.upper() ##Create title for Embed
        scores_formatted = "```" + scores + "```" ##Format the data for the embedded text into Discord
        embed = discord.Embed(title=title_team, color=0xeee657) ##Create the Embed Object
        embed.add_field(name=team.upper(), value=scores_formatted) ##Add the text to the embedded field
        await ctx.send(embed=embed) ## send the embed object to Discord

##Function for returning a list of teams with tradeblocks available
def get_tradeblock():
    appended_tradeblock='{0}tradeblock' ## Create a string for the URL
    api_url = appended_tradeblock.format(api_url_base)##Create the API URL and format it properly
    response = requests.get(api_url, headers=headers) ##get the response from the API
    if response.status_code == 200: ##IF response was successful do this
        tradeblock_info_json = json.loads(response.content.decode('utf-8')) ##Create the JSON Object
        tradeblockteams=''
        if tradeblock_info_json['code'] == 404: ##IF Call was unsuccessful return none
            return None
        for team in tradeblock_info_json['data']: ##Sort through the list of teams in the JSON object and append it to a string
            tradeblockteams = tradeblockteams + team +'\n'
        return tradeblockteams ##return the teams with tradeblocks
    else: ##Return None if the response wasn't successful
        return None

#Bot Command for getting the list of teams with tradeblocks
@bot.command(name='tradeblock', help="type /tradeblock to see the teams who have posts a tradeblock")
async def tradeblock(ctx):
    no_data_message = "No trade blocks seem to be posted at this time"
    tradeblock= get_tradeblock() ##Get the data from the API
    if tradeblock==None: ##Send the no_data_message if call was unsuccessful
        await ctx.send(no_data_message)
    else:
        embed = discord.Embed(title="Teams with tradeblocks", color=0xeee657) ##Create the discord Embed object
        embed.add_field(name='Teams', value=tradeblock) ##Add the string of teams to the discord object
        await ctx.send(embed=embed) ##Send the embed object to discord

#Get the tradeblock of a specific team
def get_tradeblock_by_team(team):
    appended_team='{0}tradeblock/'+team ##create the string to append to the API URL
    api_url = appended_team.format(api_url_base) ##Format the API URL
    response = requests.get(api_url, headers=headers) ##Get a response from the API
    if response.status_code == 200: ##If the response was successful fo this
        tradeblock_info_json = json.loads(response.content.decode('utf-8')) ##Create a JSON Object of the data
        assets=''
        if tradeblock_info_json['code'] == 404: ##If Response wasn't successful return None
            return None
        for asset in tradeblock_info_json['data']: ##Sort through the list of players and append their data to the return object
            if asset['entity_type'] == 'player': ##Append if the asset is a player
                assets=assets+ asset['position'] + ' ' + asset['first_name'] + ' ' + asset['last_name'] + '\n'
            if asset['entity_type'] == 'pick': ##Append if the asset is a pick
                assets=assets+ str(asset['pick_owner']) + ' ' + str(asset['pick_year']) + ' round ' + str(asset['pick_round']) + '\n'
        return assets ##Return the assets
    else: ##Return None if the call was unsuccessful
        return None

##BOt Command for getting a tradeblock from a team
@bot.command(name='tradeblock_for', help="type /tradeblock_for followed by the team(ie. van, cgy, edm) to get the tradeblock for a specific team")
async def tradeblock_for(ctx, team):
    no_data_message = "We could not find a tradeblock for that team, "
    tradeblocks= get_tradeblock_by_team(team) ##Get the call from the API
    if tradeblocks == None: ##If the call was unsuccessful return the No_data_message
        await ctx.send(no_data_message)
    else:
        title_team = "the tradeblock for " + team.upper() ##Create a title of call
        tradeblocks_formatted = "```" + tradeblocks + "```" ##format the text for discord
        embed = discord.Embed(title=title_team, color=0xeee657) ##Create the embed object
        embed.add_field(name=team.upper(), value=tradeblocks_formatted) ##Attach the tradeblock to the embed object
        await ctx.send(embed=embed) ##Send the Embed object to discord

##Get the standings of the whole league
def get_standings():
    appended_team='{0}standings/' ##create the string to be appended to the URL
    api_url = appended_team.format(api_url_base) ## format the URL for the API
    response = requests.get(api_url, headers=headers) ##Get a response from the API
    if response.status_code == 200: ##If the response was successful do this
        standings_info_json = json.loads(response.content.decode('utf-8')) ##Create a JSON Obeject with the data
        standings='\n'.ljust(4)+'Team' + 'GP'.rjust(4) + "W".rjust(4) + "L".rjust(4) + "OT".rjust(4) + "P".rjust(4) + '\n' #create a return value with the inital categories for the data
        if standings_info_json['code'] == 404: ##If call wasn't successful return None
            return None
        ##Combine all the data from the division to create the list of all teams in the league
        standings_info = standings_info_json['data']['Western']['Central']+standings_info_json['data']['Western']['Pacific']+standings_info_json['data']['Eastern']['Atlantic']+standings_info_json['data']['Eastern']['Metro']
        ##Sort the list by points, then GP, then regulation wings, then regulation overtime wins, then total wins
        standings_sorted=sorted(standings_info, key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))
        n=1
        for team in standings_sorted: ##Cycle through the teams and append them to the return value
            if n>9: ##Append and format the teams that are past 9th overall
                standings =standings+str(n)+'. ' + team['code'] +f"{team['gp']}".rjust(4) + f"{team['w']}".rjust(4) +f"{team['l']}".rjust(4) + f"{team['otl']}".rjust(4) + f"{team['pts']}".rjust(4)+'\n'
            else: ##Append and format the teams below 9th overall
                standings =standings+str(n)+'.  ' + team['code'] + f"{team['gp']}".rjust(4) + f"{team['w']}".rjust(4) +f"{team['l']}".rjust(4) + f"{team['otl']}".rjust(4) + f"{team['pts']}".rjust(4)+'\n'
            n+=1
        return standings ##Return the standings to the discord bot
    else:##If response is unsuccessful do this
        return None

##Bot Command to get the standings of the whole leage
@bot.command(name='standings', help="type /standings to get the standings in the league")
async def standings(ctx, divi="No divi"):
    divi=divi.capitalize()
    no_data_message = "We could not find the standings"
    print(divi)
    if divi == "Eastern" or divi== "Western":
        print("We are in the conference loop")
        Conference_standings= get_standings_by_conference(divi) ##Get the data from the API
        if get_standings_by_conference(divi) == None: ##if the response if None, send the No_data_message
            await ctx.send(no_data_message)
        else: ##if response was successful do this
            Conference_formatted = "```" + Conference_standings + "```" ##Format the return object for discord
            embed = discord.Embed(title=divi+" Standings", color=0xeee657) ##Create the return object
            embed.add_field(name=divi+" Standings", value=Conference_formatted, inline=False) ##Add the formatted string to the embed object
            await ctx.send(embed=embed) ##Send to discord
    elif divi == "Pacific" or divi== "Metro" or divi == "Atlantic" or divi== "Central" or divi == "Metropolitan":
        if divi=="Metropolitan": ##If user used Metropolitan, convert it to Metro
            divi="Metro"
        Division_standings= get_standings_by_division(divi) ##Get the division standings
        if Division_standings == None: ##If call was unsuccessful, return the No_Data_Message
            print("we are in the None loop for division standings")
            await ctx.send(no_data_message)
        else:
            Div_formatted = "```" + Division_standings + "```" ##Format the data for discord
            embed = discord.Embed(title="Division Standings", color=0xeee657) ##Create the Embed Object to send to Discord
            embed.add_field(name=divi, value=Div_formatted, inline=False) ## Embed the values into the embed object
            await ctx.send(embed=embed) ##Send the object to discord
    elif divi=="No divi":
        print("We are in the no divi loop")
        standings= get_standings() ##Get the call from the API
        if get_standings() == None: ##If Call is unsuccessful return the No_data_message
            await ctx.send(no_data_message)
        else: ##If call is successful do this
            standings1= "```"+standings.split('17.')[0]+"```" ##format the data split by teams below 17th place
            standings2= "```"+'17.'+standings.split('17.')[1]+"```" ##format the data split by teams above 17th place
            embed = discord.Embed(title="League Standings", color=0xeee657) ##Create the embed object to send to discord
            embed.add_field(name="League Standings", value=standings1, inline=False)##Add the top 16 teams to the embed object
            embed.add_field(name="----------------", value=standings2, inline=False) ##Add the rest of the teams to the embed object
            await ctx.send(embed=embed) ##Send the embed object to discord
    else:
        print("We are in the last else loop")
        await ctx.send(no_data_message)

##Get the standings of a conference
def get_standings_by_conference(conference):
    appended_conference='{0}standings/conf/'+conference ## create the string to append to the URL
    api_url = appended_conference.format(api_url_base) ## Create the API URL
    response = requests.get(api_url, headers=headers) ##Get a response from the API URL
    if response.status_code == 200: ##If the response if successful do this
        standings_info_json = json.loads(response.content.decode('utf-8')) ##Create the JSON Object
        Conference_standings ='\n'+'Team' + 'GP'.rjust(4) + "W".rjust(5) + "L".rjust(5) + "OT".rjust(5) + "P".rjust(5) + '\n' ##Create the return object with headers
        Division2_standings=''
        Division1_standings=''
        if standings_info_json['code'] == 404: ##If the response is unsuccessful do this
            return None
        if conference == 'Western': ##for the western conference
            ##Sort the standings of the top three(divisional playoff) teams
            Division2_standings = sorted(standings_info_json['data']['Central'],
                                           key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))[0:3]
            for team in Division2_standings: ##Attach the data from the top 3 teams to the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
            ##Sort the standings of the top three(divisional playoff) teams
            Division1_standings = sorted(standings_info_json['data']['Pacific'],
                                           key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))[0:3]
            Conference_standings=Conference_standings+"-----------------"+'\n' ##Add a barrier to show the seperation between conferences
            for team in Division1_standings: ##Attach the data from the top 3 teams to the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
            Conference_standings=Conference_standings+"-----------------"+'\n' ##add a barrier to show seperation
            Rest_Div1 = standings_info_json['data']['Central'][3:] ##Get the rest of the teams
            Rest_Div2 = standings_info_json['data']['Pacific'][3:] ##Get the rest of the teams
            ##Sort all the teams by points, GP, RW, ROW, and W
            Rest_of_teams= sorted(Rest_Div1+Rest_Div2,
                                            key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))
            n=0
            for team in Rest_of_teams: ##Attach the data from the rest of the teams to the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
                n+=1
                if n==2: ## after the second team is appended add a barrier to show seperation of the wild card teams
                    Conference_standings=Conference_standings+"-----------------"+'\n'
        if conference == 'Eastern': ##If the conference is the eastern conference, do this
            ##Attach the data from the top 3 teams to the return object
            Division2_standings = sorted(standings_info_json['data']['Atlantic'],
                                           key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))[0:3]
            for team in Division2_standings:##Append the data from each team the the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
            ##Attach the data from the top 3 teams to the return object
            Division1_standings = sorted(standings_info_json['data']['Metro'],
                                           key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))[0:3]
            Conference_standings=Conference_standings+"-----------------"+'\n' ##Add a barrier to show seperations
            for team in Division1_standings:##Append the data from each team the the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
            Conference_standings=Conference_standings+"-----------------"+'\n' ##Add a barrier to show seperation
            ##Get the rest of the teams from each division
            Rest_Div1 = standings_info_json['data']['Atlantic'][3:]
            Rest_Div2 = standings_info_json['data']['Metro'][3:]
            ##Combine and sort the rest of the teams by pts, GP, rw, ROW, and W
            Rest_of_teams= sorted(Rest_Div1+Rest_Div2, key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))
            n=0
            for team in Rest_of_teams: ##Add the rest of the teams to the return object
                Conference_standings =Conference_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
                n+=1
                if n==2: ##After the first two teams(wildcard teams) are appended create a barrier to show seperation
                    Conference_standings=Conference_standings+"-----------------"+'\n'
        return Conference_standings ##Return the standings
    else: ##If the call is unsuccessful, return None.
        return None

##Bot command to get the standings of a conference
@bot.command(name='standings_conference', help="type /standings followed by a conference to get the standings in the conference")
async def standings_by_conference(ctx, conf):
    conf=conf.capitalize() ##ensure the conference is capatalized
    no_data_message = "We could not find the standings"
    Conference_standings= get_standings_by_conference(conf) ##Get the data from the API
    if get_standings_by_conference(conf) == None: ##if the response if None, send the No_data_message
        await ctx.send(no_data_message)
    else: ##if response was successful do this
        Conference_formatted = "```" + Conference_standings + "```" ##Format the return object for discord
        embed = discord.Embed(title=conf+" Standings", color=0xeee657) ##Create the return object
        embed.add_field(name=conf+" Standings", value=Conference_formatted, inline=False) ##Add the formatted string to the embed object
        await ctx.send(embed=embed) ##Send to discord

##Get the standings by division
def get_standings_by_division(division):
    appended_division='{0}standings/div/'+division ##Create the string to be attached to the URL
    api_url = appended_division.format(api_url_base) ##format and create the URL for the API
    response = requests.get(api_url, headers=headers) ##Get a response from the API
    if response.status_code == 200: ##IF response is successful, do this
        standings_info_json = json.loads(response.content.decode('utf-8')) ##Create a JSON object of the data
        Division_standings ='\n'+'Team' + 'GP'.rjust(4) + "W".rjust(5) + "L".rjust(5) + "OT".rjust(5) + "P".rjust(5) + '\n' ##create the return object with the headers
        if standings_info_json['code'] == 404: ##return None if the call wasn't successful
            return None
        #sort the teams in the division
        Division_standings_sorted = sorted(standings_info_json['data'],
                                       key=lambda k: (-int(k['pts']), int(k["gp"]), int(k["rw"]), int(k['row']), int(k['w'])))
        for team in Division_standings_sorted: ##Go through the list of teams and append their data to the return object
            Division_standings =Division_standings + team['code'] + f"{team['gp']}".rjust(5) + f"{team['w']}".rjust(5) +f"{team['l']}".rjust(5) + f"{team['otl']}".rjust(5) + f"{team['pts']}".rjust(5)+'\n'
        return Division_standings ##Return the standings to the discord call
    else:##Return None if the call wasn't successful
        return None

##Bot call to get the standings of a division
@bot.command(name='standings_division', help="type /standings followed by a division to get the standings in the division")
async def standings_by_division(ctx, div):
    div=div.capitalize() ##ensure the division is capatalized
    if div=="Metropolitan": ##If user used Metropolitan, convert it to Metro
        div="Metro"
    no_data_message = "We could not find the standings"
    Division_standings= get_standings_by_division(div) ##Get the division standings
    if get_standings_by_division(div) == None: ##If call was unsuccessful, return the No_Data_Message
        await ctx.send(no_data_message)
    else:
        Div_formatted = "```" + Division_standings + "```" ##Format the data for discord
        embed = discord.Embed(title="Division Standings", color=0xeee657) ##Create the Embed Object to send to Discord
        embed.add_field(name=div, value=Div_formatted, inline=False) ## Embed the values into the embed object
        await ctx.send(embed=embed) ##Send the object to discord

##Run the token with the Bot to Connect to the Channel
bot.run(TOKEN)
