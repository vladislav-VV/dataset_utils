import os
import cv2
import glob
import argparse


def convert(args):
    paths_ann = glob.glob(os.path.join(args.dir_in_an, "*.txt"))
    for i, path_ann in enumerate(paths_ann):
        print(f"{i} from {len(paths_ann)}")
        path_im = os.path.join(args.dir_in_im, os.path.basename(path_ann).replace("txt", "jpg"))
        image = cv2.imread(path_im)
        width = image.shape[1]
        height = image.shape[0]

        path_ann_write = os.path.join(args.dir_out, os.path.basename(path_ann))

        with open(path_ann, "r") as f,\
             open(path_ann_write, "w") as g:
            for line in f:
                words = line.split(",")

                box_x = int(words[2]) / width
                box_y = int(words[3]) / height

                center_x = int(words[0]) / width + box_x / 2
                center_y = int(words[1]) / height + box_y / 2

                if words[4] == '0':  # VisDrone 'ignored regions' class 0
                    continue
                cls = int(words[5]) - 1
                if cls >= 1:
                    cls -= 1


                g.write(f"{cls} {center_x} {center_y} {box_x} {box_y}\n")




    pass


def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--dir_in_an", type=str, default=r"/media/vladislav/MailBox/DATASET/VisDrone2019/VisDrone2019-DET-val/VisDrone2019-DET-val/annotations")
    args.add_argument("--dir_in_im", type=str, default=r"//media/vladislav/MailBox/DATASET/VisDrone2019/VisDrone2019-DET-val/VisDrone2019-DET-val/images")
    args.add_argument("--dir_out", type=str, default=r"/media/vladislav/MailBox/DATASET/VisDrone2019/VisDrone2019-DET-val/VisDrone2019-DET-val/images")
    return args.parse_args()

if __name__ == "__main__":
    args = opt()
    convert(args)