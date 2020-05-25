import pandas as pd
import csv
players=[]
teams=[]
output_list=[]

def space_counter(name):
    count=0
    for a in name:
        if (a.isspace()):
            count+=1
    return count

with open('/Users/tannerbraithwaite/github/python_scripts/SimHockeyData/CCHL Draft Central - Taken Players.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[0] in (None, ""):
            continue
        if row[1] =='Team':
            continue
        if row[1] =='' :
            continue
        if row[1]=='St. Louis Blues':
            teams.append(row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Detroit Red Wings':
            teams.append(row[1].split(' ')[1]+ ' '+ row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Toronto Maple Leafs':
            teams.append(row[1].split(' ')[1]+ ' '+ row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Vegas Golden Knights':
            teams.append(row[1].split(' ')[1]+ ' '+ row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Columbus Blue Jackets':
            teams.append(row[1].split(' ')[1]+ ' '+ row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='New Jersey Devils':
            teams.append(row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Tampa Bay Lightning':
            teams.append(row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='Los Angeles Kings':
            teams.append(row[1].split(' ')[2])
            players.append(row[3])
        if row[1]=='San Jose Sharks':
            teams.append(row[1].split(' ')[2])
            players.append(row[3])
        if space_counter(row[1])==1:
            teams.append(row[1].split(' ')[1])
            players.append(row[3])


rows = zip(teams, players)
with open('playerteam.csv','w') as result_file:
    wr = csv.writer(result_file)
    for row in rows:
        wr.writerow(row)
