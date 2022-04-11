import os
import json
import numpy as np
from time import sleep
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        # self.grid()
        self.createWidget()

    def createWidget(self):
        # 新建主菜单栏
        mainmenu = Menu(self.master)

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
        self.master["menu"] = mainmenu

        # 显示当前文件名字
        self.button_openfile = Button(self.master, text="open_file",
                                      command=lambda: [self.openfile(), self.show_attribute(), self.drawpicture()])
        self.button_openfile.grid(row=0, column=0, pady=2)
        self.button_quit = Button(self.master, text="quit", command=self.quit)
        self.button_quit.grid(row=0, column=1, pady=2)
        self.button_reset = Button(self.master, text="reset_attribute", command=self.reset_attribute)
        self.button_reset.grid(row=0, column=2, pady=2)

        # 将reset_attr按钮移动到新的位置，方便操作，这个按钮有点丑啊
        self.button_add = Button(self.master, text="add_attribute",
                                 command=lambda: [self.add_attribute(), self.show_attribute()])
        self.button_add.grid(row=1, column=0, pady=2)
        self.button_modify = Button(self.master, text="modify_attribute",
                                    command=lambda: [self.modify_attribute(), self.show_attribute()])
        self.button_modify.grid(row=1, column=1, pady=2)
        self.button_delete = Button(self.master, text="delete_attribute",
                                    command=lambda: [self.delete_attribute(), self.show_attribute()])
        self.button_delete.grid(row=1, column=2, pady=2)
        self.button_show = Button(self.master, text="show_attribute", command=self.show_attribute)
        self.button_show.grid(row=1, column=3, pady=2)
        self.button_draw = Button(self.master, text="draw_picture", command=self.drawpicture)
        self.button_draw.grid(row=1, column=4, pady=2)

        # 显示当前文件名字
        self.attr_name_label = Label(self.master, text="curr_file's name")
        self.attr_name_label.grid(row=2, column=0, pady=2)
        self.var_name_content = StringVar()
        self.var_name_content.set("no file")
        self.var_name = Label(self.master, textvariable=self.var_name_content,
                              fg='blue', font=('Helvetica', 12, 'bold'))
        self.var_name.grid(row=2, column=1, pady=2)

        # attribute's name
        self.attr_name_label = Label(self.master, text="attribute's name")
        self.attr_name_label.grid(row=3, column=0, pady=2)
        var1 = StringVar()
        self.attr_name_entry = Entry(self.master, textvariable=var1)
        self.attr_name_entry.grid(row=3, column=1, pady=2)

        # attribute's value
        self.attr_value_label = Label(self.master, text="attribute's value")
        self.attr_value_label.grid(row=3, column=2, pady=2)
        var2 = StringVar()
        self.attr_value_entry = Entry(self.master, textvariable=var2)
        self.attr_value_entry.grid(row=3, column=3, pady=2)

        # 条目框
        self.dirfm = Frame(self.master)  # 第一个Frame控件，一个包含其他控件的纯容器
        self.dirfm.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=NW, pady=10)
        # 在dirfm中pack()
        self.dirsb = Scrollbar(self.dirfm)  # 主要是提供滚动功能
        self.dirsb.pack(side=RIGHT, fill=Y)  # 滚动条靠右填充整个剩余空间
        self.dirs = Listbox(self.dirfm, width=15, height=22, yscrollcommand=self.dirsb.set)
        # 绑定操作。这意味着将一个回调函数与按键、鼠标操作或者其他的一些事件连接起来。这里当双击任意条目时，会调用openfile函数
        self.dirs.bind('<Double-1>', self.setDirAndGo)
        # 在dirfm中pack()
        self.dirsb.config(command=self.dirs.yview)  # 这里同列表控件的yscrollcommand回调结合起来
        self.dirs.pack(side=LEFT, fill=BOTH)

        # 构造函数最后一部分，用于初始化GUI程序，以当前工作目录作为起始点。
        self.cwd = StringVar(self.master)
        self.dirl = Label(self.master, fg='blue', font=('Helvetica', 12, 'bold'))
        self.dirl.grid(row=2, column=2, pady=2, columnspan=2)
        self.dirn = Entry(self.master, width=40, textvariable=self.cwd)
        self.dirn.grid(row=2, column=4, columnspan=2)
        self.doLS()

        # 文本编辑区
        self.textpad1 = Text(self.master, width=18, height=30, state="normal")
        self.textpad1.grid(row=4, column=1, rowspan=1, columnspan=1, sticky=NW, pady=10)

        self.textpad2 = Text(self.master, width=18, height=30, state="normal")
        self.textpad2.grid(row=4, column=2, rowspan=1, columnspan=1, sticky=NW, pady=10)

        # 波形显示区
        self.fig = Figure(figsize=(4, 2), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(row=4, column=3, rowspan=1, columnspan=5, sticky=NW, padx=5, pady=10)

        # 创建上下菜单，想借此实现跳转上一个或下一个文件，但是实现有难度
        # 思路，直接将所有文件的路径存入队列，之后访问队列
        self.contextMenu = Menu(self.master)
        # self.contextMenu.add_command(label="the previous", command=self.previous_file)
        # self.contextMenu.add_command(label="the next", command=self.next_file)

        self.contextMenu.add_command(label="the previous", accelerator="KeyPress-Left",
                                     command=lambda: [self.previous_file(), self.show_attribute(), self.drawpicture()])
        self.contextMenu.add_command(label="the next", accelerator="KeyPress-Rigth",
                                     command=lambda: [self.next_file(), self.show_attribute(), self.drawpicture()])

        # 为右键绑定事件
        self.master.bind('<Button-3>', self.createContextMenu)

    # 与各个事件相关联的方法
    # 设置要遍历的目录；最后又调用doLS函数
    def setDirAndGo(self, ev=None):
        # 获取最新的路径
        self.last = self.cwd.get()
        # 双击时设定北京为红色
        self.dirs.config(selectbackground='red')
        # 获取下一层文件夹
        check = self.dirs.get(self.dirs.curselection())
        if not check:
            check = os.curdir
        self.cwd.set(check)
        self.doLS()

    # 实现遍历目录的功能，这也是整个GUI程序最关键的部分。
    def doLS(self, ev=None):
        error = ''
        # 获取当前双击的文件名
        tdir = self.cwd.get()
        # 进行一些安全检查
        if not tdir:
            tdir = os.curdir
        if not os.path.exists(tdir):
            error = tdir + ': 没有这个文件'
        # elif not os.path.isdir(tdir):
        #     error = tdir + ':不是文件夹'
        elif tdir[-4:] == ".txt":
            error = os.path.join(os.getcwd(), tdir)
            # 接下来如何调用openfile文件呢

            # 每次打开一个新文件都要清空textpad1的内容
            self.textpad1.config(state="normal")
            self.textpad1.delete("1.0", "end")
            # 每次打开一个新文件都要清空textpad2的内容
            self.textpad2.config(state="normal")
            self.textpad2.delete("1.0", "end")

            with open(error, 'r') as f:
                self.textpad1.insert(INSERT, f.read())
                # 使得textpad1里的内容不可修改
                self.textpad1.config(state="disabled")

                self.txt_file_path = os.getcwd()
                self.txt_file_name = tdir
                txt_file_path_split = self.txt_file_path[:-6]
                txt_file_name_split = tdir[:-4]
                json_file_temp_path = os.path.join(txt_file_path_split, 'Attributes/')
                self.json_file_path = os.path.join(json_file_temp_path, txt_file_name_split + '.json')

                self.filepath = os.path.join(os.getcwd(), tdir)
                self.var_name_content.set(self.txt_file_name)


        # 如果发生错误，之前的目录就会重设为当前目录
        if error:
            self.cwd.set(error)
            self.master.update()
            sleep(1)
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
            self.cwd.set(self.last)
            self.dirs.config(selectbackground='LightSkyBlue')
            self.master.update()
            return
        # 如果一切正常
        self.cwd.set('正在获取目标文件夹内容……')
        self.master.update()
        dirlist = os.listdir(tdir)  # 获取实际文件列表
        dirlist.sort()
        os.chdir(tdir)

        self.dirl.config(text=os.getcwd())
        self.dirs.delete(0, END)
        self.dirs.insert(END, os.curdir)
        self.dirs.insert(END, os.pardir)
        for eachFile in dirlist:  # 替换Listbox中的内容
            self.dirs.insert(END, eachFile)
        self.cwd.set(os.curdir)
        self.dirs.config(selectbackground='LightSkyBlue')

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
            self.var_name_content.set(self.txt_file_name)

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
        self.master.quit()

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

        self.fig.clear()
        value = np.loadtxt(self.filepath)
        x = range(len(value))
        ax = self.fig.add_subplot(111)
        ax.plot(x, value)
        self.canvas.draw()

        # # 计算颜色和面积
        # N = 150
        # r = 2 * np.random.rand(N)
        # theta = 2 * np.pi * np.random.rand(N)
        # area = 200 * r ** 2
        # colors = theta
        # ax = self.fig.add_subplot(111, projection='polar')
        # ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
        # self.canvas.draw()

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
            self.var_name_content.set(self.txt_file_name)

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
            self.var_name_content.set(self.txt_file_name)


if __name__ == '__main__':
    root = Tk()
    root.title('my first Gui')
    root.geometry('850x550+100+200')
    app = Application(master=root)
    root.mainloop()
