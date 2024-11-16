import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

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
    filename = "imagen_descargada.jpg"
    with open(filename, "wb") as file:
        file.write(img.content)
    
else:
        print(f"Error: {response.status_code}")