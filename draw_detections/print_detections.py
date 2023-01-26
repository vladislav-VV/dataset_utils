# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 13.01.2023
#                         
# -------------------------

import cv2
import argparse
from utils import PrintDetect
from utils import draw_detections




def main(dir_im, dir_ann, type_ann, threshold_conf):

    print_detect = PrintDetect(dir_im=dir_im,
                               dir_ann=dir_ann,
                               type_ann=type_ann,
                               threshold_conf=threshold_conf)

    for image, detections in print_detect:
        image = draw_detections(image, detections)
        cv2.imshow("image", image)
        cv2.waitKey()




def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--dir_im", type=str, default=r"D:\save_image", help="директория с изображениями")
    args.add_argument("--dir_ann", type=str, default=r"D:\save_image", help="директория с аннотациями")
    args.add_argument("--threshold_conf", type=float, default=0.0, help="порог уверенности алгоритма")
    args.add_argument("--type_ann", type=int, default=1, help="0 - верхний левый угол и нижний правый;\
                                                               1 - нормированные центр и обрамляющий приямоугольн")
    return args.parse_args()




if __name__ == "__main__":
    args = opt()
    main(dir_im=args.dir_im,
         dir_ann=args.dir_ann,
         type_ann=args.type_ann,
         threshold_conf=args.threshold_conf)