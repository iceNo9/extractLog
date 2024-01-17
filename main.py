# 这是一个示例 Python 脚本。
import csv
import os
import re
import string
import sys
from tkinter import messagebox

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

log_list = []


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


def check_dir(param):
    if os.path.isdir(param):
        return True
    else:
        return False


def check_line_comments(rv_content):
    if rv_content.count("//") > 0:
        # if re.search("\\\\", rv_content):
        return True
    else:
        return False


def add_data(rv_content, rv_key):
    pattern = r'"(.*?)"'  # 非贪婪模式，只匹配最小长度的内容
    result = re.findall(pattern, rv_content)
    data = [rv_key, result[0]]
    log_list.append(data)


def add_title(rv_content):
    data = [rv_content]
    log_list.append(data)


def check_log(rv_content):
    if re.search("infoPrint", rv_content):
        add_data(rv_content, "info")
    elif re.search("errorPrint", rv_content):
        add_data(rv_content, "error")


def file_parse(rv_path):
    with open(rv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            content = line.strip()  # 输出去除换行符的每一行内容
            if not check_line_comments(content):
                check_log(content)


def format_change(rv_file):
    with open(rv_file, "r") as at_ile:
        content = at_ile.read()

    with open(rv_file, "w", encoding="utf-8") as at_ile:
        at_ile.write(content)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    dir_path = sys.argv[1]
    log_list.clear()

    if check_dir(dir_path):
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".c"):  # 只处理后缀为".c"的文件
                    path = os.path.join(root, file)
                    add_title(file)
                    format_change(path)
                    file_parse(path)

        if len(log_list):
            with open("output.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in log_list:
                    writer.writerow(row)
                messagebox.showinfo(title='提醒', message='操作完成')
    else:
        messagebox.showinfo(title='提醒', message='请传入目录')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
