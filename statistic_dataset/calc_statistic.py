# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 25.01.2023
#                         
# -------------------------

import os
import glob
import tqdm
import argparse
import matplotlib.pyplot as plt


class ReaderAnnYolo:

    def __init__(self, path_ann: str) -> None:
        self.file = open(path_ann, "r")




    def __call__(self, *args, **kwargs):
        """
        :return nc, center_x, center_y, box_x, box_y
        """
        for line in self.file:
            words = line.split()
            nc = int(words[0])
            center_x = float(words[1])
            center_y = float(words[2])
            box_x = float(words[3])
            box_y = float(words[4])

            yield nc, center_x, center_y, box_x, box_y



def plot(a):
    plt.bar(range(len(a)), list(a.values()), align='center')
    plt.xticks(range(len(a)), list(a.keys()))
    plt.grid()
    plt.show()
    print(4)




def calc_statistic(dir_ann):

    statistic = {}

    paths_ann = glob.glob(os.path.join(dir_ann, "*.txt"))

    for path_ann in tqdm.tqdm(paths_ann):

        reader_ann_yolo = ReaderAnnYolo(path_ann)

        for nc , center_x, center_y, box_x, box_y in reader_ann_yolo():
            nc_str = str(nc)
            if not nc in statistic:
                statistic[nc] = 1
            else:
                statistic[nc] += 1

    plot(statistic)



def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--dir_ann", type=str, default=r"D:\Dataset\OPEN_DATASET\COCO\val2017")
    return args.parse_args()




if __name__ == "__main__":

    args = opt()

    calc_statistic(dir_ann=args.dir_ann)
