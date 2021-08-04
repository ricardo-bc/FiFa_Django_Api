
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

# Create your views here.

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def geTeam(request):
    try:
        name = request.data['name']
        page = request.data['page']
        return None
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
        return None
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
            [savePlayerDB(player) for player in playersinfo]
            return Response("Datos Guardados Correctamente desde el Api de fifa Ultimate Team ",status=request_query.status_code)
        else:
            return Response({"Error":"status_code Api Fifa"+str(request_query.status_code)},status=request_query.status_code)
  
    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)


def savePlayerDB(player):
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
        

        gamer = dbFiFa.gamer(
            name = namePlayer,
            nationality = nationalityPlayer,
            game_position = positionPlayer,
            team = teamPlayer
        )
        gamer.save()
    except KeyError as e:
        print(e)
        return Response({"Error": str(e)},status=446)
    except Exception as e:
        print(e)



