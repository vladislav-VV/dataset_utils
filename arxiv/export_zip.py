import os
import sys
import zipfile
import argparse
import datetime



def opt():
    args = argparse.ArgumentParser()
    args.add_argument("--data_list", default=r'/home/vladislav/Projects/Python/dataset_utils/arxiv/test.txt')
    args.add_argument("--arxiv_name", default="coco_val")
    return args.parse_args()


def fun_create_dir() -> str:
    # datetime_now = datetime.datetime.now()
    # datetime_now_str = f"{datetime_now.year}-{datetime_now.month}-{datetime_now.day}-{datetime_now.hour}-{datetime_now.minute}-{datetime_now.second}"
    datetime_now_str = f'{datetime.datetime.now():"%y-%m-%d_%H-%M-%S"}'
    datetime_now_str = datetime_now_str[1:-1]
    create_dir = os.path.join(os.getcwd(), "backup", datetime_now_str)
    os.mkdir(create_dir)
    return create_dir

def get_paths_from_list(path_to_list: str) -> list:
    with open(path_to_list, "r") as files:
        paths = list(map(lambda x: x.strip(), files.readlines()))
    return paths

def main(data_list: str, arxiv_name: str):

    create_dir = fun_create_dir()
    paths = get_paths_from_list(data_list)
    len_paths = len(paths)

    with zipfile.ZipFile(os.path.join(create_dir, f"{arxiv_name}.zip"), 'w') as zip_arxiv,\
        open(os.path.join(create_dir, "warning.list"), 'w') as warning_list:

        for i, path2image in enumerate(paths):
            sys.stdout.write("\r " + f"{i} from {len_paths}")
            path2ann = path2image[:-3] + "txt"
            if os.path.exists(path2image) & os.path.exists(path2ann):
                bytes_size_image = os.path.getsize(path2image)
                bytes_size_ann = os.path.getsize(path2ann)
                if (bytes_size_image != 0) & (bytes_size_ann != 0):
                    zip_arxiv.write(path2image, path2image, compress_type=zipfile.ZIP_DEFLATED)
                    zip_arxiv.write(path2ann, path2ann, compress_type=zipfile.ZIP_DEFLATED)
                else:
                    warning_list.write(f"file bytes is zero {bytes_size_image}\n")
            else:
                warning_list.write(f"file not exist {bytes_size_image}\n")



if __name__ == "__main__":
    args = opt()
    main(data_list=args.data_list, arxiv_name=args.arxiv_name)