from fastapi import FastAPI, status, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from db.models.user import User
from db.schemas.user import user_schema, users_all_schemas
from db.client import db_client
from bson import ObjectId #para importar un objeto con la estructura id del JSon


app = FastAPI()

#Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes (cambia esto en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


#inicia el server: uvicorn main:app --reload
#salir del server: Ctrl + C

#url local: http://127.0.0.1:8000

@app.head("/")
async def root_head():
    # Personalizar los encabezados
    headers = {"X-Custom-Header": "Valor personalizado"}
    return Response(headers=headers)

@app.get("/mongo_clientes", response_model=list[User]) #quiero una lista de todos los usuarios
async def users():
    return users_all_schemas(db_client.users.find())

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/mongodb/{id}")
async def user(id: str):
    
    return search_user("_id", ObjectId(id))  # para que id tenga la estructura correcta 

#prueba con codigo (FUNCIONA)
@app.get("/mongo_codigo/{codigo}")
async def user(codigo: str):
    
    return search_user("codigo", codigo)

#prueba con codigo y nombre (FUNCIONA)
@app.get("/mongo_nombre_codigo/{nombre}&{codigo}")
async def user(codigo: str, nombre: str):
    if type(search_user("nombre", nombre)) == User:
        return search_user("codigo", codigo)    

    
@app.post("/mongodb", response_model= User, status_code=status.HTTP_201_CREATED)  
async def user(user: User):
   
   #if type(search_user("nombre", user.nombre)) == User:   
    #    raise HTTPException(status_code=404, detail="El nombre ya existe")
   if type(search_user("codigo", user.codigo)) == User:   
        raise HTTPException(status_code=404, detail="El codigo ya existe") 
        
   user_dict = dict(user)  #convertir user en tipo dict que es tipo JSON
   del user_dict["id"]  #borrar el campo Id, solo inserta el username y el email
   id = db_client.users.insert_one(user_dict).inserted_id   #insertar usuario
   new_user = user_schema(db_client.users.find_one({"_id":id})) #buscar usuario
   return  User(**new_user)              


@app.put("/actualizar_mongo", response_model= User) 
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
       db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id)) 
    

@app.delete("/delete/{codigo}")
async def user(codigo: str):

    found = db_client.users.find_one_and_delete({"codigo": codigo})
     
    if not found:
        return {"No se encontro el usuario"}
    else:
        return {"Se borro el usuario"}
   
    

    

def search_user_email(email: str):
     
    try:                                                      
        user = user_schema (db_client.users.find_one({"email": email})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user_username(username: str):
     
    try:                                                      
        user = user_schema (db_client.users.find_one({"username": username})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user(field: str , key): #buscador generico
     
    try:                                                      
        user = user_schema (db_client.users.find_one({field : key})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}
