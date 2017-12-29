import os


def visit_directory(path, file_name):
    dirs = os.listdir(path)
    for dir in dirs:
        sub_path = os.path.join(path, dir)
        if dir == file_name and os.path.isfile(sub_path):
            os.remove(sub_path)
            return True
        elif os.path.isdir(sub_path):
            visit_directory(sub_path, file_name)
