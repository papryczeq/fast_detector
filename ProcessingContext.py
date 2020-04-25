from PIL import Image
import cv2
from utils.io_utils import check_path


class ProcessingContext:
    def __init__(self, input_path, output_path):
        self.all_files = check_path(input_path)  # all images/video from path -> [['image', path_to_file],...]
        self.input_path = input_path
        self.output_path = output_path
        self.index = 0
        self.video = False
        self.img = None
        self.all_results = []

    def split_path(path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    def get_path_without_root(self, file_path):
        dirname = split_path(os.path.dirname(file_path))
        root = split_path(self.input_path)
        path = [d for d in dirname if d not in root]
        return os.path.join(*path)

    def is_next(self):
        return len(self.all_files) >= self.index

    def get_next_item(self):
        if self.video:
            return get_video_frame()

        self.item = self.all_files[self.index]
        self.index += 1
        if self.item[0] == 'image':
            self.img = Image.open(self.item[1])
            return [self.index-1, self.img]
        elif self.item[0] == 'video':
            return video_processing()

    def video_processing(self):
        if self.video:
            self.frame_id += 1
            return get_video_frame()
        else:
            self.video = True
            self.frame_id = 0
            self.video_cap = cv2.VideoCapture(self.item[1])
            return get_video_frame()

    def get_video_frame(self):
        ret, frame = self.video_cap.read()
        if not ret:
            self.video = False
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(img_rgb)
        return [self.index-1, self.img]

    def save_result(self, results):
        id, detection = results
        if self.item[0] == 'video':
            self.all_results.append([id, self.frame_id, detection])
        else:
            self.all_results.append([id, None, detection])
        file_name = os.path.basename(self.item[1])
        file_save_path = os.path.join(self.output_path, get_path_without_root(self.item[1]))
        tmp_dir = os.path.join(file_save_path, f'tmp_{os.path.splitext(file_name)[0]}')
        if self.item[0] == 'video':
            if not os.path.exists(tmp_dir):
                os.mkdir(tmp_dir)
            #TODO save frame
            if self.video: #there are more frames to processing
                #TODO save video
        else:
            os.mkdir(file_save_path)
            #TODO save image

    def save_all_to_json(self):
        data = {}
        for id, frame_id, detection in self.all_results:
            file = self.all_files[i]
            file_name = os,path.basename(file[1])
            if file[0] == 'video':
                file_name += f'_{str(frame_id)}'
            boxes, classes, scores = detection
            data[file_name] = {
                'boxes': boxes,
                'classes': classes,
                'scores': scores
            }
        json_path = os.path.join(self.output_path, "/detections.json")
        with open(json_path, "w") as write_file:
            json.dump(data, write_file)
        print(f'JSON with detections saved: {json_path}')