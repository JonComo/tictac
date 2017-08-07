import numpy as np
import cv2
import matplotlib.pyplot as plt

class Cam():
    def __init__(self, img_rows, img_cols):
        self.img_rows = img_rows
        self.img_cols = img_cols

    def get_k(self, k):
        # realtime board detection
        cam = cv2.VideoCapture(1)
        
        last_k = []
        
        while len(last_k) < k:
            ret_val, img = cam.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (int(img.shape[1]/9), int(img.shape[0]/9)))
            sr, sc = 22, 24
            img = img[sr:sr+self.img_rows, sc:sc+self.img_cols]
            
            # adaptive thresholding
            # http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 15)
            img = 255-img
            img = img.astype(np.float64)
            img /= 255
            
            last_k.append(img)
            
            if cv2.waitKey(1) == 27:
                return last_k
                break  # esc to quit

        return last_k
                
    def show_img(self, img, resize=True):
        print("show_img not pulling up window.. still working on that!")
        if resize:
            img = cv2.resize(img, (512, 512))
        
        cv2.startWindowThread()
        cv2.namedWindow("cam")
        cv2.imshow("cam", img)
        cv2.waitKey(1000)

    def destroy_windows(self):
        cv2.destroyAllWindows()