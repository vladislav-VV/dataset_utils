import os
import glob
import shutil
import argparse

def copy(args):
    if (args.list_images == None) | (args.save_dir == None):
        print(f"--list_imagesis {args.in_dir} --save_dir is {args.save_dir}")
        exit()

    with open(args.list_images, "r") as f:
        for i, path_image in enumerate(f):
            path_image = path_image.strip("\n")
            path_ann = path_image.replace("jpg", "txt")
            name_image = os.path.basename(path_image)
            name_ann = os.path.basename(path_image).replace("jpg", "txt")
            path_save_image = os.path.join(args.save_dir, name_image)
            path_save_ann = os.path.join(args.save_dir, name_ann)


            shutil.copyfile(path_image, path_save_image)
            shutil.copyfile(path_ann, path_save_ann)
            print(f"{i} from {len(args.list_images) - 1}")



def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--list_images", default=r"C:\kovalevvladislav\__list__\--Record\--ARC\TP\Оценки_точности_TP_20_12_2022\val_list.txt")
    args.add_argument("--save_dir", default=r"\\unit32stend2\exchange2\Dataset\ARC\TP\Augmentation_DG_19_12_2022\val\res")
    return args.parse_args()

if __name__ == "__main__":
    args = opt()
    copy(args)

