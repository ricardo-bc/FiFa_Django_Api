import sys
import subprocess





listImports = ['charset-normalizer','requests','psycopg2']

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

[install(imp) for imp in listImports]
print("Package Installed")

import requests as requesthttp
import json
import psycopg2

def saveFifaApiPlayers(page):
    try:
        request_query = requesthttp.get('https://www.easports.com/fifa/ultimate-team/api/fut/item?page='+str(page))
        if request_query.status_code == 200:
            conn = psycopg2.connect(
                host = "34.135.1.143",
                database = "postgres",
                user = "postgres",
                password = "andres117",
                port = "5432"
            )
            cursor = conn.cursor()
            data = json.loads(request_query.text)
            playersinfo = data['items']
            [savePlayerDB(player,page,cursor) for player in playersinfo]
            conn.commit()
            print('End Connection to DataBase')
        else:
            print("Error status_code Api Fifa"+str(request_query.status_code))
  
    except KeyError as e:
        print(e)
    except Exception as e:
        print(e)

def existPlayer(cursor,playername):
        query = "SELECT name FROM api_gamer where name = '"""+str(playername.replace("'",""))+ "'"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
def savePlayerDB(player,page,cursor):
    try:
        namePlayer = 'None'
        nationalityPlayer = 'None'
        positionPlayer ='None'
        teamPlayer ='None'
        if player['commonName'] != '':    
            namePlayer = player['commonName']
        else:
            namePlayer = player['firstName'] + ' ' + player['lastName']
        
        if player['nation']['name'] != '':    
            nationalityPlayer = player['nation']['name']
        if player['position'] != '':
            positionPlayer = player['position']
        if player['club']['name'] != '':
            teamPlayer = player['club']['name']
        

        exist = existPlayer(cursor,namePlayer)
        if exist == []:
            insert_query = "INSERT INTO api_gamer (name,game_position,nationality,team,page) VALUES ('"+str(namePlayer.replace("'"," "))+"','"+str(positionPlayer.replace("'"," "))+ "','"+str(nationalityPlayer.replace("'"," "))+"','"+str(teamPlayer.replace("'"," "))+"','"+str(page)+"')"
            cursor.execute(insert_query)
            print("player "+str(namePlayer)+" inserted successfully")
        else:
            print("player "+str(namePlayer)+" exist ")
 
    except KeyError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    try:
        saveFifaApiPlayers(sys.argv[1])

    except:
        print('default page = 54')
        saveFifaApiPlayers(54)

        
