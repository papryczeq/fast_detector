import tensorflow.compat.v1 as tf
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os


parser = argparse.ArgumentParser(description="Detector based on efficientdet")
parser.add_argument("--saved_model", default="saved_model", type=str, help="Path to saved efficientdet model")
parser.add_argument("--input", default=None, type=str, help="Path do directory with pictures to process")
parser.add_argument("--output", default=None, type=str, help="Path to output folder")
parser.add_argument("--json_only", default=False, type=bool, help="Return only json with detections")
args = parser.parse_args()

coco_id_mapping = {
    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
    6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
    11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
    16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
    22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack',
    28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
    35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite',
    39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard',
    43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork',
    49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple',
    54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog',
    59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch',
    64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv',
    73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone',
    78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator',
    84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear',
    89: 'hair drier', 90: 'toothbrush',
}


def get_images(images_path):
    images_name = []
    images = []
    for img in tf.io.gfile.glob([images_path + '/*.jpg', images_path + '/*.png', images_path + '/*.jpeg']):
        images_name.append(img.split('/')[-1])
        images.append(Image.open(img))
    return images_name, images

def get_detections(model_path, images):
    detections = []
    with tf.Session() as sess:
        tf.saved_model.load(sess, ['serve'], model_path)
        for img in images:
            raw_images = [np.array(img)]
            detections_bs = sess.run('detections:0', {'image_arrays:0': raw_images})
            detections.append(detections_bs)
    return detections

def make_json(images_name, detections, save_path):
    data = {}
    for idx, detection in enumerate(detections):
        boxes = detection[:, 1:5].tolist()
        classes = detection[:, 6].astype(int).tolist()
        scores = detection[:, 5].tolist()
        data[images_name[idx]] = {
            'boxes': boxes,
            'classes': classes,
            'scores': scores
        }
    with open(save_path + "/detections.json", "w") as write_file:
        json.dump(data, write_file)

def draw_bboxes(images_name, images, detections, save_path):
    for idx, detection in enumerate(detections):
        boxes = detection[0][:, 1:5]
        classes = detection[0][:, 6].astype(int)
        scores = detection[0][:, 5]
        
        # convert [x, y, width, height] to [ymin, xmin, ymax, xmax]
        boxes[:, 2:4] += boxes[:, 0:2]
        
        img = images[idx]
        for i in range(boxes.shape[0]):
            #hardcoded, I know that
            if scores[i] < 0.2:
                continue
            ymin, xmin, ymax, xmax = boxes[i].tolist()

            draw = ImageDraw.Draw(img)
            (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
            #TODO customize color
            draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=2, fill=(0,0,255))

            try:
                font = ImageFont.truetype('arial.ttf', 24)
            except IOError:
                font = ImageFont.load_default()
            text = coco_id_mapping[classes[i]] + ": " + str(round(scores[i]*100)) + "%"
            draw.text((left, bottom), text, fill=(0,0,255), font=font)
        file_path = save_path + "/" + images_name[idx]
        img.save(file_path)

        
if __name__ == '__main__':
    images_name, images = get_images(args.input)
    detections = get_detections(args.saved_model, images)
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    make_json(images_name, detections, output_dir)
    if not args.json_only:
        draw_bboxes(images_name, images, detections, output_dir)