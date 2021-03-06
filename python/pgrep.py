# encoding=UTF-8
# functions: 在非AVOID_DIR目录下的文件CONTAINS_FILE中查找内容
from __future__ import print_function

import os
import sys
import commands
import re

DEBUG_PGREP = False
AVOID_DIR = ("build", "libs", ".externalNativeBuild", ".git", ".gradle", ".idea", ".settings")
CONTAINS_FILE = ("java", "xml", "c", "cpp", "gradle", "txt", "mk")

if (len(sys.argv) != 2):
    print ("arguments is ", str(sys.argv))
    print ("arguments should be one, but you have ", str(len(sys.argv) - 1))
    exit()

search_content = sys.argv[1]
if DEBUG_PGREP:
    print ("find content:", search_content)
    print ("find not in dirs:", AVOID_DIR)
    print ("find in file's extensions:", CONTAINS_FILE)

def should_grep(extend):
    if CONTAINS_FILE.__contains__(extend):
        return True

def find_file (path, content):
    parents = os.listdir(path)
    for parent in parents:
        child = os.path.join(path,parent)
        if os.path.isdir(child):
            if not AVOID_DIR.__contains__(parent):
                find_file(child, content)
            else:
                pass
        else:
            search_file(child, content)
            pass

def search_file(file, content):
    # 添加过滤条件, 符合过滤条件的继续往下
    if DEBUG_PGREP:
        print(file)
    file_divided = file.split(".")
    if len(file_divided) <= 1: #该文件无后缀
        return # gradlew文件就是没有后缀, 不需要查找
    else:
        file_extend = file_divided[len(file_divided) - 1]
        if not should_grep(file_extend):
            return
        else:
            pass

    len_cwd = len(cwd) + 1
    len_file = len(file)
    sub_file = str(file)[len_cwd: len_file]
    reg_grep = "grep '" + content + "' '" + sub_file + "' -irn"
    tuple_grep = commands.getstatusoutput(reg_grep)
    if DEBUG_PGREP:
        print(tuple_grep)
    if tuple_grep[0] == 256:
        return
    output = tuple_grep[1]
    pattern = re.compile(content, flags=re.I)
    strs = re.split(pattern, output)
    if DEBUG_PGREP:
        print("output =", output)
        for si in strs:
            print("si =", si)
    if len(strs) <= 1:
        # 出错了, 在(if tuple_grep[0] == 256:)处就应该返回
        error_content = "\033[1;32;31m%s\033[0m" % "Error:"
        print(error_content, "len(strs) =", len(strs), "grep_return_code =", tuple_grep[0])
        return
    else:
        if DEBUG_PGREP:
            print("DEBUG_PGREP: matches", "")
    color_content = "\033[1;32;31m%s\033[0m" % content
    i = 0
    for s in strs:
        if i != 0:
            print (color_content, end='')
        print (s, end='')
        i = i + 1
    print (end=u'\n')

cwd = os.getcwd()

find_file(cwd, search_content)

