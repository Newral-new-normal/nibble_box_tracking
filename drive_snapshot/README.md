# drive_snapshot — lo que solo existía en Drive

Copia literal (noviembre 2026) de los ficheros de **código y configuración** que no estaban en git ni
en ningún otro repositorio. Los datos y los modelos **no** se copian; se enlazan desde
[`docs/AS-IS.md`](../docs/AS-IS.md#5-dónde-está-cada-cosa).

Las rutas reproducen la ubicación original en Drive:

- `nibble_box_tracking_drive/` → carpeta de Drive `nibble_box_tracking` (cuenta de Newral)
- `newral_drive/` → carpeta de Drive `Newral` (cuenta UCM de Mario)

| Fichero | Origen en Drive | Por qué está aquí |
|---|---|---|
| `nibble_box_tracking_drive/notebooks/08_box_tracking.ipynb` | `notebooks/` (Beñat, 15-05-2021) | Versión posterior al último commit: usa el SSD y añade el tracking naive por IoU |
| `nibble_box_tracking_drive/notebooks/07_Testing_package_detection.ipynb` | `notebooks/` (Beñat, 17-04-2021) | Versión posterior al último commit, con rutas relativas y el error de CenterNet en Linux |
| `nibble_box_tracking_drive/object_detection_API/models/box_centernet_resnet101_v1_fpn_512/pipeline.config` | Igual | Config de entrenamiento de CenterNet (2.500 pasos, Adam) |
| `nibble_box_tracking_drive/object_detection_API/exported-models/package_ssd_mobilenet_v2_fpnlite_320/pipeline.config` | Igual | Config del SSD exportado (rutas de la máquina de Beñat) |
| `nibble_box_tracking_drive/object_detection_API/exported-models/package_ssd_mobilenet_v2_fpnlite_320/pipeline_v_mep.config` | Igual | La misma config reescrita con rutas `G:\Mi unidad\…` |
| `newral_drive/repos/tf_webcam_detection/README.md` | `repos/tf_webcam_detection/` | Versión del README **más reciente que la de GitHub**: añade las notas de la Raspberry Pi Zero (TF 2.4 para armv6) y de streaming |
| `newral_drive/tf_models/package_ssd_mobilenet_v2_fpnlite_320/labelmap.txt` | Igual | Labelmap en formato texto que espera el script TFLite |

## Cambios respecto al original

- En los dos notebooks se han **eliminado las imágenes de las salidas** (fotogramas de stock de
  Getty), porque el repo es público. El texto de las salidas y las trazas de error se conservan.
  Los notebooks se han reescrito con el formato JSON estándar de Jupyter (indent 1).
- El resto de ficheros son copias byte a byte, con finales de línea CRLF donde los tenían.

## Qué no se ha copiado, y por qué

| En Drive | Motivo |
|---|---|
| `Newral/repos/tf_webcam_detection/` (código) | Ya está en GitHub: <https://github.com/Newral-new-normal/tf_webcam_detection>. El código es idéntico; solo cambian los finales de línea |
| `Newral/repos/live_video_stream_rpi_over_network/` | Ya está en GitHub: <https://github.com/Newral-new-normal/live_video_stream_rpi_over_network>. Es idéntico; a su vez es copia de <https://github.com/Arijit1080/Live-Video-Stream-from-Raspberry-Pi-Camera-over-the-Network> |
| `pipeline_v_mep_rpi.config` | Idéntico byte a byte a `pipeline_v_mep.config` |
| Copias de `pipeline.config`, `pipeline_v_mep.config` y `labelmap.pbtxt` en `Newral/tf_models/` | Idénticas a las de arriba y a la del repo (salvo espacios en blanco) |
| `Newral/tf_lite_models/tflite_convert_commands_Windows.txt` | Versión anterior y más corta del fichero que está en el repo `tf_webcam_detection` |
| `.idea/`, `.ipynb_checkpoints/`, `.git/` y `.sync.ffs_db` | Metadatos de herramientas |
| Documentos societarios de `Newral/docs/` | No son del proyecto |
