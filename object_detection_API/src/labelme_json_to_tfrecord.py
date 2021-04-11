r"""
This code takes labelme annotations to tfrecords

Example of call in command prompt at models/research:

    python   C:\Users\buhos\Tensorflow\workspace\training_demo\src\labelme_json_to_tfrecord.py --input_path=C:\Users\buhos\Tensorflow\workspace\training_demo\images\train_json --labelmap_path=C:\Users\buhos\Tensorflow\workspace\training_demo\annotations\labelmap.pbtxt --output_path=C:\Users\buhos\Tensorflow\workspace\training_demo\images\training.tfrecords

"""




import tensorflow.compat.v1 as tf
import os
import numpy as np
import json
import base64
from object_detection.utils import dataset_util

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('input_path','', 'Path to JSONs annotations folder') 
flags.DEFINE_string('labelmap_path','', 'Path to labelmap .pbtxt file') 
FLAGS = flags.FLAGS


def read_label_map(label_map_path):
  item_id = None
  item_name = None
  items = {}
    
  with open(label_map_path, "r") as file:
    for line in file:
      line.replace(" ", "")
      if line == "item{":
        pass
      elif line == "}":
        pass
      elif "id" in line:
        item_id = int(line.split(":", 1)[1].strip())
      elif "name" in line:
        item_name = line.split(":", 1)[1].replace("'", "").strip()

      if item_id is not None and item_name is not None:
        items[item_name] = item_id
        item_id = None
        item_name = None

  return items

def create_tf_example(example):
  # TODO(user): Populate the following variables from your example.

  height = int(example['imageHeight']) # Image height
  width = int(example['imageWidth']) # Image width
  filename = str.encode(example['imagePath']) # Filename of the image. Empty if image is not from file
  encoded_image_data = base64.b64decode(example["imageData"]) # Encoded image bytes
  image_format = b'jpeg' # b'jpeg' or b'png'

  xmins = [np.min(np.array(i['points'])[:,0])/width for i in example['shapes']] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [np.max(np.array(i['points'])[:,0])/width for i in example['shapes']] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [np.min(np.array(i['points'])[:,1])/height for i in example['shapes']] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [np.max(np.array(i['points'])[:,1])/height for i in example['shapes']] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = [str.encode(i['label']) for i in example['shapes']] # List of string class name of bounding box (1 per box)
  dict_labels_id = read_label_map(FLAGS.labelmap_path)
  classes = [int(dict_labels_id[i['label']]) for i in  example['shapes']] # List of integer class id of bounding box (1 per box)

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example


def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
  folder_path = FLAGS.input_path


  # TODO(user): Write code to read in your dataset to examples variable
  examples = [os.path.join(folder_path, i) for i in  os.listdir(folder_path)]

  for example in examples:
    with open(example,'r') as file:
      example_json = json.load(file)
    tf_example = create_tf_example(example_json)
    writer.write(tf_example.SerializeToString())

  writer.close()


if __name__ == '__main__':
  tf.app.run()
