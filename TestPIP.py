
import torch
import torchvision
print(torch.__version__, torch.cuda.is_available())
print(torch. version )
print(torch.version.cuda)
from torch.utils.collect_env import main
main()


import pickle 
import flask
from flask_cors import CORS
from flask import request, jsonify
from flask import Flask
from flask import send_file
import requests



import detectron2
print("Detectron2 Version = ", detectron2.__version__)
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer
import cv2
import numpy as np


# Convert URL to image 
def score_image(predictor: DefaultPredictor, image_url: str):
    
    image_reponse = requests.get(image_url) # load an image
    image_as_np_array = np.frombuffer(image_reponse.content, np.uint8) 
    image = cv2.imdecode(image_as_np_array, cv2.IMREAD_COLOR) # Converts data into image format

    # make prediction
    return predictor(image)


# Create the model
def prepare_pridctor():
    # create config
    cfg = get_cfg()
    
    # below path applies to current installation location of Detectron2
    # model_final_f10217.pkl 
    cfgFile =  model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.merge_from_file(cfgFile)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cpu" # using a CPU Detectron copy

    classes = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes # The things in the image 
    predictor = DefaultPredictor(cfg) # Predict values
    print("Predictor has been initialized.")
    return (predictor, classes)


app = flask.Flask(__name__) # __name__ is just the name of the module.

CORS(app) # To handle Cross Origin Resource Sharing

predictor, classes = prepare_pridctor() # Load the model/predictor


@app.route("/predict-image", methods=["POST"])
def process_score_image_request():
    
    image_url = request.json["imageUrl"]
    scoring_result = score_image(predictor, image_url)

    instances = scoring_result["instances"] # Instances in the image.

    scores = instances.get_fields()["scores"].tolist()

    pred_classe = instances.get_fields()["pred_classes"].tolist()

    pred_boxes = instances.get_fields()["pred_boxes"].tensor.tolist()
    
    classeslist = []
    count = 0
    
    # Go through the predicted class.
    # I think it's not optimal to put "for loop".
    for data in scoring_result["instances"].pred_classes:
        num = data.item() # The number of the instance.
        count = count +1
        classeslist.append(MetadataCatalog.get(predictor.cfg.DATASETS.TRAIN[0]).thing_classes[num])
    
    # Prepate the output metadata.
    response = {
        "scores": scores,
        "classeslist": classeslist,
        "pred_boxes" : pred_boxes,
        "The model predicted: ":  count
    }
    
    
    ## I think it's better if I change the index to show the image. 
    ## Prepate image with instance segmentation.
    # v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)

    # outimage = v.draw_instance_predictions(instances["instances"].to("cpu"))
    
    # , send_file(outimage, mimetype='image/gif')
    return (jsonify(response)) # "jasonify" to "dump" the output as JSON-formatted string. 
            
            

@app.route("/")
def main():
    return "hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0")