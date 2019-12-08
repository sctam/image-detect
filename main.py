import time
import threading
import cv2
import numpy as np
import mss
import mss.tools
import pyscreenshot as ImageGrab
from matplotlib import pyplot as plt
from playsound import playsound
from tkinter import *

from PIL import Image, ImageTk

# Set up thing to look for.
TEMPLATE = cv2.imread(r'images\dot.jpg', 0)
TEMPLATE_W, TEMPLATE_H = TEMPLATE.shape[::-1]

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.monitor = mss.mss().monitors

        self.window_x = 0
        self.window_y = 0
        self.window_w = 240
        self.window_h = 230

        self._setup_ui()

    def _setup_ui(self):
        self.master.title("Gather Sounds")
        # Build menus.
        menu = Menu(self.master)
        self.master.config(menu=menu) # Add menu up top.
        file = Menu(menu, tearoff=0)
        file.add_command(label="Exit", command=self._exit_program) # Add exit command to file menu.
        menu.add_cascade(label="File", menu=file) # Add file menu to the bar.

        # Build labels.
        self.label_x = Label(self.master, text="X")
        self.label_y = Label(self.master, text="Y")
        self.label_w = Label(self.master, text="Width")
        self.label_h = Label(self.master, text="Height")
        self.label_x.grid(row=0, column=0)
        self.label_y.grid(row=1, column=0)
        self.label_w.grid(row=2, column=0)
        self.label_h.grid(row=3, column=0)
        
        # Build sliders.
        limit_left   = self.monitor[0]['left']
        limit_right  = limit_left + self.monitor[0]['width']
        limit_top    = self.monitor[0]['top']
        limit_bottom = limit_top + self.monitor[0]['height']
        self.slider_x = Scale(self.master, length=400, from_=limit_left, to=limit_right,  orient=HORIZONTAL, command=self._update_vars_x)
        self.slider_y = Scale(self.master, length=400, from_=limit_top,  to=limit_bottom, orient=HORIZONTAL, command=self._update_vars_y)
        self.slider_w = Scale(self.master, length=400, from_=1, to=1000, orient=HORIZONTAL, command=self._update_vars_w)
        self.slider_h = Scale(self.master, length=400, from_=1, to=1000, orient=HORIZONTAL, command=self._update_vars_h)
        self.slider_x.grid(row=0, column=1)
        self.slider_y.grid(row=1, column=1)
        self.slider_w.grid(row=2, column=1)
        self.slider_h.grid(row=3, column=1)

        # Setup label for image.
        self.label_image = Label(self.master)
        self.label_image.grid(row=0, column=3, rowspan=4)
        self._update_image() # Update image.

        self.slider_x.set(self.window_x)
        self.slider_y.set(self.window_y)
        self.slider_w.set(self.window_w)
        self.slider_h.set(self.window_h)
        
    def _update_image(self):
        exec_start = time.time()       

        with mss.mss() as screenshot:
            monitor = {"left": self.window_x, "top": self.window_y, "width": self.window_w, "height": self.window_h}
            img = screenshot.grab(monitor)
            img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            img = ImageTk.PhotoImage(img)
            self.label_image.configure(image=img)
            self.label_image.image = img

        print(time.time() - exec_start) # Time critical component.


    def _update_vars_x(self, value):
        self.window_x = int(value)
        self._update_image()
    def _update_vars_y(self, value):
        self.window_y = int(value)
        self._update_image()
    def _update_vars_w(self, value):
        self.window_w = int(value)
        self._update_image()
    def _update_vars_h(self, value):
        self.window_h = int(value)
        self._update_image()
    
    def _exit_program(self):
        exit()

# def _process_image():
#     threading.Timer(0.8, _process_image).start()
#     exec_start = time.time()

#     pil_img = ImageGrab.grab(bbox=(WINDOW_X, WINDOW_Y, WINDOW_X+WINDOW_W, WINDOW_Y+WINDOW_H))  # X1,Y1,X2,Y2

#     # Convery PIL to CV
#     img_rgb = np.array(pil_img) 
#     img_rgb = img_rgb[:, :, ::-1].copy() # Convert RGB to BGR 

#     # Set up base image to look at.
#     #img_rgb  = cv2.imread('base.jpg')
#     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

#     # Match.
#     res = cv2.matchTemplate(img_gray, TEMPLATE, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.8
#     loc = np.where(res >= threshold)
#     for pt in zip(*loc[::-1]):
#         cv2.rectangle(img_rgb, pt, (pt[0] + TEMPLATE_W, pt[1] + TEMPLATE_H), (0, 0, 255), 2)

#     if loc[0].size > 0:
#         playsound(r'sounds\beep2.wav', False)
#         print("found")

#     cv2.imwrite('result.png', img_rgb)

#     exec_end = (time.time() - exec_start)
#     print(exec_end)

def main():
    #_process_image()

    root = Tk()
    app = Window(root)

    root.mainloop()  

if __name__ == "__main__":
    main()
