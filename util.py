import cv2
import numpy as np
SIZE_CHECK = ['tiny','largest','smallest','biggest']
COLOR_CHECK = ['red','blue','green','gray','yellow']
OBJECT_CHECK = ['object','polyhedron','sphere','cylinder','cube','ball','cone']
DATA_CHECK = {'ball':0,'sphere':0,'cube':1,'cone':2,'cylinder':3,'polyhedron':4,'object':5}
SIZE_CHECK_DICT = {'tiny':min,'largest':max,'smallest':min,'biggest':max}
#cylinder hinh tru
import subprocess
def GetDetectObject(label_name):
    if label_name == 'object':
        return  'object'
    elif label_name == 'sphere' or label_name == 'ball':
        return 'tron'
    elif label_name == 'polyhedron':
        return 'lucgiac'
    elif label_name == 'cone':
        return 'non'
    elif label_name == 'cylinder':
        return 'tru'
    elif label_name == 'cube':
        return 'lapphuong'

def RunJSFile(filename):
    result = subprocess.run(['node', filename], capture_output=True, text=True)
    return result.stdout.strip()
def GetDetect(prompt:str):
    res = prompt.replace('.','').split()[3:]
    s = c = o = ''
    if res[0] not in SIZE_CHECK:
        if res[0] not in COLOR_CHECK:
            o = res[0]
        else:
            c = res[0]
            o = res[1]
    else:
        s = res[0]
        if res[1] not in COLOR_CHECK:
            o = res[1]
        else:
            c = res[1]
            o = res[2]
    return s,c,o
def detect_color(hsv_value):
    h, s, v = hsv_value
    print(h,s,v)
    if 100 <= h <= 140 and s > 50 and v > 50:
        return "blue"
    elif 35 <= h <= 85 and s > 50 and v > 50:
        return "green"
    elif (0 <= h <= 10 or 170 <= h <= 180) and s > 50 and v > 50:
        return "red"
    elif 20 <= h <= 35 and s > 50 and v > 50:
        return "yellow"
    elif s < 30 and v > 100:  # Low saturation and high value (Gray)
        return "gray"
    else:
        
        return "Unknown"
def detect_color2(hsv_image):
    # Define color ranges in HSV space
    
    # Blue: Hue between 100 and 140
    blue_lower = np.array([100, 150, 50])
    blue_upper = np.array([140, 255, 255])
    
    # Green: Hue between 35 and 85
    green_lower = np.array([35, 50, 50])
    green_upper = np.array([85, 255, 255])
    
    # Red: Hue between 0-10 or 170-180
    red_lower1 = np.array([0, 150, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 150, 50])
    red_upper2 = np.array([180, 255, 255])
    
    # Yellow: Hue between 20 and 35
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([35, 255, 255])
    
    # Gray: Low saturation and high value
    gray_lower = np.array([0, 0, 100])
    gray_upper = np.array([180, 30, 200])

    # Convert image to HSV
    hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
    
    # Create masks for each color range
    blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper)
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
    red_mask1 = cv2.inRange(hsv_image, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv_image, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    gray_mask = cv2.inRange(hsv_image, gray_lower, gray_upper)
    
    # Calculate the number of non-zero pixels in each mask
    blue_pixels = cv2.countNonZero(blue_mask)
    green_pixels = cv2.countNonZero(green_mask)
    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    gray_pixels = cv2.countNonZero(gray_mask)
    
    # Determine the most dominant color
    color_counts = {
        "blue": blue_pixels,
        "green": green_pixels,
        "red": red_pixels,
        "yellow": yellow_pixels,
        "gray": gray_pixels
    }

    dominant_color = max(color_counts, key=color_counts.get)
    
    return dominant_color

# print(GetDetect('Please click the blue sphere. '))


    