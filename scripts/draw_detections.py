import os
import cv2
import glob
import tqdm
import random
import argparse
import numpy as np
from typing import Tuple

class GetDetections:

    def __init__(self, path_2dir_images: str, path_2dir_ann: str, mode: int = 0):
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.pick_mode(mode)
        self.suffixes = ["png", "jpg", "bmp"]
        self.paths2images = self.__get_paths_images(path_2dir_images)
        self.path_2dir_ann = path_2dir_ann




    def pick_mode(self, mode: int):
        if mode == 0:
            self.read_ann = self.read_box_mode_0
            print(f"You pick mode {mode}")
        elif mode == 1:
            self.read_ann = self.read_box_mode_1
            print(f"You pick mode {mode}")
        else:
            print(f"This pick mode {mode} not found!")




    def __get_paths_images(self, path_2dir_images: str) -> list:
        paths_to_images = []
        for suffix in self.suffixes:
            paths_to_images.extend(glob.glob(os.path.join(path_2dir_images, "*." + suffix)))

        return paths_to_images




    def read_box_mode_0(self, path2ann: str, width_image: int, height_image: int) -> list:
        detections = []
        with open(path2ann, "r") as f:
            for line in f:
                detection = dict()
                words = line.split()

                nc = int(words[0])
                center_x = float(words[1])
                center_y = float(words[2])
                box_x = float(words[3])
                box_y = float(words[4])

                detection["nc"] = nc
                detection["x1"] = int((center_x - box_x / 2) * width_image)
                detection["y1"] = int((center_y - box_y / 2) * height_image)
                detection["x2"] = int((center_x + box_x / 2) * width_image)
                detection["y2"] = int((center_y + box_y / 2) * height_image)
                detections.append(detection)

        return detections




    def read_box_mode_1(self, path2ann: str, width_image: int = None, height_image:int = None) -> list:
        detections = []
        with open(path2ann, "r") as f:
            for line in f:
                detection = dict()
                words = line.split()
                detection["nc"] = int(words[0])
                detection["x1"] = int(float(words[1]))
                detection["y1"] = int(float(words[2]))
                detection["x2"] = int(float(words[3]))
                detection["y2"] = int(float(words[4]))
                detections.append(detection)

        return detections




    def __call__(self) -> Tuple[np.ndarray, list]:
        for path2image in tqdm.tqdm(self.paths2images):
            name = os.path.basename(path2image)
            path2ann = os.path.join(self.path_2dir_ann, name[:len(name)-3] + "txt")
            if not os.path.exists(path2ann):
                print(f"File {path2ann} not exist!")
                continue
            image = cv2.imread(path2image)
            width_image = image.shape[1]
            height_image = image.shape[0]
            detections = self.read_ann(path2ann, width_image, height_image)
            yield image, detections




    def draw_detections(self, image: np.ndarray, detections: list) -> np.ndarray:
        for detection in detections:
            nc = str(detection["nc"],)
            pt0 = (detection["x1"], detection["y1"])
            pt1 = (detection["x2"], detection["y2"])
            color = tuple(random.randint(0, 255) for _ in range(3))
            image = cv2.rectangle(image, pt0, pt1, color, 1)
            image = cv2.putText(image, nc,  pt0, self.font, 0.5, color)

        return image




def main(args):

    get_detections = GetDetections(path_2dir_images=args.path_2dir_images,
                                   path_2dir_ann=args.path_2dir_ann,
                                   mode=args.mode)

    for image, detections in get_detections():
        image = get_detections.draw_detections(image, detections)
        cv2.imshow("image", image)
        cv2.waitKey()

def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--path_2dir_images", type=str, default=r"C:\DATASET\COCO\val2017", help="Path to directory with images")
    args.add_argument("--path_2dir_ann", type=str, default=r"H:\DATASET\COCO\coco2017labels\coco\labels\val2017", help="Path to directory with annotations")
    args.add_argument("--mode", type=int, default=0, help="mode 0 - format darknet; mode 1 - abs coord")

    return args.parse_args()

if __name__ == "__main__":
    args = opt()
    main(args)
