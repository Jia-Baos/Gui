import os
import json


# 查
def find_attribute(path: str):
    print("find: ")
    if os.access(path, os.F_OK):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            # print(type(load_dict))
            # print(load_dict)
            for key, value in load_dict.items():
                print(key, value)
    else:
        print('未找到文件')


# 改
def modify_attribute(path: str, attr_name: str, attr_value: str):
    print("modify: ")
    if os.access(path, os.F_OK):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)

            print("before modify: ")
            print(load_dict)

            load_dict[attr_name] = attr_value

            print("after modify: ")
            print(load_dict)

        with open(path, 'w', encoding='utf-8') as dump_f:
            json.dump(load_dict, dump_f, ensure_ascii=False)
    else:
        print('未找到文件')


# 增
def add_attribute(path: str, **kwargs):
    print("add: ")
    if os.access(path, os.F_OK):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
            load_dict.update(kwargs)
            print(load_dict)

        with open(path, 'w', encoding='utf-8') as dump_f:
            json.dump(load_dict, dump_f, ensure_ascii=False)
    else:
        print('未找到文件')


# 删
def delete_attribute(path: str, attr_name: str):
    print("delete: ")
    if os.access(path, os.F_OK):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)

            del load_dict[attr_name]
            print(load_dict)
        with open(path, 'w', encoding='utf-8') as dump_f:
            json.dump(load_dict, dump_f, ensure_ascii=False)
    else:
        print('未找到文件')


if __name__ == '__main__':
    path = "D:\\PythonProject\\Gui\\Data\\Attributes"
    for item in os.listdir(path):
        print(item)
        item_path = os.path.join(path, item)
        print(item_path)

        # 查
        find_attribute(item_path)

        # 改
        modify_attribute(item_path, attr_name='cls', attr_value='123')

        # 增
        add_attribute(item_path, temperature=35)

        # 删
        delete_attribute(item_path, attr_name='temperature')

        # 增
        add_attribute(item_path, temperature=60)
