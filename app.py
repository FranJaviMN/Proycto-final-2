from flask import Flask, abort, render_template
import requests
import os
key=os.environ["clave_propia"]
#payload = {"locale=es_ES":"es_ES"}
headers={"Authorization":"bearer "+key}
URL_BASE_CARTAS = "https://us.api.blizzard.com/hearthstone/cards"
#URL_BASE_PARAMETROS = "https://us.api.blizzard.com/hearthstone/metadata/"
app=Flask(__name__)


#En esta ruta solo definimos el inicio de la pagina que se encuentra en el fichero inicio.html

@app.route('/', methods=["GET"])
def inicio():
    return render_template('inicio.html')

app.run('0.0.0.0', debug=True)


