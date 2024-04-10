# -*- coding: utf-8 -*-
"""本脚本用于打包后的程序瘦身"""
import json
import os
import sys
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

file_json = Path.cwd() / "white_files.json"

white_dict = {"python": ["api-ms-win-core", "base_library.zip", ".tcl", "tclIndex", "MSVCP140.dll",
                         "cacert.pem", "cp936.enc", "__init__", "python.exe", "pythonw.exe",],
              "matplotlib": ["matplotlibrc", ".load-order"],
              "request": ["msgcat-1.6.1.tm"],
              "plotly": ["plotly.json", "plotly.min.js"],
              "pyecharts": ["pyecharts"],
              "pyqtwebengine": ["QtWebEngineProcess.exe", "icudtl.dat", "qtwebengine_devtools_resources.pak",
                                "qtwebengine_resources", "qt.conf"],
              "win32": ["pywin32.pth"],
              "streamlit": ["streamlit\\static"]

              }
white_file_type = [".pyi", ".py"]


def get_file_paths(directory: Path) -> list:
    """获取指定路径所有文件名"""
    file_list = []
    files_paths = directory.glob("**/*.*")
    for path in files_paths:
        if path.is_file():
            file_list.append(path)
    return file_list


def is_file_in_use(file_name: Path) -> bool:
    """判断该文件是否被占用,被占用即返回True"""
    file_name = str(file_name)
    try:
        # 尝试以读写模式打开文件
        with open(file_name, "r+", encoding="utf-8") as file:
            # 如果文件成功打开，说明没有被占用
            return False
    except OSError as e:
        # 如果抛出OSError异常，说明文件被占用
        return True
    except Exception as e:
        # 处理其他可能的异常
        print(f"An error occurred: {e}")
        return False


def move_file_to_folder(file_old: Path, file_new: Path) -> None:
    """使用Path.rename方法移动文件"""
    if not file_new.parent.exists():
        try:
            os.makedirs(file_new.parent)
        except PermissionError as pe:
            messagebox.showerror("权限错误", f"无法创建目录：{pe}")
            return
    try:
        file_old.rename(file_new)
    except PermissionError as pe:
        pass
    except Exception as e:
        messagebox.showerror("未知错误", f"移动文件时发生错误：{e}")


class WinGUI(Tk):
    """窗口类"""

    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_button_file = self.__tk_button_file(self)
        self.tk_button_start = self.__tk_button_start(self)
        self.tk_input_file = self.__tk_input_file(self)
        self.tk_button_infor = self.__tk_button_infor(self)
        self.tk_progressbar_progress = self.__tk_progressbar_progress(self)

    def __win(self):
        """创建窗口"""
        self.title("打包瘦身小工具")
        width = 335
        height = 140
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    @staticmethod
    def __tk_button_file(parent):
        """创建button"""
        btn = Button(parent, text="目标文件夹", takefocus=False, )
        btn.place(x=5, y=5, width=100, height=30)
        return btn

    @staticmethod
    def __tk_button_start(parent):
        """创建button"""
        btn = Button(parent, text="开始处理", takefocus=False, )
        btn.place(x=5, y=55, width=100, height=30)
        return btn

    @staticmethod
    def __tk_input_file(parent):
        """创建输入框"""
        ipt = Entry(parent, )
        ipt.place(x=124, y=5, width=200, height=30)
        return ipt

    @staticmethod
    def __tk_button_infor(parent):
        """创建button"""
        btn = Button(parent, text="使用说明", takefocus=False, )
        btn.place(x=240, y=55, width=80, height=30)
        return btn

    @staticmethod
    def __tk_progressbar_progress(parent):
        progressbar = Progressbar(parent, orient=HORIZONTAL)
        progressbar.place(x=5, y=100, width=320, height=30)
        return progressbar


