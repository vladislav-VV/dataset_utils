import os
import cv2
import glob
import argparse




class GetDetections:

    def __init__(self, path_2dir_images, path_2dir_ann, mode):
        self.pick_mode(mode)
        self.suffixes = ["png", "jpg", "bmp"]
        self.paths2images = self.__get_paths_images(path_2dir_images)
        self.path_2dir_ann = path_2dir_ann

    def pick_mode(self, mode):
        if mode == 0:
            self.read_ann = self.read_box_mode_0
            print(f"You pick mode {mode}")
        elif mode == 1:
            self.read_ann = self.read_box_mode_1
            print(f"You pick mode {mode}")
        else:
            print(f"This pick mode {mode} not found!")



    def read_box_mode_0(self, path2ann, width_image, height_image):
        """
        :return:
        """
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



    def __get_paths_images(self, path_2dir_images):
        paths_to_images = []
        for suffix in self.suffixes:
            paths_to_images.extend(glob.glob(os.path.join(path_2dir_images, "*." + suffix)))
        return paths_to_images

    def __call__(self):
        for path2image in self.paths2images:
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

        

    
def draw_detections(image, detections, color=(255, 0, 0), font=cv2.FONT_HERSHEY_COMPLEX):
    for detection in detections:
        nc = str(detection["nc"],)
        pt0 = (detection["x1"], detection["y1"])
        pt1 = (detection["x2"], detection["y2"])
        image = cv2.rectangle(image, pt0, pt1, color, 1)
        image = cv2.putText(image, nc,  pt0, font, 0.5, color)
    return image







def main(args):

    get_detections = GetDetections(path_2dir_images=args.path_2dir_images,
                                     path_2dir_ann=args.path_2dir_ann,
                                     mode=args.mode)

    for image, detections in get_detections():
        image = draw_detections(image, detections)
        cv2.imshow("image", image)
        cv2.waitKey()

def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--path_2dir_images", type=str, default=r"C:\DATASET\COCO\val2017", help="Path to directory with images")
    args.add_argument("--path_2dir_ann", type=str, default=r"H:\DATASET\COCO\coco2017labels\coco\labels\val2017", help="Path to directory with annotations")
    args.add_argument("--mode", type=int, default=0, help="modes 0 - norm_x, norm_y, norm_box_x, norm_box_y; 1 - left top, right bot")
    return args.parse_args()


if __name__ == "__main__":
    args = opt()
    main(args)
