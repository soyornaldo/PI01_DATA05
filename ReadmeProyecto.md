Para resolver la tarea asignada prepare carpetas:
CaptaDatos - Aqui va a estar todo lo relacionado con cargar los datos desde los origenes y al final lo pasaria todo a una 
             Base de Datos en SQLite, las apis que me piden las voy a tener en unas vistas
Server - Es donde voy a crear el Servidor que permitira realizar las consultas api a la base de datos


Procedimiento empleado:
- Use un fichero jupyter notebook para cargar, transformar, y crear los dataframes que se convertiran en tablas sqlite.

- Cargue en DataFrames las cuatro tablas (3 csv, 1 json) que contiene la informacion originaria.

- Junte los 4 DataFrames en uno solo

- Salvo todos los DataFrames en una BD SQLite 'origen_audiovisual.db'
Usando SQLiteStudio
Es mas comodo revisar visualmente las tablas usando los grids 

- Revise las info de las tablas para ver los nulos donde estan

- Aqui voy de SQLite a Jupyter y viceversa revisando y cambiando

- Hago una copia de los DataFrames originales y ya desecho los campos que asumo no me hacen falta de acuerdo a lo que me estan pidiendo

- Primero tengo que separar el valor entero de la descripcion en la columna duration y dejar solo el entero

- Ejecuto una funcion en todos los DataFrames y ya tengo la columna duration con numeros

- Despues de analizar los nulos en cast, existe como sacar algunos porque existen titles repetidos que en un caso tiene cast y en otro no. De momento todos los nulos se va con la etiqueta N/A

- Creo el DataFrame df_plataforma (Clasificador)

- Agrego una columna a cada tabla y le pongo el valor que le corresponde en la tabla df_plataforma, para poder juntarlas en una sola tabla

- Creo un dataframe unico concatenando los 4 dataframes que me entran. Este va a dar origen a la tabla principal que se va a llamar 'audiovisual'

- Preparo los Clasificadores de 'genero' y 'artista'
  Para hacer esto recorri la tabla principal y le extraje a los campos listed_in (genero) y cast (artistas) la informacion para ponerla en ua lista que me sirva para crear los dataframes.

- Preparo las tablas puentes para relacionar a 'audiovisual' con 'genero' y 'artista'.
  Las tablas nuevas se van a llamar 'genero_audio' y 'artista_audio'  
  Para esto voy a realizar el mismo procedimiento del pado anterior y por ej:
    Estoy recorriendo 'audiovisual' y dentro de ese recorrido estoy recorriendo la lista de artistas que se origina de 'cast' y para cada artista busco en el clasificador 'artista' y formo el diccionario con el id del audiovisual y el id del artista.

- Envio todo a la base de datos en SQLite

- Al exportar todas las tablas a SQLite para empezar a ser usada como fuente del Servidor api
me quedaba pendiente rellenar la columna duration que al principio habia puesto 0 en los nulos.
Realice esta consulta:

   SELECT DISTINCT TYPE
   FROM   AUDIOVISUAL
   WHERE  DURATION = 0

El resultado dio que solo habia nulos en el type = 'Movie' y entonces decidi usar el promedio de todos los
type = 'Movie' como fuente para suplir los nulos

   UPDATE AUDIOVISUAL
   SET    DURATION = (
                       SELECT CAST(AVG(DURATION) AS INT)
                       FROM   AUDIOVISUAL
                       WHERE  TYPE = 'Movie' AND DURATION > 0
                     )
   WHERE  DURATION = 0

   Como ya sabia que solo habia nulos en 'Movie'  no hacia falta agregar esa condicion al WHERE del UPDATE

- Creo las cuatro vista que responden a las preguntas. 

- Use flask para hacer el Servidor api.

- Dentro de la aplicacion servidora defino los caminos y levanto el Servidor en localhost:5001, para facilitar la experiencia puse una lista con las preguntas que me hicieron y un acceso JSON o CSV para que el usuario haga click en cualquiera de los dos. Eso se cumple para las cuatro preguntas.
Si se hace click en JSON se ejecutara la la consulta a la BD y se presentara en pantalla el resultado, una vez alli se puede filtrar por los parametros que pidieron, si se hace clic en CSV se ejecuta la consulta y se descarga el fichero.



Nota: No pude hacer el docker. Yo vivo en Cuba y se me esta negado el acceso a esa plataforma. Yo generalmente resulvo con el uso de VPN, pero en el caso de linux el cual vi por primera vez aqui en el curso he pasado mucho trabajo, por ejemplo yo uso proton VPN y en windows me trabaj perfecto, en linux al principio en el M4 me trabajo bien, de hecho pude instalar hadoo, docker y lo probe con el hello world, al dia siguiente se acabo. En el M4 siempre estuve detras una o dos clases del grupo pase de ubuntu en todas sus versiones desde la 18 a la 22 y al final estoy en linux mint y mas de lo mismo, de hecho siempre termino con que no puedo usar internet (mi internet es conectando mi telefono por wifi con las dos laptos, yo no tengo intenert en mi casa) y ahi empieza de nuevo el proceso de reinstalar todo desde el principio. Alguien de mi grupo me hablo de docker desktop en windows, tratare de probar entre el Viernes y el Domingo a ver si me sale.