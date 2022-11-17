from fastapi import FastAPI
from shodan import Shodan
import pdb, uvicorn, validators


app = FastAPI()

@app.get("/")                                       # Correspond à la racine du prjet
async def read_root():
    return "Rien à voir ici pour le moment, revenez vite"

@app.get("/iplogger/{ip}")                          # Correspond à l'url localhost:5000/iplogger/{ip}
async def read_iplogger(ip: str, apikey: str):
    
    if not validators.ipv4(ip):             # Si l'ip n'est pas valide alors on retourne une erreur
        return {"Erreur ": "IP invalide"}
    else:
        if not validators.length(apikey, min=32, max=32):   # Si la clé d'api n'est pas de la bonne taille on retourne une erreur
            return {"Erreur ": "Api invalide"}
        else:
            try:
                api = Shodan(apikey)                    # On appelle l'api Shodan
                result = api.host(ip)                   # On demande à l'api Shodan de récupérer les informations sur l'IP demandé
                return {
                    "latitude": result["latitude"],     # Latitude
                    "longitude": result["longitude"],   # Longitude
                }
            except Exception as e:                      # Si une erreur se produit on affiche l'erreur dans un format dictionnaire {key : value}
                return {"Erreur ": str(e)}


    
if __name__ == "__main__":
    uvicorn.run("serv:app", host="localhost", port=5000, log_level="info")  # On définit que le serveur uvicorn doit se lancer sur localhost et sur le port 5000
        