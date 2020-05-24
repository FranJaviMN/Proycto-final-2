from flask import Flask, abort, render_template
import requests
import os
key=os.environ["clave_propia"]
#payload = {"locale=es_ES":"es_ES"}
headers={"Authorization":"bearer "+key}
URL_BASE_CARTAS = "https://us.api.blizzard.com/hearthstone/cards?locale=es_ES"
#URL_BASE_PARAMETROS = "https://us.api.blizzard.com/hearthstone/metadata/"
app=Flask(__name__)


#En esta ruta solo definimos el inicio de la pagina que se encuentra en el fichero inicio.html

@app.route('/', methods=["GET"])
def inicio():
    return render_template('inicio.html')


@app.route('/todas_cartas/<int:pagina>', methods=["GET"])
def cartas(pagina):
    peticion_todas_cartas=requests.get(URL_BASE_CARTAS+'&pageSize=21&page='+str(pagina), headers=headers)
    if peticion_todas_cartas.status_code == 200:
        doc_cartas=peticion_todas_cartas.json()
        return render_template('todas-cartas.html', doc_cartas=doc_cartas, pagina=1)
    else:
        return abort(404)

app.run('0.0.0.0', debug=True)


