import Annotator
import ProcessingContext


def main(path):
    context = ProcessingContext(path)
    annotator = Annotator()

    results = []
    while context.is_next():
        id, img = context.get_netx_item()
        detections = annotator.gimme_bboxes(img)
        context.save_result([id, detections])
    context.save_all_to_json():

if __name__ == '__main__':
    main()