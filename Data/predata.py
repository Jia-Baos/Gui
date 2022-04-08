import os
import json

images_path = "D:\\PythonProject\\Gui\\Data\\Images"
attributes_path = "D:\\PythonProject\\Gui\\Data\\Attributes"

for item in os.listdir(images_path):
    item_name = os.path.splitext(item)[0]
    print(item)
    print(item_name)

    json_path = os.path.join(attributes_path, item_name + '.json')
    file = open(json_path, 'w')

    test = {
        "name": "000001",
        "cls": "0 1",
        "avg": "2",
        "mse": "3"}

    jsondata = json.dumps(test, indent=4, separators=(',', ': '))

    file.write(jsondata)
    file.close()


