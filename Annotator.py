import tensorflow.compat.v1 as tf
import numpy as np

class Annotator:
    def __init__(self, model_path):
        self.sess = tf.Session()
        tf.saved_model.load(sess, ['serve'], model_path)

    def gimme_bboxes(image):
        raw_images = [np.array(image)]
        detections_bs = sess.run('detections:0', {'image_arrays:0': raw_images})
        return detections_bs