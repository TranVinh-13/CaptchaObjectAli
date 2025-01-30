from ultralytics import YOLO
import cv2
import numpy as np
from util import detect_color,GetDetect,SIZE_CHECK_DICT,SIZE_CHECK,COLOR_CHECK,GetDetectObject,detect_color2
def solve(image_path, model,prompt):
    prompt = GetDetect(prompt)
    image = cv2.imread(image_path)
    # verbose=False hide any information in consle =))
    results = model.predict(source=image_path, conf=0.6, line_width=1, save=False, show=False,verbose=False)
    # results = model(source=image)
    predictions = results[0].boxes 
    boxes_detected = []
    compareMode = None
    for i, box in enumerate(predictions.xyxy.cpu().numpy()):  
        x1, y1, x2, y2 = box
        label = int(predictions.cls.cpu().numpy()[i]) 
        confidence = predictions.conf.cpu().numpy()[i]
        label_name = model.names[label]
        cropped_image = image[int(y1+5):int(y2), int(x1):int(x2-5)]
        center_x = int((x1 + x2) // 2)
        center_y = int((y1 + y2) // 2)
        # cv2.imshow("Biggest ", cropped_image)
        # cv2.waitKey(0)
        center_pixel = image[center_y, center_x]
        center_pixel_hsv = cv2.cvtColor(np.uint8([[center_pixel]]), cv2.COLOR_BGR2HSV)[0][0]
        # cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1) 
        color = detect_color2(cropped_image)
        # print( f'{label_name}-{color}')
        # cv2.putText(image, f'{label_name}-{color}: {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        if prompt[2] == "object":
            if prompt[0] != "":compareMode = SIZE_CHECK_DICT[prompt[0]]
            if prompt[1] != "":
                if prompt[1] == color:
                    boxes_detected.append( [(x2 - x1) * (y2 - y1) ,x1,y1,x2,y2,label_name,confidence])
            else:
                boxes_detected.append( [(x2 - x1) * (y2 - y1) ,x1,y1,x2,y2,label_name,confidence])
        else:
            if label_name ==GetDetectObject(prompt[2]):
                if prompt[0] != "":
                    compareMode = SIZE_CHECK_DICT[prompt[0]]
                    
                if prompt[1] != '':
                    
                    if prompt[1] == color: 
                        boxes_detected.append( [(x2 - x1) * (y2 - y1) ,x1,y1,x2,y2,label_name,confidence])
                else: 
                    boxes_detected.append( [(x2 - x1) * (y2 - y1) ,x1,y1,x2,y2,label_name,confidence])

            # cropped_image = image[int(y1):int(y2), int(x1):int(x2)]

            # hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
            # lower_yellow = np.array([20, 100, 100])
            # upper_yellow = np.array([30, 255, 255])
            # mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            # yellow_area = np.sum(mask == 255)
            # if yellow_area > 500: 
            #     area = (x2 - x1) * (y2 - y1) 
            #     yellow_cones.append((area, x1, y1, x2, y2, label_name, confidence))
    current_box = boxes_detected[0]
    if compareMode != None:
        current_box = compareMode(boxes_detected,key = lambda x:x[0])
    area,x1, y1, x2, y2, label_name, confidence = current_box
    # print(prompt)
    # cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    # cv2.putText(image, f'{label_name}: {confidence:.2f}', (int(x1), int(y1) - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    # cv2.imshow("result ", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # return current_box
    return  int((x1 + x2) // 2),int((y1+y2)//2)
   


model = YOLO("best.pt",task="detect")
if __name__ == "__main__":
    prompt = "Please click the smallest yellow object."
    image_path = '.\\img\\Pleaseclickthesmallestyellowobject._1eac5cca-ce7b-401d-8b00-c641adb01700.jpg'
    biggest_cone = solve(image_path, model,prompt)
    print(biggest_cone)
