import time
import threading
import cv2
import numpy as np
import pyscreenshot as ImageGrab
from matplotlib import pyplot as plt
from playsound import playsound

WINDOW_X = 2290
WINDOW_Y = 50
WINDOW_W = 240
WINDOW_H = 230

# Set up thing to look for.
TEMPLATE = cv2.imread(r'images\dot.jpg', 0)
TEMPLATE_W, TEMPLATE_H = TEMPLATE.shape[::-1]

def _process_image():
    threading.Timer(0.8, _process_image).start()
    exec_start = time.time()

    pil_img = ImageGrab.grab(bbox=(WINDOW_X, WINDOW_Y, WINDOW_X+WINDOW_W, WINDOW_Y+WINDOW_H))  # X1,Y1,X2,Y2

    # Convery PIL to CV
    img_rgb = np.array(pil_img) 
    img_rgb = img_rgb[:, :, ::-1].copy() # Convert RGB to BGR 

    # Set up base image to look at.
    #img_rgb  = cv2.imread('base.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Match.
    res = cv2.matchTemplate(img_gray, TEMPLATE, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + TEMPLATE_W, pt[1] + TEMPLATE_H), (0, 0, 255), 2)

    if loc[0].size > 0:
        playsound(r'sounds\beep2.wav', False)
        print("found")

    cv2.imwrite('result.png', img_rgb)

    exec_end = (time.time() - exec_start)
    print(exec_end)

def main():
    _process_image()

if __name__ == "__main__":
    main()