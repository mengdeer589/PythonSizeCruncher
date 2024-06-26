# PythonSizeCruncher 打包瘦身脚本 
This script is aimed at reducing the size of packages generated by PyInstaller, Nuitka, or Python embeddable builds through selective file trimming.

本脚本用于打包后的程序瘦身，用于有效减小pyinstaller/nuitka/python embeddable打包后的程序体积。

# Principle of Operation 实现原理
When a Python program runs, it will cause files it needs to become locked or occupied. By running this script concurrently with the Python program, it identifies and deletes files that are not currently being used, thereby achieving the goal of filtering out unnecessary files for the program.

python程序运行时，会将需要的文件变为占用状态，通过运行python程序的同时，运行本脚本，将未被占用的文件删除，达到筛选程序不需要的文件的目的。
# Steps of Operation 操作流程
1，Running your self-packaged program, which could have been bundled using either PyInstaller, Nuitka, or a Python embeddable distribution, aims to maintain program operation under conditions where all features are ideally enabled and functional.

1，运行自己打包好的程序，可以是pyinstaller/nuitka/python embeddable打包的程序，尽量功能全开的情况下，保持程序运行。

2，Run this script and specify the program directory. The script will automatically access all files within the designated directory. If a file is found to be unoccupied, meaning it is not currently in use, it will be identified as unnecessary for the program and consequently moved to a '_new' directory.

2，运行本脚本，指定程序目录，脚本会自动访问指定目录下的所有文件，若该文件未被占用，即认定为程序不需要的文件，会移动该文件至_new目录。

3，Upon completion of the moving process, close your own program and then run it again. If prompted about missing files, refer to the '文件移动清单.txt' to locate and restore the necessary files.

3，移动结束后，关闭自己的程序，并再运行一遍自己的程序，如果提示文件缺少，可以从《文件移动清单.txt》去找，还原即可。
# Cruncher Result 瘦身效果
Based on my historical usage records, this script is capable of reducing the size of packages created with PyInstaller by approximately 50%, while for programs bundled with Nuitka and Python embeddable distributions, it achieves a reduction in size of around 30%.

根据我的历史使用记录，本脚本针对pyinstaller打包的程序能缩小体积50%左右，针对nuitka和python embeddable打包的程序能缩小体积30%左右。
# Attention 注意事项
The script is currently not fully optimized, and for some files that are essential for the program but are not occupied during program execution, it is necessary to add these filenames to a whitelist. The script will then refrain from moving these files during processing.

脚本目前还不够完善，对于有些文件，是程序必须的，但是又在程序运行时不占用的，就需要将文件名加入白名单列表中，脚本会在处理时不移动这些文件。

Currently, this script has only been tested on Win7/win11.

目前本脚本仅在win7/win11上做过测试，功能正常。

When the program runs for the first time, it automatically generates a 'white_files.json' file, which records the files that the tool does not move during its operation. Please add or modify this list according to your specific usage scenarios.

程序第一次运行，会自动生成white_files.json文件，该文件记录了工具运行时不移动的文件，请根据使用情况酌情添加。
# 视频演示
[b站视频-python程序打包瘦身](https://www.bilibili.com/video/BV16r421E7zU/)
