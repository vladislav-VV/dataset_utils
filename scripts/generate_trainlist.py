import os
import glob
import random
import argparse




class GenerateTrainList:
    def __init__(self, proc_k: str, shuffle: bool = False):
        self.suffix_image_format = ["bmp", "jpg", "png"]
        self.dir_save = os.path.join(os.getcwd(), "train_test")
        self.shuffle = shuffle
        self.proc_k = proc_k
        self.paths = []
        if not os.path.exists(self.dir_save):
            os.mkdir(self.dir_save)
        self.file_train = open(os.path.join(self.dir_save, "train.txt"), "w")
        self.file_test = open(os.path.join(self.dir_save, "test.txt"), "w")




    def __call__(self, directory: str):
        for suffix in self.suffix_image_format:
            self.paths.extend(glob.glob(os.path.join(directory, "*." + suffix)))




    def __del__(self):
        if self.shuffle:
            random.shuffle(self.paths)
        threshold = len(self.paths) * self.proc_k
        for i, path in enumerate(self.paths):
            if i < threshold:
                self.file_train.write(f"{path}\n")
            else:
                self.file_test.write(f"{path}\n")
            print(f"{i} {path}")
        self.file_test.close()
        self.file_train.close()




def generate(directories: list, proc_k: float, shuffle: bool):

    generate_train_list = GenerateTrainList(proc_k=proc_k,
                                            shuffle=shuffle)
    for direct in directories:
        generate_train_list(direct)




def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--directories", type=list, default=[r"/media/vladislav/Windows-SSD/DATASET/COCO/3_class/val"])
    args.add_argument("--proc_k", type=float, default=0.5)
    args.add_argument("--shuffle", type=bool, default=False)

    return args.parse_args()

if __name__ == "__main__":
    args = opt()
    generate(args.directories, args.proc_k, args.shuffle)