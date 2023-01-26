# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 19.01.2023
#                         
# -------------------------

import os
import cv2
import glob
import numpy as np
from typing import Union




class PrintDetect:


    def __init__(self, dir_im: str, dir_ann: str, type_ann: int = 0, threshold_conf: float = 0):
        """
        :param path_im: путь к директории с изображениями
        :param path_txt: путь к директории с аннотациями
        :param flag_draw: 0 - верхний левый угол и нижний правый
                          1 - нормированные центр и обрамляющий приямоугольник
        """
        self.names_txt = glob.glob(os.path.join(dir_ann, "*.txt"))
        self.path_im = dir_im
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.flag_draw = type_ann
        self.threshold_conf = threshold_conf




    def __iter__(self) -> Union[np.ndarray, list]:
        for i, name_txt in enumerate(self.names_txt):
            if os.path.exists(os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "jpg")):
                image_path = os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "jpg")
            elif os.path.exists(os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "png")):
                image_path = os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "png")
            elif os.path.exists(os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "bmp")):
                image_path = os.path.join(self.path_im, os.path.basename(name_txt)[:-3] + "bmp")
            else:
                print(f"{i} files not exist {name_txt}")
                continue
            print(f"{i} files exist {name_txt}")
            image    = cv2.imread(image_path)

            with open(name_txt, "r") as file_ann:
                detections = []
                if self.flag_draw == 0:
                    detections += self.read_flag_draw_0(file_ann)
                if self.flag_draw == 1:
                    width = image.shape[0]
                    height = image.shape[1]
                    detections += self.read_flag_draw_1(file_ann, width, height)

            yield image, detections




    def read_flag_draw_0(self, file_ann):
        detections = []
        for line in file_ann:
            words   = line.split()
            if self.threshold_conf == 0:
                N_class = int(words[0])
                conf    = 1
                xmin    = int(words[1])
                ymin    = int(words[2])
                xmax    = int(words[3])
                ymax    = int(words[4])
            else:
                N_class = int(words[0])
                conf  = float(words[1])
                xmin    = int(words[2])
                ymin    = int(words[3])
                xmax    = int(words[4])
                ymax    = int(words[5])

            if conf > self.threshold_conf:
                detections.append([N_class, xmin, ymin, xmax, ymax])

        return detections




    def read_flag_draw_1(self, file_ann, width, height):
        detections = []
        for line in file_ann:
            words   = line.split()
            if self.threshold_conf == 0:
                #-----------------------------------
                # Детекциии с уверенностью алгоритма
                #-----------------------------------
                N_class = words[0]
                conf    = 1
                # conf = float(words[1])
                center_x = float(words[1])
                center_y = float(words[2])
                box_x    = float(words[3])
                box_y    = float(words[4])
                xmin     = int((center_x - box_x / 2) * height)
                ymin     = int((center_y - box_y / 2) * width)
                xmax     = int((center_x + box_x / 2) * height)
                ymax     = int((center_y + box_y / 2) * width)
            else:
                #-------------------------
                # Разметка без уверенности
                #-------------------------
                N_class = words[0]
                conf = float(words[1])
                center_x = float(words[2])
                center_y = float(words[3])
                box_x    = float(words[4])
                box_y    = float(words[5])
                xmin     = int((center_x - box_x / 2) * height)
                ymin     = int((center_y - box_y / 2) * width)
                xmax     = int((center_x + box_x / 2) * height)
                ymax     = int((center_y + box_y / 2) * width)

            if conf > self.threshold_conf:
                detections.append([N_class, xmin, ymin, xmax, ymax])

        return detections




def draw_detections(image: np.ndarray, detections: list) -> np.ndarray:
    for det in detections:
        N_class = det[0]
        xmin = det[1]
        ymin = det[2]
        xmax = det[3]
        ymax = det[4]
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
        cv2.putText(image, "{}".format(N_class), (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
    return image