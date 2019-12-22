import time
import cv2
import numpy as np
import mss
import pyscreenshot as ImageGrab
from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk

# Set up thing to look for.
REFERENCE_PATH = r'images\reference.jpg'
REFERENCE_IMG = cv2.imread(REFERENCE_PATH, 0)
REFERENCE_W, REFERENCE_H = REFERENCE_IMG.shape[::-1]

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.monitor = mss.mss().monitors

        self.window_x = 0
        self.window_y = 0
        self.window_w = 240
        self.window_h = 230
        self.window_t = 0.77
        self.alerted = False

        self._setup_ui()

    def _setup_ui(self):
        self.master.title("Image Detect")
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
        self.label_t = Label(self.master, text="Threshold")
        self.label_i = Label(self.master, text="Searching for image at '{}'".format(REFERENCE_PATH))
        self.label_x.grid(row=0, column=0)
        self.label_y.grid(row=1, column=0)
        self.label_w.grid(row=2, column=0)
        self.label_h.grid(row=3, column=0)
        self.label_t.grid(row=4, column=0)
        self.label_i.grid(row=5, column=0, columnspan=2, ipadx=0, ipady=0, padx=0, pady=0)
        
        # Build sliders.
        limit_left   = self.monitor[0]['left']
        limit_right  = limit_left + self.monitor[0]['width']
        limit_top    = self.monitor[0]['top']
        limit_bottom = limit_top + self.monitor[0]['height']
        self.slider_x = Scale(self.master, length=400, from_=limit_left, to=limit_right,  orient=HORIZONTAL, command=self._update_vars_x)
        self.slider_y = Scale(self.master, length=400, from_=limit_top,  to=limit_bottom, orient=HORIZONTAL, command=self._update_vars_y)
        self.slider_w = Scale(self.master, length=400, from_=1, to=1000, orient=HORIZONTAL, command=self._update_vars_w)
        self.slider_h = Scale(self.master, length=400, from_=1, to=1000, orient=HORIZONTAL, command=self._update_vars_h)
        self.slider_t = Scale(self.master, length=400, from_=0, to=1,    orient=HORIZONTAL, command=self._update_vars_t, resolution=0.01)
        self.slider_x.grid(row=0, column=1)
        self.slider_y.grid(row=1, column=1)
        self.slider_w.grid(row=2, column=1)
        self.slider_h.grid(row=3, column=1)
        self.slider_t.grid(row=4, column=1)

        # Setup label for image.
        self.label_image = Label(self.master)
        self.label_image.grid(row=0, column=3, rowspan=4)
        self._update_image() # Update image.

        self.slider_x.set(self.window_x)
        self.slider_y.set(self.window_y)
        self.slider_w.set(self.window_w)
        self.slider_h.set(self.window_h)
        self.slider_t.set(self.window_t)

    def _update_image(self):
        # exec_start = time.time()       

        with mss.mss() as screenshot:
            monitor = {"left": self.window_x, "top": self.window_y, "width": self.window_w, "height": self.window_h}
            img = screenshot.grab(monitor)
            img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            img = ImageTk.PhotoImage(img)
            self.label_image.configure(image=img)
            self.label_image.image = img

        # print(time.time() - exec_start) # Time critical component.

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
    def _update_vars_t(self, value):
        self.window_t = float(value)
    
    def _exit_program(self):
        exit()

    def _process_image(self, root, delay):
        # exec_start = time.time()
        with mss.mss() as screenshot:
            monitor = {"left": self.window_x, "top": self.window_y, "width": self.window_w, "height": self.window_h}
            img = screenshot.grab(monitor)

        img_rgb = np.array(img) 

        # Set up base image to look at.
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Match.
        res = cv2.matchTemplate(img_gray, REFERENCE_IMG, cv2.TM_CCOEFF_NORMED)
        threshold = self.window_t
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + REFERENCE_W, pt[1] + REFERENCE_H), (0, 0, 255), 2)

        if loc[0].size > 0:
            if not self.alerted:
                self.alerted = True
                playsound(r'sounds\beep2.wav', False)
        else:
            self.alerted = False

        # Uncomment to capture ot file.
        # cv2.imwrite('result.png', img_rgb)

        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(img_rgb)
        img = ImageTk.PhotoImage(img)
        self.label_image.configure(image=img)
        self.label_image.image = img

        # print(time.time() - exec_start)
        root.after(delay, self._process_image, root, delay) # Reschedule.

def main():
    root = Tk()
    app = Window(root)
    timeout = 50 # Refresh delay in ms.
    root.after(timeout, app._process_image, root, timeout)

    root.mainloop()  

if __name__ == "__main__":
    main()
