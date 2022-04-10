import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *


class Application(Frame):
    """
    一个经典的GUI程序的类的写法
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        # 新建主菜单栏
        mainmenu = Menu(root)

        # 创建子菜单栏
        menuFile = Menu(mainmenu)
        menuEdit = Menu(mainmenu)
        menuHelp = Menu(mainmenu)

        # 将子菜单加入到主菜单栏
        mainmenu.add_cascade(label="File", menu=menuFile)
        mainmenu.add_cascade(label="Eidt", menu=menuEdit)
        mainmenu.add_cascade(label="Help", menu=menuHelp)

        # 添加菜单项
        menuFile.add_command(label='new', command=self.myreact)
        menuFile.add_command(label='open', command=self.openfile)
        menuFile.add_command(label='save', command=self.savefile)
        menuFile.add_separator()
        menuFile.add_command(label='quit', command=self.exit)

        menuEdit.add_command(label='add', command=self.add_attribute)
        menuEdit.add_command(label='delete', command=self.delete_attribute)
        menuEdit.add_command(label='modify', command=self.modify_attribute)
        menuEdit.add_command(label='show', command=self.show_attribute)
        # menuEdit.add_command(label="reset_attr", command=self.reset_attribute)
        menuEdit.add_command(label='drawpicture', command=self.drawpicture)

        menuHelp.add_command(label="advice", command=self.myadvice)

        # 将主菜单栏加到根窗口
        root["menu"] = mainmenu

        # 显示当前文件名字
        self.attr_name_label = Label(self, text="curr_name's name")
        self.attr_name_label.pack(side=TOP)
        self.var_name = StringVar()
        self.var_name = Entry(self, textvariable=self.var_name)
        self.var_name.pack(side=TOP)


        # attribute's name
        self.attr_name_label = Label(self, text="attribute's name")
        self.attr_name_label.pack(side=LEFT)
        var1 = StringVar()
        self.attr_name_entry = Entry(self, textvariable=var1)
        self.attr_name_entry.pack(side=LEFT)

        # attribute's value
        self.attr_value_label = Label(self, text="attribute's value")
        self.attr_value_label.pack(side=LEFT)
        var2 = StringVar()
        self.attr_value_entry = Entry(self, textvariable=var2)
        self.attr_value_entry.pack(side=LEFT)

        # 将reset_attr按钮移动到新的位置，方便操作，这个按钮有点丑啊
        self.button_reset = Button(self, text="reset_attribute", command=self.reset_attribute)
        self.button_reset.pack(side=RIGHT)

        # 文本编辑区
        self.textpad1 = Text(root, width=40, height=30, state="normal")
        self.textpad1.pack(side=LEFT)

        self.textpad2 = Text(root, width=40, height=30, state="normal")
        self.textpad2.pack(side=RIGHT)

        # 创建上下菜单，想借此实现跳转上一个或下一个文件，但是实现有难度
        # 思路，直接将所有文件的路径存入队列，之后访问队列
        self.contextMenu = Menu(root)
        self.contextMenu.add_command(label="the previous", command=self.previous_file)
        self.contextMenu.add_command(label="the next", command=self.next_file)

        # 为右键绑定事件
        root.bind("<Button-3>", self.createContextMenu)

    # 与各个事件相关联的方法
    # methods of menuFile
    def openfile(self):
        # 每次打开一个新文件都要清空textpad1的内容
        self.textpad1.config(state="normal")
        self.textpad1.delete("1.0", "end")
        # 每次打开一个新文件都要清空textpad2的内容
        self.textpad2.config(state="normal")
        self.textpad2.delete("1.0", "end")

        with askopenfile(title="open files") as f:
            # previous和next还是在这个文件夹下完成的，所以这个属性不需要需要修改
            self.txt_file_path = os.path.split(f.name)[0]
            self.txt_file_name = os.path.split(f.name)[1]
            txt_file_path_split = self.txt_file_path[:-6]
            txt_file_name_split = self.txt_file_name[:-4]
            # print(txt_file_path_split)
            print("************************curr_file************************")
            print("openfile: ")
            print(self.txt_file_name)

            # 对于previous和next需要修改json文件的地址，因为每次都在变化嘛
            json_file_temp_path = os.path.join(txt_file_path_split, 'Attributes/')
            self.json_file_path = os.path.join(json_file_temp_path, txt_file_name_split + '.json')
            # print(self.json_file_path)

            self.textpad1.insert(INSERT, f.read())
            # 使得textpad1里的内容不可修改
            self.textpad1.config(state="disabled")
            # 这个属性存的是当前文件的绝对路径，后续的previous和next都要对其进行修改
            # 其只影响save和drawpicture
            self.filepath = f.name
            print(f.name)

    def savefile(self):
        print("savefile: ")
        with open(self.filepath, 'w') as f:
            filecontent = self.textpad1.get(1.0, END)
            # 避免save后在文本末尾追加空行
            # print(type(filecontent[:-1]))
            f.write(filecontent[:-1])

    def myreact(self):
        messagebox.showinfo("Message", "this func can't use")

    def exit(self):
        root.quit()

    # methods of menuEdit
    # 增
    def add_attribute(self):
        print("add: ")
        if os.access(self.json_file_path, os.F_OK):
            with open(self.json_file_path, 'r', encoding='utf-8') as load_f:
                load_dict = json.load(load_f)
                # dict_pre = '='.join([self.attr_name_entry.get(), self.attr_value_entry.get()])
                # 避免添加空白字典对象进json文件
                if len(self.attr_name_entry.get()) == 0:
                    pass

                elif len(self.attr_name_entry.get()) >= 1:
                    dict_pre = dict()
                    # print(type(self.attr_name_entry.get()))
                    dict_pre[self.attr_name_entry.get()] = self.attr_value_entry.get()
                    load_dict.update(dict_pre)
                    # print(load_dict)

            with open(self.json_file_path, 'w', encoding='utf-8') as dump_f:
                json.dump(load_dict, dump_f, ensure_ascii=False)
        else:
            print('未找到文件')

    # 删
    def delete_attribute(self):
        print("delete: ")
        if os.access(self.json_file_path, os.F_OK):
            with open(self.json_file_path, 'r', encoding='utf-8') as load_f:
                load_dict = json.load(load_f)
                # print(load_dict)

                del load_dict[self.attr_name_entry.get()]
                # print(load_dict)
            with open(self.json_file_path, 'w', encoding='utf-8') as dump_f:
                json.dump(load_dict, dump_f, ensure_ascii=False)
        else:
            print('未找到文件')

    # 改
    def modify_attribute(self):
        print("modify: ")
        if os.access(self.json_file_path, os.F_OK):
            with open(self.json_file_path, 'r', encoding='utf-8') as load_f:
                load_dict = json.load(load_f)

                if self.attr_name_entry.get() in load_dict.keys():
                    load_dict[self.attr_name_entry.get()] = self.attr_value_entry.get()

                else:
                    messagebox.showinfo("Message", "the attribute is False")
            with open(self.json_file_path, 'w', encoding='utf-8') as dump_f:
                json.dump(load_dict, dump_f, ensure_ascii=False)
        else:
            print('未找到文件')

    # 查
    def show_attribute(self):
        print("show: ")
        # 再次show之前要清空textpad2的内容
        self.textpad2.config(state="normal")
        self.textpad2.delete("1.0", "end")
        if os.access(self.json_file_path, os.F_OK):
            with open(self.json_file_path, 'r', encoding='utf-8') as load_f:
                load_dict = json.load(load_f)
                for key, value in load_dict.items():
                    # print(key, value)
                    self.textpad2.insert(INSERT, key)
                    self.textpad2.insert(INSERT, ": ")
                    self.textpad2.insert(INSERT, value)
                    self.textpad2.insert(INSERT, "\n")
                # 使得textpad2里的内容不可修改
                self.textpad2.config(state="disabled")

        else:
            print('未找到文件')

    # 重置attribute的输入，以便重新输入新的值
    def reset_attribute(self):
        self.attr_name_entry.delete(0, 'end')
        self.attr_value_entry.delete(0, 'end')

    # 绘制波形图
    def drawpicture(self):
        value = np.loadtxt(self.filepath)
        y = value
        x = range(len(y))
        plt.plot(y)
        plt.show()

    # methods of menuHelp
    def myadvice(self):
        messagebox.showinfo("Message", "Place call 18383827268")

    # methods of submenu
    def createContextMenu(self, event):
        # 菜单在鼠标右键单击的座标处显示
        self.contextMenu.post(event.x_root, event.y_root)

    def previous_file(self):
        # 每次打开一个新文件都要清空textpad1的内容
        self.textpad1.config(state="normal")
        self.textpad1.delete("1.0", "end")
        # 每次打开一个新文件都要清空textpad2的内容
        self.textpad2.config(state="normal")
        self.textpad2.delete("1.0", "end")

        file_list = os.listdir(self.txt_file_path)
        curr_file_index = file_list.index(self.txt_file_name)
        print(self.txt_file_path)
        print(self.txt_file_name)
        previous_file_path = os.path.join(self.txt_file_path, file_list[curr_file_index - 1])
        # 可以用此方法解决路径问题
        previous_file_path = '/'.join(previous_file_path.split('\\'))
        print(previous_file_path)
        with open(previous_file_path, 'r') as f:
            self.textpad1.insert(INSERT, f.read())
            # 使得textpad1里的内容不可修改
            self.textpad1.config(state="disabled")
            self.txt_file_name = file_list[curr_file_index - 1]
            self.filepath = f.name
            print(self.filepath)

            txt_file_path_split_previous = self.txt_file_path[:-6]
            txt_file_name_split_previous = self.txt_file_name[:-4]
            json_file_temp_path = os.path.join(txt_file_path_split_previous, 'Attributes/')
            self.json_file_path = os.path.join(json_file_temp_path, txt_file_name_split_previous + '.json')

    def next_file(self):
        # 每次打开一个新文件都要清空textpad1的内容
        self.textpad1.config(state="normal")
        self.textpad1.delete("1.0", "end")
        # 每次打开一个新文件都要清空textpad2的内容
        self.textpad2.config(state="normal")
        self.textpad2.delete("1.0", "end")

        file_list = os.listdir(self.txt_file_path)
        curr_file_index = file_list.index(self.txt_file_name)
        print(self.txt_file_path)
        print(self.txt_file_name)
        previous_file_path = os.path.join(self.txt_file_path, file_list[curr_file_index + 1])
        # 可以用此方法解决路径问题
        previous_file_path = '/'.join(previous_file_path.split('\\'))
        print(previous_file_path)
        with open(previous_file_path, 'r') as f:
            self.textpad1.insert(INSERT, f.read())
            # 使得textpad1里的内容不可修改
            self.textpad1.config(state="disabled")
            self.txt_file_name = file_list[curr_file_index + 1]
            self.filepath = f.name
            print(self.filepath)

            txt_file_path_split_next = self.txt_file_path[:-6]
            txt_file_name_split_next = self.txt_file_name[:-4]
            json_file_temp_path = os.path.join(txt_file_path_split_next, 'Attributes/')
            self.json_file_path = os.path.join(json_file_temp_path, txt_file_name_split_next + '.json')


if __name__ == '__main__':
    root = Tk()
    root.title('my first Gui')
    root.geometry('600x500+100+200')
    app = Application(master=root)
    root.mainloop()
