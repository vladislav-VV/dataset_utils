# -------------------------
#                         
#      python script      
#      Kovalev V.V.
#      Date 18.01.2023
#                         
# -------------------------
import os
import random
import argparse
from datetime import datetime



def fun_create_dir() -> str:
    datetime_now =  datetime.now()
    datetime_now_str =  f"{datetime_now.second}_{datetime_now.minute}_{datetime_now.hour}_{datetime_now.day}_{datetime_now.month}_{datetime_now.year}"
    create_dir = os.path.join(os.getcwd(), "backup", datetime_now_str)
    os.mkdir(create_dir)
    return create_dir


def main(args):

    create_dir = fun_create_dir()
    f = open(args.path_to_file, "r")
    paths = f.read().split("\n")
    random.shuffle(paths)
    res_path = paths[:int(len(paths) * args.k)]

    with open(os.path.join(create_dir, os.path.basename(args.path_to_file)), "w") as fw:
        for line in res_path:
            fw.write(line + "\n")

    print("End!")


def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--path_to_file", default=r"\\unit32stend2\Exchange\Kovalev\ARC\train.txt", type=str)
    args.add_argument("--k", default=0.25, type=float)
    return args.parse_args()



if __name__ == "__main__":
    args = opt()
    main(args)