# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 11.01.2023
#
# -------------------------
import os
import cv2
import glob


def get_list_annotations(dirs: list, suffix: list) -> list:
    files = []
    i = 0
    for direct in dirs:
        iter_dir = os.walk(direct)
        for dir in iter_dir:
            for suf in suffix:
                files.extend(glob.glob(os.path.join(dir[0], f"*.{suf}")))
                print(f"{i}")
                i += 1
    return files

def i_to_str(i):
    str_i = str(i)
    while len(str_i) < 8:
        str_i = "0" + str_i
    return str_i

def convert():
    paths_images = get_list_annotations(path_dir_images, ["jpg"])
    for i, path in enumerate(paths_images):

        image = cv2.imread(path)
        name = os.path.basename(path)

        path_save = os.path.join(dir_save, name)

        if image is None:
            print(f"{i} {image} is None")
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path_save, image)
            print(f"{i} from {len(paths_images) - 1}")





if __name__ == "__main__":
    path_dir_images = [r"\\unit32stend2\exchange2\Dataset\ARC\TV\OPEN_DATASET\Wind\Windows"]
    dir_save = r"\\unit32stend2\exchange2\Dataset\ARC\TV\OPEN_DATASET\Wind\Windows"
    convert()