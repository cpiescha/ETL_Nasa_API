import requests
import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI_CLOUD = os.getenv("MONGO_URI2")  # DATOS PARA ACCEDER A MONGO ATLAS CLOUD
DB_NAME_CLOUD = "etlprocess"             
COLLECTION_NAME_CLOUD= "nasa"         

MONGO_URI_LOCAL = "mongodb://localhost:27017" # DATOS PARA ACCEDER A MONGO COMPASS LOCAL
DB_NAME_LOCAL = "etlprocess"             
COLLECTION_NAME_LOCAL = "colleccion1"         


# Conectar a MongoDB CLOUD
client1 = MongoClient(MONGO_URI_CLOUD)
db1 = client1[DB_NAME_CLOUD]
collection1 = db1[COLLECTION_NAME_CLOUD]

# Conectar a MongoDB LOCAL
client2 = MongoClient(MONGO_URI_LOCAL)
db2 = client2[DB_NAME_LOCAL]
collection2 = db1[COLLECTION_NAME_LOCAL]

lat=6.25184
lon=-75.56359
API_key = os.getenv('NASA_API_KEY')
Movie_API_key=os.getenv('MOVIE_API_KEY')
url=f'https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date=2024-01-25&dim=0.25&api_key={API_key}' #url para descargar fotos de la tierra
url2=f'https://api.nasa.gov/planetary/apod?api_key={API_key}' #url para obtener imagen del dia de la nasa
url3 = f'https://api.themoviedb.org/3/movie/157336?api_key={Movie_API_key}'
response= requests.get(url2)
    # Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Convertir la respuesta en formato JSON
    response=response.text
    response=json.loads(response)
    print(response)
    img = requests.get(response['url'])
    filename = "C:/Users/USUARIO/Desktop/ETL_Nasa_API/img/imagen.jpg"
    archivo_json = "C:/Users/USUARIO/Desktop/ETL_Nasa_API/tmp/data.json"
    with open(filename, "wb") as file:
        file.write(img.content)
    if not os.path.exists(archivo_json):
        with open(archivo_json, "w", encoding="utf-8") as archivo:
            json.dump({"items": []}, archivo, indent=4, ensure_ascii=False)

# Leer el archivo JSON existente
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

# Agregar el nuevo objeto a la lista "items"
    datos["items"].append(response)

# Escribir los datos actualizados en el archivo JSON
    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print(f"Nuevo objeto agregado al archivo {archivo_json}")
    

    if response:
        result = collection1.insert_one(response)
        result2 = collection2.insert_one(response)# Inserta un solo documento en cloud
        print(f"Nuevo documento insertado en cloud con ID: {result.inserted_id}")
        print(f"Nuevo documento insertado de forma local con ID: {result2.inserted_id}")
    else:
        print("El archivo JSON no contiene datos válidos.")

    # Cerrar la conexión
    client1.close()
    client2.close()  
else:
        print(f"Error: {response.status_code}")