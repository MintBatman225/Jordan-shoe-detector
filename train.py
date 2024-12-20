import os
from ultralytics import YOLO

config_path = './config.yaml'

if __name__ == '__main__':
    # Load the pretrained YOLOv8 small model
    model = YOLO(r'C:\Users\markj\work\practice\shoe_detector\runs\detect\train26\weights\last.pt')

    # Now `model` is loaded and ready for training, inference, or fine-tuning
    model.train(data=config_path, epochs=200, batch=32)
