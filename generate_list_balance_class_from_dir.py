# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 23.08.2022
#                         
# -------------------------
import cv2
import os
import glob
import argparse
import random
import numpy as np



def get_list_names(file):
    names = []
    with open(file, "r") as f:
        for name in f:
            names.append(name.rstrip())
    return names

def main(args):
    names = get_list_names(args.file_names)
    nc_all = len(names)

    annotations = glob.glob(os.path.join(args.dir_annotation, "*.txt"))
    random.shuffle(annotations)
    statostic = [0 for _ in range(nc_all)]
    statostic = np.array(statostic)
    paths = []
    for i, ann in enumerate(annotations):
        print(f"{i} {ann}")
        stat = [0 for _ in range(nc_all)]
        with open(ann, "r") as f:
            for line in f:
                words = line.split()
                nc = int(words[0])
                stat[nc] = stat[nc] + 1
        flag = True
        for nc in range(nc_all):
            if stat[nc] +  statostic[nc] > args.threshold_obj_count:
                flag = False
        if flag:
            statostic +=   np.array(stat)
            paths.append(ann)
                # statostic[nc].add_count()

    with open(os.path.join(os.getcwd(), "val_list.txt"), "w") as fw:
        for path in paths:
            fw.write(path.replace("txt", "jpg") + "\n")




def options():
    args = argparse.ArgumentParser()
    args.add_argument("--dir_annotation", type=str, default=r"\\unit32stend2\exchange2\Dataset\ARC\TP\Augmentation_DG_19_12_2022\val\Output_Train_d\output_20")
    args.add_argument("--file_names", type=str, default=r"E:\codepy\UTILS\dataset_utils\names.names")
    args.add_argument("--threshold_obj_count", type=int, default=500)

    return args.parse_args()


if __name__ == "__main__":
    args = options()
    main(args)