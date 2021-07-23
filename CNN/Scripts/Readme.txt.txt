Fichero EEGRAPH:
 - Modificación local de la librería EEGraph, para generar las imágenes de los grafos generados. Las imágenes generadas son en 	escala de grises. En la imagen las aristas tienen un grosor e intensidad de color en función del valor de la conexión.

Fichero data:
 - Datasets empleados en el estudio. Cada dataset se compone de un fichero '0' (con los EEGs de la clase 0) y otro fichero '1'(con los EEGs de la clase 1).  

 - Contiene los datasets de los dos casos de uso empleados:
	- Presalva vs Vigilia sin/con
	- Presalva vs (Espasmo, Interesp sin/con, Postsalva)

Scripts:

 * PreProcess_EEG_IMG:
    - Script para generar las imágenes de un dataset, tiene en cuenta el fichero en el que se encuentra para asignar dicha clase. 
      Separa las imagenes generadas en los mismos ficheros como el dataset original. 

      Dentro del script se debe especificar:
	- path: del dataset a emplear.
        - connectivity_measures: Medida/s de conectividad a emplear y las bandas de frecuencia (si la medida lo requiere). 
	- window_size_class_0: Tamaño de la ventana.
	- window_size_class_0: Tamaño de la ventana.

      Las imágenes se guardan en una jerarquía de ficheros que corresponde con los parametros empleados, y deben ser creado antes de ejecutar el script.

      Por ejemplo:
	- Ventana de 1 segundo.
	- Medida 'Squared_Coherence'. 
	
	Las imágenes de la clase 0 se van a guardar en IMG/1-seg/squared_coherence/0
	Las imágenes de la clase 1 se van a guardar en IMG/1-seg/squared_coherence/1 
	**Estos ficheros deben existir antes de la ejucción del script. 

 * Combine_Images:
    - Script para combinar imágenes de tres bandas de frecuencia en una única imagen de 3 canales. 

      Dento del script se debe especificar:
        - conn: La medida de conectividad empleada. (La utilizada para generar las imágenes a partir de los EEGs). 
	- window: La ventana empleada. (La utilizada para generar las imágenes a partir de los EEGs). 
	 
      Obtiene las imagenes de IMG/{window}/{conn}, las combina y las guarda en otra jerarquía de ficheros IMG_Bands/{window}/{conn}. Que también debe existir antes de la ejecución del script.  

        Por ejemplo:
	- Ventana de 1 segundo.
	- Medida 'Squared_Coherence'.

        Las imágenes de la clase 0 se obtienen de IMG/1-seg/squared_coherence/0 y se guardan en IMG_Bands/1-seg/squared_coherence/0
	Las imágenes de la clase 1 se obtienen de IMG/1-seg/squared_coherence/1 y se guardan en IMG_Bands/1-seg/squared_coherence/1

 * EEG_SNA:
    - Script que calcula las métricas estadísticas de los grafos generados, para cada clase por separado. 

       Dentro del script se debe especificar lo mismo que en PreProcess_EEG_IMG:
        - path: del dataset a emplear.
        - connectivity_measures: Medida/s de conectividad a emplear y las bandas de frecuencia (si la medida lo requiere). 
	- window_size_class_0: Tamaño de la ventana.
	- window_size_class_0: Tamaño de la ventana.