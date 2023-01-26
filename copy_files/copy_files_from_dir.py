
import os
import glob
import shutil
import argparse

def copy(args):
    if (args.in_dir == None) | (args.save_dir == None):
        print(f"--in_dir is {args.in_dir} --save_dir is {args.save_dir}")
        exit()

    paths = glob.glob(os.path.join(args.in_dir, "*." + args.suf))
    for i, path in enumerate(paths):
        shutil.copyfile(path, os.path.join(args.save_dir, os.path.basename(path)))
        print(f"{i} from {len(paths) - 1}")



def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--in_dir", default=r"D:\Dataset\OPEN_DATASET\VOC\VOC2012\Ann_txt")
    args.add_argument("--save_dir", default=r"\\unit32stend2\exchange2\Dataset\ARC\TV\OPEN_DATASET\COCO\val2017")
    args.add_argument("--suf", default="txt")
    return args.parse_args()

if __name__ == "__main__":
    args = opt()
    copy(args)