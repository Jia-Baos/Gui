import os
import json


def get_attribute(path):
    if os.access(path, os.F_OK):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(type(load_dict))
            print(load_dict)
            for key, value in load_dict.items():
                print(key, value)

    else:
        print('未找到文件')


if __name__ == '__main__':
    path = "D:\\PythonProject\\Gui\\test1.json"
    get_attribute(path)
