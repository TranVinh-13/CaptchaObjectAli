import numpy as np
import torch
import sys
import os
import cv2
import torchvision.transforms as transforms
from os import path
from os import getcwd
from ops import non_max_suppression, resize_and_pad_image, scale_boxes
"""
0:tron
1:lapphuong
2:non
3:tru
4:lucgiac



"""
from util import GetDetect
class YoloCaptchaV2:
    def __init__(self, weight_path):
        self.torch_script_model = torch.jit.load(weight_path)

    def find_most_similar_characters(self, image, show=False):
        original_image = cv2.imread(str(image))
        image = resize_and_pad_image(original_image)
        transform = transforms.ToTensor()
        tensor = transform(image)
        preds = self.torch_script_model(tensor.unsqueeze(0))
        preds = non_max_suppression(preds, 0.25, 0.7, agnostic=False,max_det=300,classes=None)[0]
        data = preds[:, :4].numpy()
   
        data[:, :4] = scale_boxes( image.shape,data[:, :4], original_image.shape).astype(int)
        unique_labels, label_counts = np.unique(preds[:, -1], return_counts=True)
        labels_appearing_twice = unique_labels[label_counts >= 2]
        center_points = []
        print(unique_labels,label_counts)
        for label in labels_appearing_twice:
           
            label_indices = np.where(preds[:, -1] == label)[0]
            print(label)
            label_bboxes = data[label_indices, :4]
            label_center_x = ((label_bboxes[:, 0] + label_bboxes[:, 2]) / 2.0).astype(int)
            label_center_y = ((label_bboxes[:, 1] + label_bboxes[:, 3]) / 2.0).astype(int)
            label_centers = np.stack((label_center_x, label_center_y), axis=-1)
            center_points.append(label_centers)
        center_points =np.vstack(center_points)[:2]
        original_height, original_width = original_image.shape[:2]
        center_points = center_points.astype(int)
        for point in center_points:
            
            x, y = point
            cv2.circle(original_image, (x, y), 5, (0, 255, 0), -1) 
        cv2.imshow("Image with Points", original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return center_points
prompt = 'Please click the yellow cone'
filename = 'Pleaseclicktheyellowcone._a822290e-59a7-4044-81f8-82c89bfb02d7.jpg'
print(YoloCaptchaV2('best.torchscript').find_most_similar_characters('img\\Pleaseclicktheyellowcone._a822290e-59a7-4044-81f8-82c89bfb02d7.jpg'))