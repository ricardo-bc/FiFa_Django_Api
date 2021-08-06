# FiFa_Django_Api

Para este proyecto backend
#Base de datos
se utilizo una base de datos Postgres alojada remotamente con google Cloud, los detalles de la conexion esta en la carpeta config y en el archivo configApi.json

# 1 punto
 el Script esta en la carpeta rais del proyecto y se llama scrptSaveDB_part_1.py tambien se creo un endpoint en el api rest que hace lo mismo en el postman collection se llama Save_db_fifa_api_players
 
 # 2 Api rest
 se creo el api con django api rest framework
 tambien cree una colecion en postman que tiene los end points y algunos extra como de autentificacion via token y lista de jugadores
 solo tocaria agregarle el hanbiente {{url}} o reamplazarlo con la url
 en los puntos solicitados cumple con el nombre de los endpoints.
 
# Dockers
se creo el dockerfile y el docker-compose para el despliege sencillo de la aplicacion
 en la carpeta rais donde esta estos dos archivos 
 tambien se creo dockers para el front.
 comando docker-compose up --build
 
