# -*- coding: utf-8 -*-
"""本脚本用于打包后的程序瘦身"""
import _tkinter
import json
import os
import sys
import threading
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

file_json = Path(__file__).parent.joinpath("white_files.json")

white_dict = {"python": ["api-ms-win-core", "base_library.zip", ".tcl", "tclIndex", "MSVCP140.dll",
                         "cacert.pem", "cp936.enc", "__init__", "python.exe", "pythonw.exe", "VCRUNTIME140_1.dll"],
              "matplotlib": ["matplotlibrc", ".load-order"],
              "request": ["msgcat-1.6.1.tm"],
              "plotly": ["plotly.json", "plotly.min.js", "package_data\\templates"],
              "pyecharts": ["pyecharts"],
              "pyqtwebengine": ["QtWebEngineProcess.exe", "icudtl.dat",
                                "qtwebengine_devtools_resources.pak",
                                "qtwebengine_resources", "qt.conf"],
              "streamlit": ["streamlit\\static"],
              "trame_vtk": ["static_viewer.html"]

              }
white_file_type = [".pyi", ".py", ".pth", "._pth"]


class WinGUI(Tk):
    """窗口类"""

    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_button_file = self.__tk_button_file(self)
        self.tk_button_start = self.__tk_button_start(self)
        self.tk_input_file = self.__tk_input_file(self)
        self.tk_button_infor = self.__tk_button_infor(self)
        self.tk_check_button_safe = self.__tk_check_button_safe(self)
        self.tk_label_progressbar = self.__tk_label_progressbar(self)
        self.tk_progressbar_progress = self.__tk_progressbar_progress(self)

    def __win(self):
        """创建窗口"""
        self.title("打包瘦身小程序")
        width = 500
        height = 150
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = f'{width}x{height}+{int((screenwidth - width) / 2)}+{int((screenheight - height) / 2)}'
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    @staticmethod
    def __tk_button_file(parent):
        """创建button"""
        btn = Button(parent, text="目标文件夹", takefocus=False, )
        btn.place(x=5, y=10, width=100, height=30)
        return btn

    @staticmethod
    def __tk_button_start(parent):
        """创建button"""
        btn = Button(parent, text="开始处理", takefocus=False, )
        btn.place(x=5, y=100, width=100, height=30)
        return btn

    @staticmethod
    def __tk_input_file(parent):
        """创建输入框"""
        ipt = Entry(parent, )
        ipt.place(x=110, y=10, width=370, height=30)
        return ipt

    @staticmethod
    def __tk_button_infor(parent):
        """创建button"""
        btn = Button(parent, text="使用说明", takefocus=False, )
        btn.place(x=380, y=100, width=100, height=30)
        return btn

    @staticmethod
    def __tk_check_button_safe(parent):
        cb = Checkbutton(parent, text="当前：安全模式", )
        cb.place(x=180, y=100, width=120, height=30)
        return cb

    @staticmethod
    def __tk_label_progressbar(parent):
        label = Label(parent, text="处理进度", anchor="center")
        label.place(x=5, y=55, width=100, height=30)
        return label

    @staticmethod
    def __tk_progressbar_progress(parent):
        """创建进度条"""
        progressbar = Progressbar(parent, orient=HORIZONTAL)
        progressbar.place(x=110, y=55, width=370, height=30)
        return progressbar


