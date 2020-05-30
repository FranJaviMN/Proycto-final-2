from flask import Flask, abort, render_template, request
import requests
import os
key=os.environ["clave_propia"]
#payload = {"locale=es_ES":"es_ES"}
headers={"Authorization":"bearer "+key}
URL_BASE_CARTAS = "https://us.api.blizzard.com/hearthstone/cards?locale=es_ES"
URL_CARTA_DETALLES = "https://us.api.blizzard.com/hearthstone/cards/"
URL_BASE_PARAMETROS = "https://us.api.blizzard.com/hearthstone/metadata?locale=es_ES"
app=Flask(__name__)


#En esta ruta solo definimos el inicio de la pagina que se encuentra en el fichero inicio.html

@app.route('/', methods=["GET"])
def inicio():
    return render_template('inicio.html')


#En est ruta vamos a ver todas la cartas disponibles en la api usada.

@app.route('/todas_cartas/<int:pagina>', methods=["GET"])
def cartas(pagina):
    peticion_todas_cartas=requests.get(URL_BASE_CARTAS+'&pageSize=21&page='+str(pagina), headers=headers)
    if peticion_todas_cartas.status_code == 200:
        doc_cartas=peticion_todas_cartas.json()
        return render_template('todas-cartas.html', doc_cartas=doc_cartas, pagina=1)
    else:
        return abort(404)

#En esta ruta vamos a poder buscar las cartas mediante la clase, la rareza y el tipo de carta.

@app.route('/buscador_cartas', methods=["GET","POST"])
def buscador():
    lista_heroes=[]
    lista_rare=[]
    lista_tipo=[]
    peticion_parametros=requests.get(URL_BASE_PARAMETROS, headers=headers)
    if peticion_parametros.status_code == 200:
        doc_parametros=peticion_parametros.json()
        for classes in doc_parametros['classes']:
            lista_heroes.append(classes)
        for rares in doc_parametros['rarities']:
            lista_rare.append(rares)
        for tipo in doc_parametros['types']:
            lista_tipo.append(tipo)
    
    if request.method == "GET":
            return render_template('buscador.html', lista_heroes=lista_heroes, lista_rare=lista_rare, lista_tipo=lista_tipo)
    else:
        palabra_buscador=request.form.get("nombre")
        clase=request.form.get("clases")
        rareza=request.form.get("rarities")
        tipo=request.form.get("tipo")
        if palabra_buscador == "":
            peticion_cartas=requests.get(URL_BASE_CARTAS+"&class="+clase+"&rarity="+rareza+"&type="+tipo, headers=headers)
            if peticion_cartas.status_code == 200:
                doc_cartas=peticion_cartas.json()
                return render_template("buscador.html", doc_cartas=doc_cartas, lista_heroes=lista_heroes, lista_rare=lista_rare, lista_tipo=lista_tipo)
        else:
            peticion_cartas=requests.get(URL_BASE_CARTAS+"&class="+clase+"&rarity="+rareza+"&type="+tipo+"&textFilter="+palabra_buscador, headers=headers)
            if peticion_cartas.status_code == 200:
                doc_cartas=peticion_cartas.json()
                return render_template("buscador.html", doc_cartas=doc_cartas, lista_heroes=lista_heroes, lista_rare=lista_rare, lista_tipo=lista_tipo)


#Con esta ruta vamos a ver los detalles de la cartas.


@app.route('/detalles/<idcarta>', methods=["GET"])
def detalles(idcarta):
    peticion_detalles=requests.get(URL_CARTA_DETALLES+idcarta+'?locale=es_ES', headers=headers)
    peticion_parametros=requests.get(URL_BASE_PARAMETROS, headers=headers)
    if peticion_detalles.status_code == 200 and peticion_detalles.status_code == 200:
        doc_detalle=peticion_detalles.json()
        doc_parametros=peticion_parametros.json()
        return render_template('detalles.html', doc_detalles=doc_detalle, doc_parametros=doc_parametros)
    else:
        return abort(404)



#Activar cuando ya no se este en desarrollo.

port=os.environ["PORT"]

app.run('0.0.0.0', int(port), debug=False)

#Activar cuando aun se esta en desarrollo

#app.run('0.0.0.0', debug=True)


