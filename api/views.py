
from collections import namedtuple
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import json
import api.models as dbFiFa
import requests as requesthttp

@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def geListPlayers(request):
    try:
        players = list(dbFiFa.gamer.objects.all())
        listPlayers = []
        for player in players:
            listPlayers.append({
                'id':player.id,
                'name':player.name,
                'game_position':player.game_position,
                'nationality': player.nationality,
                'team':player.team,
            } )

        return Response({'players':listPlayers},status=200)

    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)
@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def geTeam(request):
    try:
        teamN = request.data['name']
        page_num = request.data['page']
        teamPlay = list(dbFiFa.gamer.objects.filter(team__icontains=teamN)) # page=page_num

        teamPlayers = []
        if teamPlay != []:

            for player in teamPlay:
                teamPlayers.append({
                    'id':player.id,
                    'name':player.name,
                    'game_position':player.game_position,
                    'nationality': player.nationality,
                    'team':player.team,
                } )
            totalPages = 1
            totalItems = len(teamPlay)
            items = len(teamPlay)
            jsonRepon = {
                "name":teamN,
                "Page":page_num,
                "totalPages":totalPages,
                "Items": items,
                "totalItems":totalItems,
                "Players": teamPlayers
            }

            return Response(jsonRepon,status=200)
        else:
            return Response("The Team is not in the Database",status=305)

    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPlayers(request):
    try:
        name_player = request.data['search']
        page_p = request.data['page']
        order = request.data['order']
        listPlayers = list(dbFiFa.gamer.objects.filter(name__icontains=name_player)) # ,page=page_p

        if order == "desc":
            listPlayers = listPlayers.sort(key=lambda player: player.name,reverse=True)
    
        else:
            listPlayers =  sorted(listPlayers, key=lambda player: player.name, reverse=False)

        listPla = []
        if listPlayers != []:
            for player in listPlayers:
                listPla.append({
                    'id':player.id,
                    'name':player.name,
                    'game_position':player.game_position,
                    'nationality': player.nationality,
                    'team':player.team,
                } )

            
            print(listPlayers)
            totalPages = 1
            totalItems = len(listPlayers)
            items = len(listPlayers)
            jsonRepon = {
                "Page":page_p,
                "totalPages":totalPages,
                "Items": items,
                "totalItems":totalItems,
                "Players": listPla
            }
            return Response(jsonRepon,status=200)
        else:
            return Response("not match in the Database",status=305)

    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveFifaApiPlayers(request):
    try:
        page = request.data['page']
        request_query = requesthttp.get('https://www.easports.com/fifa/ultimate-team/api/fut/item?page='+str(page))
        if request_query.status_code == 200:
            data = json.loads(request_query.text)
            playersinfo = data['items']
            [savePlayerDB(player,page) for player in playersinfo]
            return Response("Datos Guardados Correctamente desde el Api de fifa Ultimate Team ",status=request_query.status_code)
        else:
            return Response({"Error":"status_code Api Fifa"+str(request_query.status_code)},status=request_query.status_code)
  
    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)


def savePlayerDB(player,page_api):
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
        
        exist= list(dbFiFa.gamer.objects.filter(name = namePlayer ))
        if exist == []:
            gamer = dbFiFa.gamer(
                name = namePlayer,
                nationality = nationalityPlayer,
                game_position = positionPlayer,
                team = teamPlayer,
                page = page_api
            )
            gamer.save()
    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)



