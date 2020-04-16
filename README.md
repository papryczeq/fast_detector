# fast_detector

Object detector based on [EfficientDet](https://arxiv.org/abs/1911.09070).

## Run

Build one of EfficentDet models [here](https://github.com/google/automl) or
download already builded [here](https://drive.google.com/open?id=17ucEeIw6ifMcySXVAmOQmwikEVq1Q9Yc)

Then run code:

```
python detector.py --saved_model=path_to_saved_model_dir --input=path_to_images_dir --output=output_dir
```

and you will get pictures with bounding boxes of all COCO classes + JSON file with detections. 

## References
- Project borrows some parts from the official implementation [google/automl](https://github.com/google/automl)