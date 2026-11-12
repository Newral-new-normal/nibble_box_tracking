# TFlite Webcam Detection

To use tf_lite models:

src/tflite_webcam_detection.python

To use tf models:

src/real_time.py
src/


## Installation

TFlite Installation on RPi Zero W: https://github.com/cloudwiser/TensorFlowLiteRPIZero

How to Perform Object Detection with TensorFlow Lite on Raspberry Pi: https://www.digikey.com/en/maker/projects/how-to-perform-object-detection-with-tensorflow-lite-on-raspberry-pi/b929e1519c7c43d5b2c6f89984883588
TFlite environment

Object Detection API: https://www.tensorflow.org/lite/examples/object_detection/overview

Running on mobile with TensorFlow Lite: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_on_mobile_tensorflowlite.md

Running TF2 Detection API Models on mobile: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_on_mobile_tf2.md

TensorFlow Lite converter: https://www.tensorflow.org/lite/convert

tflite_convert_commands_Windows: src/tflite_convert_commands_Windows.txt

Training Custom Object Detector: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html#

“TypeError: Expected Operation, Variable, or Tensor, got level_5”: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/issues.html#export-error

### RPi Config
```
sudo raspi-config
(Performance- Video Memory 32MB)
```

Streaming Rpi camera to server
https://github.com/Arijit1080/Live-Video-Stream-from-Raspberry-Pi-Camera-over-the-Network

### Install Python 3.7

https://installvirtual.com/install-python-3-7-on-raspberry-pi/

```
alias python=python3.7
```

TensorFlow 2.4 environment

```
mkdir -p Projects/Python/tf24
cd Projects/Python/tf24
python -m venv tf24-env
source tf24-env/bin/activate
```

TensorFlow 2.4 installation
https://github.com/lhelontra/tensorflow-on-arm/releases

```(tf24)
# wget https://storage.googleapis.com/tensorflow/raspberrypi/tensorflow-2.3.0rc2-cp35-none-linux_armv6l.whl
# wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp35-none-linux_armv6l.whl
# wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.3.0/tensorflow-2.3.0-cp35-none-linux_armv6l.whl
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv6l.whl
python -m pip install tensorflow-2.4.0-cp37-none-linux_armv6l.whl --no-cache-dir
```

Install additional libraries... and object_detection: https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi

## Usage

```Anaconda Prompt
(nib_box_track) G:\Mi unidad\Newral\repos\nibble_box_tracking\object_detection_API\exported-models\package_ssd_mobilenet_v2_fpnlite_320>python ..\..\..\..\tf_lite_webcam_detection\src\real_time.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)