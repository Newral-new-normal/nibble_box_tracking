# Notes on TF object detection API

The current folder (training_demo/) mostly mimics the procedure explained in https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/index.html


### Data adquisition

In the images/train folder the images of packages annotated with labelme (https://github.com/wkentaro/labelme). The annotation outputs have a json format.

Create the labelmap.pbtxt for the classes to be detected (in this example it is stored in /images).

In the version used, the dataset consisted on 847 photos that belonged to 12 videos. The train-validation split was done using notebooks/0_test_train_split.ipynb, where all the images from 4 random videos were chosen as the validation set and the rest as the training set. Validation videos ids: ['476762116', '477008982', '141728167', '162812920']; which supposed a 34% of the total number of photos.

The annotation json's were transformed into tfrecords using the code from src/labelme_json_to_tfrecord.py. Example of call in command prompt at models/research:

python   C:\Users\buhos\Tensorflow\workspace\training_demo\src\labelme_json_to_tfrecord.py --input_path=C:\Users\buhos\Tensorflow\workspace\training_demo\images\train_json --labelmap_path=C:\Users\buhos\Tensorflow\workspace\training_demo\annotations\labelmap.pbtxt --output_path=C:\Users\buhos\Tensorflow\workspace\training_demo\images\training.tfrecords



### Model download an configuration file:

Download a model from https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
and store it inside the folder pre-trained-models/

Copy the config file and paste it inside a new folder inside models/ (models/box_centernet_resnet101_v1_fpn_512).

Edit the config file following https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html#configure-the-training-pipeline

### Training

Copy the file models/research/object_detection/model_main_tf2.py of the tensorflow object detection API and save a copy it in the folder we are working at, i.e. training_demo/model_main_tf2.py

Call it from a command prompt:

python model_main_tf2.py --model_dir=models/box_centernet_resnet101_v1_fpn_512 --pipeline_config_path=models/box_centernet_resnet101_v1_fpn_512/pipeline.config

### Export the model

Copy the file models/research/object_detection/exporter_main_v2.py of the tensorflow object detection API and save a copy it in the folder we are working at, i.e. training_demo/exporter_main_v2.py

Call it from a command prompt:

python .\exporter_main_v2.py --input_type image_tensor --pipeline_config_path .\models\box_centernet_resnet101_v1_fpn_512\pipeline.config --trained_checkpoint_dir .\models\box_centernet_resnet101_v1_fpn_512\ --output_directory .\exported-models\package_centernet_resnet


### Appendix: Environment installation 

## Conda environment `nib_box_track` for tensorflow-gpu 2.2.0

Best approach so far (from here: https://stackoverflow.com/questions/65273118/why-is-tensorflow-not-recognizing-my-gpu-after-conda-install):

```
conda create --name nib_box_track tensorflow-gpu=2.1
conda activate nib_box_track
pip install tensorflow-gpu==2.2.0 --user
```
The first one will install automatically cuDNN and CUDAToolkit (a pain in the ass if you go manual).

Then activate and upgrade with `pip` the tf version (`--user` flag optional if it an error is thrown without it).

Check it
```
python
>>> import tensorflow as tf 
>>> tf.test.is_built_with_cuda() # True
>>> tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None) # GeForce GTX 1660 SUPER, Compute Capability 7.5
```

## Additional actions needed `object_detection` package

https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html#tensorflow-object-detection-api-installation

(Install https://visualstudio.microsoft.com/es/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16
Checking MSVC 14+)

In order to get `object_detection` python library to work:
```
git clone https://github.com/tensorflow/models.git
cd models/research
protoc object_detection/protos/*.proto --python_out=.

cd object_detection/packages/tf2/setup.py .
python -m pip install .

# From within TensorFlow/models/research/
cp object_detection/packages/tf2/setup.py . # copy object_detection\packages\tf2\setup.py .
python -m pip install .
```

Test it:

```
# From within TensorFlow/models/research/
python object_detection/builders/model_builder_tf2_test.py
```
