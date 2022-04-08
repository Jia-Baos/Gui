import os
import numpy as np
import matplotlib.pyplot as plt

data_path = "D:\\PythonProject\\Gui\\Data\\Images"

for item in os.listdir(data_path):
    item_path = os.path.join(data_path, item)
    value = np.loadtxt(item_path)
    y = value
    x = range(len(y))
    plt.plot(y)
    plt.show()
