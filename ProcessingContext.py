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

    def get_path_without_root(self, file_path):
        return file_path[len(self.input_path):]

    def is_next(self):
        if len(self.all_files) >= self.index:
            return True
        else:
            return False

    def get_next_item(self):
        if self.video:
            return get_video_frame()

        self.item = self.all_files[self.index]
        if self.item[0] == 'image':
            self.index += 1
            self.img = Image.open(self.item[1])
            return [self.index-1, self.img]
        elif self.item[0] == 'video':
            #self.index += 1
            return video_processing()

    def video_processing(self):
        self.item = self.all_files[self.index]
        if self.video:
            return get_video_frame()
        else:
            self.video = True
            self.video_cap = cv2.VideoCapture(self.item[1])
            return get_video_frame()

    def get_video_frame(self):
        ret, frame = self.video_cap.read()
        if not ret:
            self.video = False
            self.index += 1
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(img_rgb)
        return [self.index, self.img]

    def save_result(self, results):
        id, detection = results
        self.all_results.append(results)
        file_name = self.item[1].split("/")[-1]
        file_save_path = self.output_path + "/" + get_path_without_root("".join(self.item[1].split("/")[:-1]) #need refactor
        #TODO saving images/video with bboxes
        if self.video:
            if os.path.exists(file_save_path):
                pass
        else:
            pass

    def save_all_to_json(self):
        pass