# Nibble Box Tracking — estado AS IS (noviembre 2026)

Este documento recoge **lo que existe**, tal cual estaba al pararse el proyecto en 2021. Une lo que hay
en este repositorio con lo que solo quedó en Google Drive. No propone rediseño. Los juicios
técnicos van aparte, en la sección 8. Sirve de punto de partida para decidir cómo retomarlo.

- Fecha del levantamiento: 2026-11-12.
- Fuentes:
  - Este repositorio: `main` en `dd936ee` y sus ramas.
  - La carpeta de Drive `nibble_box_tracking`, de la cuenta de Newral.
  - La carpeta de Drive `Newral`, de la cuenta UCM de Mario.
- Leyenda: **[V]** comprobado en ficheros o metadatos · **[I]** inferido, sin comprobar.

---

## 1. Resumen

- **Qué es.** Una prueba de concepto de visión artificial de Newral para Nibble Automation: detectar
  y seguir cajas (paquetes) que pasan por una instalación. El README habla de cajas, cubos y
  bandejas, pero **solo se llegó a una clase, `package`** [V].
- **Cuándo.** Entre el 13-03-2021 y el 15-05-2021. En git solo hay trabajo hasta el 17-04-2021.
  Todo lo de abril y mayo posterior a esa fecha está **únicamente en Drive** [V].
- **Hasta dónde llegó.**
  - Hay un dataset propio anotado: unas 1.000 imágenes de 640×360 sacadas de vídeos de stock de Getty.
  - Hay dos detectores entrenados con la Object Detection API de TensorFlow 2: CenterNet ResNet101 y
    SSD MobileNet v2 FPNLite 320.
  - La detección en tiempo real con webcam funcionó en PC con el SSD [V].
  - Se empezó un tracking por IoU que **no se terminó** [V].
  - El despliegue en Raspberry Pi se preparó (se compró el hardware, se probó streaming y se intentó
    convertir a TFLite) pero **no consta que funcionara** [I].
- **Datos y modelos.** Se conservan en Drive, no en git (sección 5). Este repo solo los enlaza.
- **Código que solo estaba en Drive.** Se ha copiado a [`drive_snapshot/`](../drive_snapshot/README.md)
  sin tocarlo, salvo una excepción: se han quitado las imágenes de las salidas de dos notebooks.

## 2. Contexto

- **Newral.** Startup de analítica e IA creada a finales de 2020. De sus socios, aparecen en el historial
  de git Beñat San Sebastián y Mario (`Mepoide`).
- **Nibble.** Empresa de automatización industrial: logística, almacenes automáticos y transporte de
  equipajes.
- **Joint venture Newral–Nibble.** En Drive hay un borrador de anuncio del 14-03-2021
  (`Newral/docs/borrador_newral_nibble_joint_venture.rtf`) con su infografía en
  `Newral/infographies/`. Enumera estos casos de uso:
  1. Visualización y dashboard de procesos y eventos en las instalaciones.
  2. Procesamiento eficiente de datos en cualquier tipo de sistema de transporte.
  3. Modelos predictivos para mejorar el rendimiento de la instalación.
  4. Implantación de elementos con inteligencia artificial en las instalaciones.

  **Box tracking es el único que se desarrolló**, y encaja en el punto 4. De los otros tres no hay
  rastro [V].
- **Presentación de casos de uso para Nibble.** No se ha encontrado en ninguna de las dos carpetas ni
  en el resto del Drive accesible. Puede que sea un pptx local o que esté en otra cuenta.
- **Hardware.** El 03-04-2021 se compraron una Raspberry Pi Zero y un módulo de cámara [V].

## 3. Cronología