class MasterGui(WinGUI):
    """程序主窗口"""

    def __init__(self):
        super().__init__()
        icon = Path(__file__).parent.joinpath("file.ico")
        try:
            self.wm_iconbitmap(icon)
        except FileNotFoundError:
            pass
        except _tkinter.TclError:
            pass
        self.safe_var = BooleanVar()
        self.progress_var = DoubleVar()
        self.tk_button_file.config(command=self.select_file)
        self.tk_button_start.config(command=self.start_work)
        self.tk_button_infor.config(command=self.sys_info)
        self.tk_check_button_safe.config(variable=self.safe_var)
        self.safe_var.set(True)
        self.safe_var.trace_add("write", self.mode_change)
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

    def update_progress_safe(self, value):
        """安全地更新进度条的值"""
        self.after(0, lambda: self.update_progress(value))

    def update_progress(self, value):
        """更新进度条的值"""
        self.progress_var.set(value)
        self.update_idletasks()

    def select_file(self) -> None:
        """选择目标文件夹"""
        selected_path = filedialog.askdirectory()
        if selected_path == "":
            return
        selected_path = Path(selected_path)
        #为了避免误操作C盘重要文件，本程序不允许在C盘进行操作
        if "C" in selected_path.drive:
            messagebox.showinfo(title="警告", message="本程序不支持在C盘路径进行操作，请重选路径！")
            return
        self.tk_input_file.delete(0, "end")
        self.tk_input_file.insert(0, str(selected_path))

    def work_thread_func(self, white_list, file_path):
        """文件移动多线程"""
        file_dir_new = Path(str(file_path) + "_new")
        only_binary = self.safe_var.get()
        file_list = FileRemove.get_file_paths(file_path, only_binary)
        file_move_list = []
        rst_txt = Path(file_path).parent.joinpath(f"{file_path.name}_文件移动清单.txt")
        file_count = len(file_list)
        for idx, filename in enumerate(file_list):
            if FileRemove.check_file(white_list, filename) and (not FileRemove.is_file_in_use(filename)):  # 检查白名单和占用
                relative_path = filename.relative_to(file_path)
                filename_new = file_dir_new.joinpath(relative_path)
                FileRemove.move_file_to_folder(filename, filename_new)
                file_move_list.append(str(filename))
                print(f"移动{filename}")
            else:
                print(f"跳过{filename}")
            self.update_progress_safe((idx + 1) / file_count * 100)

        if rst_txt.exists():
            os.remove(str(rst_txt))
        with open(rst_txt, "w", encoding="utf-8") as file:
            for temp_file in file_move_list:
                file.write(f"{temp_file}\n")
        messagebox.showinfo("提示", "文件移动结束！")
        self.tk_button_start.config(state=ACTIVE)

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
        self.tk_progressbar_progress.config(value=0)

        file_move_thread = threading.Thread(target=self.work_thread_func,
                                            args=(self.white_list, file_path,
                                                  ),
                                            daemon=True)
        self.tk_button_start.config(state=DISABLED)
        file_move_thread.start()

    def mode_change(self, *args):
        value = self.safe_var.get()
        if value:
            self.tk_check_button_safe.config(text="当前：安全模式")
        else:
            self.tk_check_button_safe.config(text="当前：极限模式")

    @staticmethod
    def sys_info() -> None:
        """程序说明"""
        message = ("运行原理：\n"
                   "本程序仅在win7/win11测试通过。"
                   "程序通过指定文件目录，来移动该目录下未被程序占用的文件，移动的文件会在指定文件目录外的\"目录_new\"里面，同时生成文件移动清单.txt。\n\n"
                   "使用方法：\n1，运行自己打包好的程序，尽量功能全开的情况下;\n2，使用本程序，指定程序目录，程序开始移动未占用的文件;\n"
                   "3，移动结束后，请再运行一遍自己的程序，如果提示文件缺少，可以从《文件移动清单.txt》去找，还原即可。\n\n"
                   "瘦身效果：\n根据我的历史使用记录，本程序针对pyinstaller打包的程序能缩小体积50%左右，针对nuitka打包的程序能缩小体积30%左右。\n"
                   "注意事项：程序目前还不够完善，对于有些文件，是程序必须的，但是又在程序运行时不占用的，就需要将文件名加入白名单列表中。\n\n"
                   "安全模式：程序只针对pyd,dll文件进行操作，瘦身成功率较高；\n"
                   "极限模式：程序针对所有类型文件进行操作，瘦身效果较好，默认使用安全模式。\n\n"
                   "程序第一次运行，会自动生成white_files.json文件，该文件记录了程序运行时不移动的文件，请根据使用情况酌情添加。")
        messagebox.showinfo(title="使用说明", message=message)


class FileRemove:
    """文件移动函数类"""

    @staticmethod
    def get_file_paths(directory: Path, only_binary: bool = True) -> list:
        """获取指定路径所有文件名,only_binary设置是否只检测pyd,dll文件"""
        file_list = []
        if only_binary:
            files_paths = [path for pattern in ('*.pyd', '*.dll') for path in directory.glob('**/' + pattern)]
        else:
            files_paths = directory.glob("**/*.*")
        for path in files_paths:
            if path.is_file():
                file_list.append(path)
        return file_list

    @staticmethod
    def is_file_in_use(file_name: Path) -> bool:
        """判断该文件是否被占用,被占用即返回True"""
        file_name = str(file_name)
        try:
            # 尝试以读写模式打开文件
            with open(file_name, "r+", encoding="utf-8") as file:
                # 如果文件成功打开，说明没有被占用
                return False
        except OSError:
            # 如果抛出OSError异常，说明文件被占用
            return True
        except Exception as e:
            # 处理其他可能的异常
            print(f"An error occurred: {e}")
            return True

    @staticmethod
    def move_file_to_folder(file_old: Path, file_new: Path) -> None:
        """使用Path.rename方法移动文件"""
        if not file_new.parent.exists():
            try:
                os.makedirs(file_new.parent)
            except (PermissionError, FileNotFoundError):
                pass
        try:
            file_old.rename(file_new)
        except Exception:
            pass

    @staticmethod
    def check_file(white_list: list, file: Path) -> bool:
        """判断该文件是否在白名单中,或在白名单文件类型中,如果在即返回False"""
        file = str(file)
        for data in white_list:
            if data in file:
                return False
        for file_type in white_file_type:
            if Path(file).suffix == file_type:
                return False
        return True


def start():
    win = MasterGui()


if __name__ == "__main__":
    win = MasterGui()
