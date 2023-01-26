
# -------------------------
#
#      python script
#      Kovalev V.V.
#      Date __.__.____
#
# -------------------------
import os
import tqdm
import glob
import argparse
import shutil

def main(args):
    with open(args.dir, 'r') as f:
        image_list = f.read().splitlines()
    for  path in tqdm.tqdm(image_list):
        bytes_size = os.path.getsize(path)
        if bytes_size == 0:
            print(path)




def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--dir", type=str, default=r"E:\codepy\UTILS\generate-list-path_im-train\DG.txt")
    return args.parse_args()


if __name__ == "__main__":
    args = opt()
    main(args)