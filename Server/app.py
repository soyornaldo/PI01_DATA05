from flask import Flask, request, Response
import sqlite3
import pandas as pd
import numpy as np
import json 


path = 'C:\\Users\\ornal\\Desktop\\CursoDataScience\\PI01_DATA05\\CaptaDatos\\audiovisuales.db'
csvFileName = "./Salida.csv"



app = Flask(__name__)



'''
    HOME
'''
@app.route('/')
def index():
  return '''<!DOCTYPE html>
<html>
    <head>       
        <meta charset="utf-8">
        <title>Ejemplo del uso de listas - aprenderaprogramar.com</title>
    </head>
    <body>
<ul>

 <li type="circle">Máxima duración según tipo de film (película/serie), por plataforma y por año. (<a href="http://localhost:5001/json/max_duration"> JSON </a>,<a href="http://localhost:5001/csv/max_duration"> CSV </a>)</li>

 <li type="circle">Cantidad de películas y series (separado) por plataforma. (<a href="http://localhost:5001/json/count_plataform"> JSON </a>,<a href="http://localhost:5001/csv/count_plataform"> CSV </a>)</li>

 <li type="circle">Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. (<a href="http://localhost:5001/json/listedin"> JSON </a>,<a href="http://localhost:5001/csv/listedin"> CSV </a>)</li>


 <li type="circle">Actor que más se repite según plataforma y año. (<a href="http://localhost:5001/json/actor"> JSON </a>,<a href="http://localhost:5001/csv/actor"> CSV </a>)</li>



</ul>

</body>
</html>  
  '''





'''
    Cantidad de películas y series (separado) por plataforma
    El request debe ser: get_count_plataform(plataforma)
'''
@app.route('/json/count_plataform', methods=['GET'])
def get_count_plataform_json():
 
  con = sqlite3.connect(path)

  consulta = "select * from cant_plataforma_tipo"
  ya = False

  plataforma = request.args.get('plataforma')
  type = request.args.get('type')
  

  if plataforma != None or type != None:
    consulta = consulta + " where "
    
  if plataforma != None:  
    consulta = consulta + " plataforma = '"+str(plataforma)+"'" 
    ya = True

  if type != None:
    if ya:
      consulta = consulta + " and type = '"+str(type)+"'" 
    else:  
      consulta = consulta + " type = '"+str(type)+"'"  

  
  df = pd.read_sql(consulta, con)

  con.close()

  result = df.to_json(orient="columns") 
  parsed = json.loads(result)
  
  lista = json.dumps(parsed)      
  return '{'+lista[1:len(lista)-1]+'}' 



@app.route('/csv/count_plataform', methods=['GET'])
def get_count_plataform_csv():
 
  con = sqlite3.connect(path)

  df_cant_plataforma = pd.read_sql("select * from cant_plataforma_tipo", con)

  con.close()

  csv = df_cant_plataforma.to_csv() 

  return Response(csv,mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=cantidad_peliculas_y_series.csv"})




'''
    Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    El request debe ser: get_listedin('genero')  
    Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.
''' 
@app.route('/json/listedin', methods=['GET'])
def get_listedin_json():
 
  con = sqlite3.connect(path)

  consulta = "select * from cant_genero_plataforma"
  ya = False

  nombre_genero = request.args.get('nombre_genero') 
  plataforma    = request.args.get('plataforma')

  if plataforma != None or nombre_genero != None:
    consulta = consulta + " where "
    
  if plataforma != None:  
    consulta = consulta + " plataforma = '"+str(plataforma)+"'" 
    ya = True

  if nombre_genero != None:
    if ya:
      consulta = consulta + " and nombre_genero = '"+str(nombre_genero)+"'" 
    else:  
      consulta = consulta + " nombre_genero = '"+str(nombre_genero)+"'"  

  
  df = pd.read_sql(consulta, con)

  con.close()

  result = df.to_json(orient="columns") 
  parsed = json.loads(result)
  
  lista = json.dumps(parsed)      
  return '{'+lista[1:len(lista)-1]+'}' 



@app.route('/csv/listedin', methods=['GET'])
def get_listedin_csv():
 
  con = sqlite3.connect(path)

  df = pd.read_sql("select * from cant_genero_plataforma", con)

  con.close()

  csv = df.to_csv() 

  return Response(csv,mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=frecuencia_genero_y_plataforma.csv"})







'''
    Máxima duración según tipo de film (película/serie), por plataforma y por año:
    El request debe ser: get_max_duration(año, plataforma, [min o season])
'''
@app.route('/json/max_duration', methods=['GET'])
def get_max_duration_json():
 
  con = sqlite3.connect(path)

  consulta = "select * from movie_max_duracion"
  ya = False

  plataforma = request.args.get('plataforma')
  release_year = request.args.get('release_year')
  duracion = request.args.get('duracion') 

  if plataforma != None or release_year != None or duracion != None:
    consulta = consulta + " where "
    
  if plataforma != None:  
    consulta = consulta + " plataforma = '"+str(plataforma)+"'" 
    ya = True

  if release_year != None:
    if ya:
      consulta = consulta + " and release_year = "+str(release_year)
    else:  
      consulta = consulta + " release_year = "+str(release_year) 
    ya = True 

  if duracion != None:
    if ya:
      consulta = consulta + " and duracion = "+str(duracion)
    else:  
      consulta = consulta + " duracion = "+str(duracion)
  
  df_cant_plataforma = pd.read_sql(consulta, con)

  con.close()

  result = df_cant_plataforma.to_json(orient="columns") 
  parsed = json.loads(result)
  
  lista = json.dumps(parsed)      
  return '{'+lista[1:len(lista)-1]+'}' 



@app.route('/csv/max_duration', methods=['GET'])
def get_max_duration_csv():
 
  con = sqlite3.connect(path)

  df = pd.read_sql("select * from movie_max_duracion", con)

  con.close()

  csv = df.to_csv() 

  return Response(csv,mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=max_duracion.csv"})



'''
   Actor que más se repite según plataforma y año.
   El request debe ser: get_actor(plataforma, año)
'''
@app.route('/json/actor', methods=['GET'])
def get_actor_json():
 
  con = sqlite3.connect(path)

  consulta = "select * from actor_mas_repite"
  ya = False

  plataforma = request.args.get('plataforma')
  release_year = request.args.get('release_year')

  if plataforma != None or release_year != None:
    consulta = consulta + " where "
    
  if plataforma != None:  
    consulta = consulta + " plataforma = '"+str(plataforma)+"'" 
    ya = True

  if release_year != None:
    if ya:
      consulta = consulta + " and release_year = "+str(release_year)
    else:  
      consulta = consulta + " release_year = "+str(release_year) 
    ya = True 

  
  df = pd.read_sql(consulta, con)
  df = df.groupby(['plataforma','release_year']).first()

  con.close()

  result = df.to_json(orient="columns") 
  parsed = json.loads(result)
  
  lista = json.dumps(parsed)      
  return '{'+lista[1:len(lista)-1]+'}' 



@app.route('/csv/actor', methods=['GET'])
def get_actor_csv():
 
  con = sqlite3.connect(path)

  df = pd.read_sql("select * from actor_mas_repite", con)
  df = df.groupby(['plataforma','release_year']).first()

  con.close()

  csv = df.to_csv() 

  return Response(csv,mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=actor_mas_repite.csv"})



if __name__ == "__main__":
  #app.run(debug=True)
  app.run(host='localhost', port=5001, debug=True)