class MasterGui(WinGUI):
    """程序主窗口"""

    def __init__(self):
        super().__init__()
        try:
            self.wm_iconbitmap("file.ico")
        except FileNotFoundError:
            pass
        self.progress_var = DoubleVar()
        self.tk_button_file.config(command=self.select_file)
        self.tk_button_start.config(command=self.start_work)
        self.tk_button_infor.config(command=self.sys_info)
        self.tk_progressbar_progress.config(variable=self.progress_var, length=100, )
        self.file_name = ""
        self.white_dict = None
        self.white_list = []

        self.ini_window()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.mainloop()

    def ini_window(self) -> None:
        """程序初始化"""
        if Path(file_json).exists():
            print("读取白名单配置文件", f"{file_json}")
            with open(file_json, "r", encoding="utf-8") as file:
                self.white_dict = json.load(file)
            try:
                assert isinstance(self.white_dict, dict)
            except AssertionError:
                print("读取的白名单配置文件不合法，请检查!")
                input("按回车键继续...")
                sys.exit()
        else:
            self.white_dict = white_dict
        for value in self.white_dict.values():
            self.white_list.extend(value)

    @staticmethod
    def close_window():
        """窗口关闭事件，保存白名单文件列表"""
        if not Path(file_json).exists():
            json_data = json.dumps(white_dict, indent=4)
            with open(file_json, 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)
            print(f"已写入默认白名单配置文件，{file_json},下次运行程序自动读取")
            messagebox.showinfo(title="保存", message=f"已写入默认白名单配置文件{file_json}")
        sys.exit()

    def select_file(self) -> None:
        """选择目标文件夹"""
        selected_path = filedialog.askdirectory()
        if selected_path == "":
            return
        selected_path = Path(selected_path)
        if "C" in selected_path.drive:
            messagebox.showinfo(title="警告", message="本程序不支持在C盘路径进行操作，请重选路径！")
            return
        self.tk_input_file.delete(0, "end")
        self.tk_input_file.insert(0, str(selected_path))

    def check_file(self, file: Path) -> bool:
        """判断该文件是否在白名单中,或在白名单文件类型中,如果在即返回False"""
        file = str(file)
        for data in self.white_list:
            if data in file:
                return False
        for file_type in white_file_type:
            if Path(file).suffix == file_type:
                return False
        return True

    def start_work(self):
        """开始处理"""
        file_path = self.tk_input_file.get()
        if file_path == "":
            return
        file_path = Path(file_path)
        if not file_path.exists():
            return
        if "C" in file_path.drive:
            messagebox.showinfo(title="警告", message="本程序不支持在C盘路径进行操作，请重选路径！")
            return
        self.file_name = file_path

        file_dir_old = self.file_name
        file_dir_new = Path(str(file_dir_old) + "_new")
        file_list = get_file_paths(self.file_name)
        file_move_list = []
        rst_txt = Path(file_dir_old).parent.joinpath(f"{self.file_name.name}_文件移动清单.txt")
        self.tk_progressbar_progress.config(value=0)
        for idx, filename in enumerate(file_list):
            if self.check_file(filename):  # 检查白名单
                if not is_file_in_use(filename):
                    relative_path = filename.relative_to(self.file_name)
                    filename_new = file_dir_new.joinpath(relative_path)
                    move_file_to_folder(filename, filename_new)
                    file_move_list.append(str(filename))
            self.progress_var.set(idx / len(file_list) * 100)
            self.update()
        if rst_txt.exists():
            os.remove(str(rst_txt))
        with open(rst_txt, "w", encoding="utf-8") as file:
            for temp_file in file_move_list:
                file.write(f"{temp_file}\n")
        messagebox.showinfo("提示", "文件移动结束！")

    @staticmethod
    def sys_info() -> None:
        """工具说明"""
        message = ("运行原理：\n"
                   "本工具仅在win7/win11测试通过。"
                   "工具通过指定文件目录，来移动该目录下未被程序占用的文件，移动的文件会在指定文件目录外的\"目录_new\"里面，同时生成文件移动清单.txt。\n"
                   "使用方法：运行自己打包好的程序，尽量功能全开的情况下，使用本工具，指定程序目录，工具开始移动未占用的文件。\n"
                   "移动结束后，请再运行一遍自己的程序，如果提示文件缺少，可以从《文件移动清单.txt》去找，还原即可。\n"
                   "瘦身效果：根据我的历史使用记录，本工具针对pyinstaller打包的程序能缩小体积50%左右，针对nuitka打包的程序能缩小体积30%左右。\n"
                   "注意事项：工具目前还不够完善，对于有些文件，是程序必须的，但是又在程序运行时不占用的，就需要将文件名加入白名单列表中。\n"
                   "程序第一次运行，会自动生成white_files.json文件，该文件记录了工具运行时不移动的文件，请根据使用情况酌情添加。")
        messagebox.showinfo(title="使用说明", message=message)


if __name__ == "__main__":
    win = MasterGui()
