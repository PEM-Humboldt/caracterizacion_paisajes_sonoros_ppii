# Análisis de grabaciones pasivas - ANH PPII

Este repositorio tiene por objetivo describir el flujo de análisis de grabaciones pasivas, y
contiene todos los scripts usados para dicha tarea para que este análisis sea replicable.

## Prerequisitos
Los análisis fueron programados en lenguajes de programación de software libre: Python (v3.7) y R (v3.6.1).
A continuación se detallan las librerías usadas en cada uno de estos lenguajes:

- Python: scikit-maad (v1.3), scikit-learn (v0.24.1), pandas (v1.2.4), numpy (v1.19.2)
- R: seewave (v2.1.6), tuneR (1.3.3)

## Archivos requeridos
Las grabaciones pasivas objeto de este estudio están almacenadas en la Colección de Sonidos Ambientales del Instituto Humboldt.

## 1. Preprocesamiento

### 1.1. Agragar prefijos a los nombres de los archivos
Las grabaciones realizadas con Audiomoth dejan marcas temporales en el nombre del archivo,
pero no tienen ningún prefijo que permita saber a qué sensor corresponde. Para facilitar esta identificación y evitar errores se agregó el nombre de las grabadoras al principio del archivo usando `bash` 
y la siguiente línea de comando:

```bash
for i in *.WAV; do mv {,G001_}$i; done # G001 se remplaza con el nombre correspondiente
```

### 1.2. Extraer metadatos
Se automatizó la extracción de metadatos fundamentales de cada archivo de audio usando R.
El script [audio_metadata_utilities.R](aguas_altas/preprocessing/audio_metadata_utilities.R) contiene las funciones
necesarias y [read_audio_metadata.R](aguas_altas/preprocessing/read_audio_metadata.R) presenta el paso a paso para
automatizar el proceso en todas las grabaciones. **Los archivos deben estar organizados 
teniendo un durectorio por cada unidad de muestreo**.

### 1.3. Visión de conjunto e inspección manual
Para asegurarnos de tener información válida en etapas siguentes del análisis es improtante
tener una visión de conjunto y realizar una inspección manual. Se tomó una muestra de 
5 segundos por cada grabación durante 5 días. Así se verificó que los micrófonos estaban
funcionando correctamente y se identificaron los principales patrones en los datos.

Se usaron los scripts de Python:
- [sample_acoustic_monitoring.py](aguas_altas/preprocessing/sample_acoustic_monitoring.py)
- [audio_to_spectro_image.py](aguas_altas/preprocessing/audio_to_spectro_image.py)

Se encontraron grabadoras con un desfase en sus archivos. La hora se corrigió en el 
nombre del archivo con el script [rename_files_time_delay.py](aguas_altas/preprocessing/rename_files_time_delay.py).

## 2. Caracterización de comunidad acústica
Para evidenciar los principales patrones de diversidad de la comunidad acústica, evaluamos características en tiempo y frecuencia a través de la huella acústica y calculamos múltiples índices acústicos. La huella acústica se calculó usando el paquete Seewave (v2.1.6) de R (v3.6.1) y los índices acústicos fueron calculados usando el paquete scikit-maad (v1.3) en Python (v3.7). Estos scripts se encuentran en la carpeta [acoustic_community_characterization](aguas_altas/acoustic_community_characterization).

## Autores y contacto
Estos análisis fueron desarrollados por Juan Sebastián Ulloa (julloa@humboldt.org.co), investigador del PRograma de Evaluación y Monitoreo de la Biodiversidad del Intituto Humboldt.

## Licencia
Este desarrollo es de fuente libre y está acompañado de una licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
