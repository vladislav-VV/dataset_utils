# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 12.01.2023
#
# -------------------------

import os
# import cv2
# import tqdm
import glob
import argparse
from datetime import datetime




def get_list_annotations(directory: list, sufffix: list) -> list:
    annotations_count = []
    for direct in directory:
        iter_dir = os.walk(direct)
        for dir in iter_dir:
            for suf in sufffix:
                annotations_count += glob.glob(os.path.join(dir[0], f"*.{suf}"))
    return annotations_count




def fun_create_dir() -> str:
    datetime_now =  datetime.now()
    datetime_now_str =  f"{datetime_now.second}_{datetime_now.minute}_{datetime_now.hour}_{datetime_now.day}_{datetime_now.month}_{datetime_now.year}"
    create_dir = os.path.join(os.getcwd(), "backup", datetime_now_str)
    os.mkdir(create_dir)
    return create_dir




def check(args):

    create_dir = fun_create_dir()

    list_images = get_list_annotations(args.in_dir, args.suffix)


    with open(os.path.join(create_dir, "train.txt"), "w") as f, \
         open(os.path.join(create_dir, "test.txt"), "w") as g, \
         open(os.path.join(create_dir, "warning.txt"), "w") as warning_file:
        for i, path2image in enumerate(list_images):
            words_ann = path2image.split(".")
            suf_im = words_ann[-1]
            path2ann = path2image.replace(suf_im, "txt")
            # frame = cv2.imread(path2image)
            if (os.path.exists(path2image)) & (os.path.exists(path2ann)):
                bytes_size_im = os.path.getsize(path2image)
                bytes_size_txt = os.path.getsize(path2ann)
                if (bytes_size_im == 0) | (bytes_size_txt == 0):
                    warning_file.write(f"{path2image}\n")
                elif i < len(list_images) * args.threshold:
                    f.write(f"{path2image}\n")
                else:
                    g.write(f"{path2image}\n")

            else:
                warning_file.write(f"Not exist {path2image}\n")


            print(f"{i} from {len(list_images)}")
    print("End")




def opt():

    args = argparse.ArgumentParser()
    args.add_argument("--in_dir", type=str, default=[
                      r"/home/vladislav/Data/coco/train2017"]
                      )

    # args.add_argument("--in_dir", type=str, default=[r'\\unit32stend2\exchange2\Dataset\ARC\TV\Validations',
    #                                                  r"\\unit32stend2\exchange2\Dataset\ARC\TV\OPEN_DATASET\COCO\val2017",
    #                                                  r"\\unit32stend2\exchange2\Dataset\ARC\TV\OPEN_DATASET\VOC2012"])


    args.add_argument("--threshold", type=float, default=0.0)
    args.add_argument("--suffix", type=list, default=["png", "jpg", "bmp"])

    return args.parse_args()




if __name__ == "__main__":
    args = opt()
    check(args)