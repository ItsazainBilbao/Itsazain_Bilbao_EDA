# Itsazain_Bilbao_EDA
 
## Descripción
Exploratory Data Analysis sobre Commander. Estudio sobre si las cartas publicadas recientemente tienen impacto o algún uso en el juego, comunidad y metajuego moderno.
## Estructura
### src/Data
Directorio con la base de datos en .csv (en bruto y limpia) y los mazos en .txt.
Se pueden guardar los mazos en carpetas o pro separado. Si se guardan en una carpeta se pueden luego importar en bulk todos los mazos al mismo dataframe.
### src/img
Directorio para las imágenes de los gráficos, y en caso de quererlo, de otras imágenes para los notebooks
### src/notebooks
Directorio donde están todos los Notebooks que se han empleado para pruebas y análisis
#### AnalisisCantidad.ipynb
Donde se analiza la cantidad de cartas impresas y reimpresas a lo largo de los 30 años de magic.
#### AnalisisCasosEspeciales.ipynb
Donde se estudian los casos especiales que pueden generar ruido en el análisis debido a que la mayor parte de las cartas que emplean son de colecciones específicas.
#### AnalisisEDHREC.ipynb
Donde se estudian los mazos competitivos teniendo en cuenta la popularidad de las cartas que utilizan. También se mira el color de las cartas nuevas que utilizan para ver si se descubre algún hallazgo interesante.
#### Definicion_EDA.ipynb
Donde se definió por primera vez el EDA, aunque desde entonces ha llovido un poco y se han cambiado varias cosas.
#### PreparacionDFC.ipynb
Donde se limpia, transforma y prepara la Base de Datos de cartas para luego poder añadirle columnas relevantes a los mazos y estudiarlos. Guarda la base de datos limpia en un .csv
#### PreparacionMazos.ipynb
Donde en su momento pensaba automatizar la preparación de los mazos a analizar, añadiéndole las columnas y limpiando los nulos, pero al final simplemente es para pruebas.
### Utils
Directorio donde se encuentran los .py que se han utilizado en el análisis o tratamiento de los datos.
#### api_requests.py
.py donde se hace la llamada a la API de scryfall para descargar en json toda su base de datos. Luego se transforma en un dataframe y se guarda como un .csv para gestionarlo más cómodo.
#### edhrec_requests.py
.py donde en un principio iban a hacerse requests a edhrec, pero fue imposible porque no tiene API y el data wraping no me iba. Asi que se quedó como una librería para gestionar y transformar los datos. Aquí es donde está el código que importa y procesa los .txt de los mazos para luego utilizarlos en el análisis.
#### funciones.py
.py pequeño con funciones varias que no me encajaban en el edhrec_requests.py
#### graficos.py
.py con funciones que generan gráficos. Esperaba usar más los gráficos para diferentes mazos, pero al final me he quedado con dos y he usado cada uno una vez. Eficiencia.


## 🛠 Instalación 🛠
# Clonar el repositorio
```bash
git clone https://github.com/ItsazainBilbao/Itsazain_Bilbao_EDA.git
```
# Instalar dependencias
```bash
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
```
