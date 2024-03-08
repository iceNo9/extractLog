# 这是一个示例 Python 脚本。
import csv
import os
import re
import string
import sys
from tkinter import messagebox
import chardet
import codecs

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


def add_data(rv_content, rv_key, rv_num):
    pattern1 = r'"(.*?)"'  # 非贪婪模式，只匹配最小长度的内容
    result1 = re.findall(pattern1, rv_content)
    if result1:
        pattern2 = r'\\n'
        result2 = re.findall(pattern2, result1[0])
        print(result1[0])
        if result2:
            pattern3 = r'[^0-9a-zA-Z]\\n'
            result3 = re.findall(pattern3, result1[0])
            if result3:
                data = ["", rv_key, result1[0], "Need Modify \\n"]
            else:
                data = ["", rv_key, result1[0]]
        else:  # 没有\n
            data = ["", rv_key, result1[0], "Need Add \\n"]
    else:
        data = ["", "Row " + str(rv_num) + " Find Error"]
    log_list.append(data)


def add_title(rv_content):
    data = [rv_content]
    log_list.append(data)


def check_log(rv_content, rv_num):
    if re.search("infoPrint", rv_content):
        add_data(rv_content, "info", rv_num)
    elif re.search("errorPrint", rv_content):
        add_data(rv_content, "error", rv_num)


def file_parse(rv_path):
    with open(rv_path, "r", encoding="utf-8") as f:
        for num, line in enumerate(f, 1):
            content = line.strip()  # 输出去除换行符的每一行内容
            if not check_line_comments(content):
                check_log(content, num)


def convert_to_utf8(file_path, output_path=None):
    # Step 1: 检测文件的原始编码
    with open(file_path, 'rb') as at_file:
        raw_data = at_file.read()
        result = chardet.detect(raw_data)
        detected_encoding = result['encoding']

    # Step 2: 打开文件并转码
    if output_path is None:
        output_path = file_path + ".utf8"

    with codecs.open(file_path, 'r', encoding=detected_encoding) as source_file:
        source_content = source_file.read()

    with codecs.open(output_path, 'w', encoding='utf-8') as target_file:
        target_file.write(source_content)
    print(f"文件 '{file_path}' 已成功转换为 UTF-8 编码，并保存为 '{output_path}'。")


def format_change(rv_file):
    convert_to_utf8(rv_file, rv_file)


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
