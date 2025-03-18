from pymongo import MongoClient

#base de datos local#
#db_client = MongoClient().local #si esta vacio la url es en el local host

#base de datos en servidor internacional o remota#
db_client = MongoClient(
    "mongodb+srv://eddy:rock@impresionbd.9wxjz.mongodb.net/?retryWrites=true&w=majority&appName=ImpresionBD"
    ).impresionBD