| Fecha (2021) | Hito | Dónde |
|---|---|---|
| 13-03 | Primer commit: notebooks de few-shot (eager) de los tutoriales de TF | git |
| 14-03 | Borrador de la joint venture e infografía | Drive `Newral/` |
| 16-03 | Descarga de vídeos de Getty y 4 vídeos propios grabados con móvil (WhatsApp) | Drive `data/raw/videos` |
| 19–24-03 | Extracción de fotogramas y anotación con labelme (`getty_ann`) | Drive `data/` |
| 22-03 | Modelo few-shot inicial (`initial_model/model.tflite`) | Drive `models/` |
| 25-03 | TFRecords y entrenamiento de CenterNet ResNet101 (ckpt-1 a ckpt-3) | Drive `object_detection_API/` |
| 27–30-03 | Entrenamiento y exportación de SSD MobileNet v2 FPNLite 320; zips de los dos modelos | Drive `models/` |
| 03-04 | Compra de la Raspberry Pi Zero y la cámara | — |
| 05-04 | Reorganización del repo (PR #1, rama `reorganize`) y creación de la carpeta compartida de Drive | git / Drive |
| 11–17-04 | Código de la API, `path_annotation.py` y primer `08_box_tracking`. **Último commit (17-04)** | git |
| 24-04 | Rama `deploy_to_rpi` creada sin commits; carpeta `rpi_issues/` vacía; `pipeline_v_mep.config` | git / Drive |
| 01–03-05 | Modelos de TF1 cuantizados (SSD MobileNet v1/v3) y conversión a TFLite: `detect.tflite` (6,9 MB) y `package_detect.tflite` (**696 bytes: conversión fallida** [I]) | Drive `Newral/tf_models`, `tf_lite_models` |
| 04–09-05 | `tf_webcam_detection`: detección en tiempo real con webcam (TF y TFLite); grabación `outputff.avi` | Drive `Newral/repos/` |
| 10-05 | `pipeline_v_mep_rpi.config` | Drive |
| 15-05 | `08_box_tracking.ipynb` pasa al SSD y añade un tracking naive por IoU; repos de streaming de vídeo de la Raspberry Pi al PC | Drive |
| 27-09 | Sincronización de la copia local de Beñat a Drive con FreeFileSync. No hay actividad posterior | Drive |

## 4. Pipeline y estado por fase

| # | Fase | Estado | Evidencia |
|---|---|---|---|
| 0 | Obtención de vídeo | ✅ 29 vídeos de stock de Getty y 4 propios | Drive `data/raw/videos` |
| 1 | Extracción de fotogramas | ✅ Manual, fotograma a fotograma con OpenCV | `notebooks/00_capture_frames_from_video.ipynb` |
| 2 | Anotación | ✅ labelme 4.5.7, rectángulos, clase `package`, imagen incrustada en el JSON | Drive `data/processed/getty_ann` |
| 3 | Reparto entrenamiento/validación | ✅ Por vídeo: 4 de 12 vídeos a validación, el 34 % de los fotogramas | `notebooks/05_test_train_split.ipynb` |
| 4 | Conversión a TFRecord | ✅ `training.tfrecord` y `val.tfrecord` | `object_detection_API/src/labelme_json_to_tfrecord.py`; Drive |
| 5a | Entrenamiento de CenterNet ResNet101 FPN 512 | ✅ Entrenado. ⚠️ Solo carga en la máquina con la que se entrenó (ver 8.2) | Drive `object_detection_API/models/box_centernet_resnet101_v1_fpn_512` |
| 5b | Entrenamiento de SSD MobileNet v2 FPNLite 320 | ✅ Entrenado y exportado. Es el que acabó usándose | Drive `models/package_ssd_mobilenet_v2_fpnlite_320.zip` |
| 6 | Evaluación | ❌ No hay métricas guardadas (mAP o similar). Solo inspección visual | — |
| 7 | Detección en tiempo real en PC | ✅ Webcam y SSD con la API de TF; vídeo grabado | `drive_snapshot/newral_drive/repos/tf_webcam_detection`; Drive `outputff.avi` |
| 8 | Tracking | 🧪 Empezado: función `iou()`, filtro de detecciones (score > 0,5 y caja menor de 2/3 del fotograma) e IDs de visualización fijos `[0,1,2,3]`. **No hay bucle de asociación entre fotogramas** | `drive_snapshot/nibble_box_tracking_drive/notebooks/08_box_tracking.ipynb` |
| 8b | Trayectoria esperada | 🧪 Herramienta para dibujar los segmentos por los que debería pasar el centro de la caja; guarda un JSON que nada consume todavía | `src/path_annotation.py` |
| 9 | Conversión a TFLite | ⚠️ Intentada; un resultado de 696 bytes indica que falló [I] | Drive `Newral/tf_models`, `tf_lite_models` |
| 10 | Despliegue en Raspberry Pi | 📋 Solo preparación: streaming de la Raspberry Pi al PC, config `_rpi` y rama vacía | `drive_snapshot/newral_drive/repos/live_video_stream_rpi_over_network` |

## 5. Dónde está cada cosa

### 5.1 Repositorio (este)

| Ruta | Qué es |
|---|---|
| `notebooks/00`–`08` | Exploración, preparación de datos, few-shot, pruebas de inferencia y tracking (versión del 17-04) |
| `object_detection_API/` | Scripts de la API de TF (`model_main_tf2.py`, `exporter_main_v2.py` copiados del repo de TF), `labelmap.pbtxt`, conversión de labelme a TFRecord |
| `src/path_annotation.py` | Herramienta para anotar la trayectoria esperada |
| `drive_snapshot/` | **Nuevo:** código y configs que solo existían en Drive (ver su README) |
| `docs/AS-IS.md` | Este documento |

**Ramas:**
- `main` (`dd936ee`).
- `reorganize`: fusionada en el PR #1.
- `deploy_to_rpi`: igual que `main`, nunca recibió commits.

El `.git` sincronizado en Drive confirma que **no hay commits sin subir** [V].

### 5.2 Drive: carpeta `nibble_box_tracking` (cuenta de Newral)

Enlace: <https://drive.google.com/drive/folders/1W3u_tG37JJ8l-9gbEM6kxvqJUElujgag> (acceso restringido).

En la misma carpeta hay **dos árboles mezclados**:
- **A:** subida original de la cuenta de Newral, del 05-04-2021. Contiene los datos y modelos pesados.
- **B:** sincronización FreeFileSync de la copia local de Beñat, del 27-09-2021. Contiene el código,
  los notebooks y el `.git`. Le faltan los ficheros de más de unos 5,5 MB [I].

`object_detection_API/` es una sola carpeta en la que se mezclan los dos árboles.

| Recurso | Ubicación en Drive | Notas |
|---|---|---|
| Vídeos originales | `data/raw/videos/{getty, getty/boxes, getty_tracking, WhatsApp…}` | 29 de Getty (unos 86 MB) y 4 propios. `getty_tracking` = vídeo 162812919 |
| Fotogramas sin anotar | `data/raw/images/{getty/mix, getty/boxes/full, getty_tracking, WhatsApp…}` | `getty_tracking`: todos los fotogramas de 162812919 |
| Anotaciones labelme | `data/processed/getty_ann/boxes/{train,val,full}`, `object_detection_API/images/{train_json,val_json}` | `full` = 1.059 imágenes de 17 vídeos. Los recuentos de train/val son mínimos (≥), porque la paginación del conector no llegó al final |
| Dataset externo | `data/processed/Packages.v5-augmented-v1.coco` | Dataset público de Roboflow "Packages" (COCO) |
| TFRecords | `object_detection_API/images/{training,val}.tfrecord` | 13,2 MB y 9,6 MB |
| CenterNet entrenado | `object_detection_API/models/box_centernet_resnet101_v1_fpn_512/` (ckpt-1 a ckpt-3, unos 887 MB) | Solo completo en A. También en `models/package_centernet_resnet.zip` (331 MB) |
| SSD exportado | `models/package_ssd_mobilenet_v2_fpnlite_320.zip` (20 MB) | Las carpetas `exported-models/` sueltas están incompletas: faltan `.data` y `saved_model.pb` |
| Modelo few-shot | `models/initial_model/model.tflite` (11,5 MB) | 22-03 |
| Modelos de partida | `object_detection_API/pre-trained-models/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8` | El de CenterNet está vacío |
| Vídeo de demo | `object_detection_API/exported-models/package_ssd_mobilenet_v2_fpnlite_320/outputff.avi` (26,5 MB) | Lo genera `real_time.py` (webcam y SSD), 09-05 [I] |
| Notebooks posteriores al último commit | `notebooks/08_box_tracking.ipynb` (15-05), `notebooks/07_Testing_package_detection.ipynb` | Copiados a `drive_snapshot/` |

Identificadores de Drive de los recursos principales:

| Recurso | ID |
|---|---|
| `package_centernet_resnet.zip` | `1ffMne4RaczS5viNDrdk0uXkPI0jgi6ej` |
| `package_ssd_mobilenet_v2_fpnlite_320.zip` | `1Krhb40oFLu0FRjKwc9SLMUoxOMMMCX5n` |
| `initial_model/model.tflite` | `18bbBPU4pbydc7k6RwCF6q71TZ2B3kxcc` |
| `training.tfrecord` / `val.tfrecord` | `1Vh-CgGFU-YI6uVHsfaRV12S8B0KxjVHU` / `1HPLByB9uRYzHsrTwpBrbrQfwkUO_CPHY` |
| CenterNet `ckpt-3.data` | `10o0vFMGv2FDKsnDAGXaeeX6qaxiS5kQH` |
| `outputff.avi` | `1UnG1EnXWAMHxGbfAg8cp6NWu76Z8RCVO` |

Formato de enlace: `https://drive.google.com/file/d/<ID>/view`. Los IDs no cambian si se mueven o
renombran los ficheros dentro de Drive.

### 5.3 Drive: carpeta `Newral` (cuenta UCM de Mario)

Enlace: <https://drive.google.com/drive/folders/1WnFAHamnQthtt-8MsntyPpeK0wRxDATY> (acceso restringido).

| Ruta | Contenido |
|---|---|
| `docs/` | Borrador de la joint venture con Nibble (14-03-2021) y documentos societarios de Newral. Los societarios no van al repo |
| `infographies/` | Infografía de la joint venture (nube de palabras y apretón de manos), logos, tipografías y notebook `word_cloud_infography.ipynb` |
| `repos/tf_webcam_detection/` | Detección en tiempo real con webcam (TF y TFLite) y grabación a `.avi`. **Copiado a `drive_snapshot/`** |
| `repos/live_video_stream_rpi_over_network/` | Servidor y cliente de streaming de vídeo de la Raspberry Pi al PC. **Copiado a `drive_snapshot/`** |
| `repos/Live-Video-Stream-from-Raspberry-Pi-Camera-over-the-Network/` | Mismo contenido que el anterior (clon original) |
| `repos/tensorflow/models/` | Clon de `tensorflow/models`. No se copia |
| `repos/nibble_box_tracking` | Acceso directo a la carpeta del 5.2 |
| `tf_models/` | Modelos del zoo de TF1 cuantizados (SSD MobileNet v1, v1 PPN, v3 small), aptos para TFLite, y una copia de trabajo de `package_ssd_mobilenet_v2_fpnlite_320` con `package_detect.tflite` (696 bytes) |
| `tf_lite_models/` | `detect.tflite` (6,9 MB, 02-05), `tflite_graph.pb` (27,7 MB) y comandos de conversión |
| `rpi_issues/` | Vacía |
| `cudnn-11.3-windows-x64-v8.2.0.53/` | Instalador de cuDNN para Windows. Irrelevante |

## 6. `drive_snapshot/`

Copia **literal** del código y la configuración que solo existían en Drive. La estructura y el detalle
fichero a fichero están en [`drive_snapshot/README.md`](../drive_snapshot/README.md). Lo único que se
ha cambiado: en los dos notebooks copiados se han **eliminado las imágenes de las salidas**, que eran
fotogramas de stock de Getty, porque el repo es público. El texto de las salidas y las trazas de error
se mantienen.

## 7. Equipo y máquinas (por las rutas que aparecen en el código)

| Quién | Entorno | Rastro |
|---|---|---|
| Beñat San Sebastián | Windows (`C:\Users\buhos\Tensorflow\workspace\training_demo`) con conda `od`. Después, Linux con conda `nibble_box_tracking` y Python 3.8 | Entrenó los modelos. CenterNet solo cargaba en su Windows |
| Mario (`Mepoide`) | Windows, Google Drive como `G:\Mi unidad\Newral\repos\…`, conda `nib_box_track` y Python 3.7 | Configs `_v_mep`, webcam, Raspberry Pi y streaming |
| `sjnj` | — | `src/path_annotation.py` |

## 8. Observaciones técnicas (AS IS, sin corregir)

### 8.1 Datos

1. **El dataset son vídeos de stock de Getty**, no imágenes de una instalación de Nibble. Hay 4 vídeos
   propios grabados con móvil y sus fotogramas, pero no consta que se usaran para entrenar.
2. **Solo hay una clase (`package`).** Los cubos y bandejas que menciona el README no se anotaron.
3. **No existe `package_dataset.csv`**, el reparto que generaba `05_test_train_split`. Hay que
   reconstruirlo a partir de los IDs de vídeo del README.
4. **El notebook `00` todavía conserva un reparto aleatorio por fotograma**, anterior al de `05`, que
   mezcla fotogramas de un mismo vídeo entre entrenamiento y validación. Está superado por el de `05`.

### 8.2 Modelos

1. **CenterNet no carga fuera de la máquina en que se entrenó.** Falla con
   `Tensor's shape (3, 3, 64, 256) is not compatible with supplied shape (1, 1, 64, 1)`. Los configs
   son coherentes entre sí: `num_classes: 1` y redimensionado a 512. Las trazas del error salen de
   versiones distintas de `center_net_meta_arch.py`, así que la hipótesis es un **desajuste de versión
   de la Object Detection API** entre máquinas [I]. Por eso, en mayo, `08_box_tracking` pasó al SSD.
2. **No hay evaluación cuantitativa guardada.** Los notebooks de few-shot "prueban" con imágenes de
   entrenamiento.
3. **Conversión a TFLite inconclusa.** El SSD v2 FPNLite (TF2) no generó un `.tflite` válido (696
   bytes). Se probó con modelos cuantizados de TF1 del zoo, que sí convierten, pero no están entrenados
   con nuestras cajas [I].

### 8.3 Código

1. **Rutas absolutas de Windows y de Drive** por todas partes (`C:\Users\buhos\…`, `G:\Mi unidad\…`).
2. **Línea corrupta** en la celda de extracción de fotogramas de `08_box_tracking.ipynb` de mayo:
   `for video_file in 095444444444444444444444444`. Es un error de sintaxis; parece una pulsación
   accidental [I].
3. **El tracking es solo un esbozo**: hay funciones auxiliares y una visualización con IDs fijos.
4. **`labelme_json_to_tfrecord.py`, función `read_label_map`**: el `line.replace(...)` no se asigna y
   las comparaciones con `"item{"`/`"}"` nunca casan. Funciona por casualidad con un `labelmap` de una
   sola clase.
5. **Excepciones capturadas sin tipo** (`except:`) en los bucles de captura de vídeo. En `00` hay una
   línea cortada (`cv2.d`).
6. **`exportnet.sh` es un comando de Windows** (rutas con `.\`), no un script de shell.
7. **Pila desfasada**: TF 2.1/2.2, Object Detection API de TF2 de 2021 y Python 3.7/3.8.
8. **En `main`, los notebooks llevan las salidas guardadas**, incluidos fotogramas de Getty, en un
   repositorio público. También se subieron `.ipynb_checkpoints/` y un `desktop.ini`.

### 8.4 Organización

1. **Dos copias del proyecto mezcladas en una sola carpeta de Drive**, y la de Beñat está incompleta.
2. **Trabajo de mayo repartido en cuatro sitios**: el Drive del proyecto, el Drive de Newral, repos
   locales sin remoto y una rama vacía. Este documento y `drive_snapshot/` lo unifican en lectura; en
   Drive no se ha movido nada.

## 9. Pendiente de este levantamiento

- **Recuentos exactos de imágenes y JSON por carpeta.** El conector de Drive pagina mal en las carpetas
  grandes; los recuentos marcados con ≥ son cotas inferiores.
- **Comprobar si hay otras clases** dentro de los JSON de `getty/mix` y del dataset de Roboflow.
- **Contenido de los zips de modelos**, que no se han descargado.
- **Ver `outputff.avi`** para confirmar qué muestra.
- **Presentación de casos de uso para Nibble**, que no se ha encontrado.
