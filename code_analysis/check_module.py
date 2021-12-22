# -*- coding: utf-8 -*-

import operator
import re
import os
import glob
import fnmatch
import argparse
from functools import reduce


def main():
    """
    主函数
    """
    print('\ \ /\ / / __|')
    print(' \ V  V / (__')
    print('  \_/\_/ \___|')
    parser = argparse.ArgumentParser(description="this is wordCounter")
    parser.add_argument("-c", metavar="--char", dest="char_arg", help="return the number of characters")
    parser.add_argument("-w", metavar="--word", dest="word_arg", help="return the number of words")
    parser.add_argument("-l", metavar="--line", dest="line_arg", help="return the number of lines")
    parser.add_argument("-s", metavar="--recurve", dest="recur_arg",
                        help="Recursive file information under the directory")
    parser.add_argument("-a", metavar="--CCBcount", dest="ccb_arg",
                        help="Counts the number of lines of code, comment lines, blank lines in the file  or files in the directory")
    args = parser.parse_args()
    if args.char_arg:
        charsCount = CharCount(args.char_arg)
        print("文本的字符数目：%s" % (charsCount))
    if args.word_arg:
        wordsCount = WordCount(args.word_arg)
        print("文本的单词数目：%s" % (wordsCount))
    if args.line_arg:
        linesCount = LineCount(args.line_arg)
        print("文本的行数：%s" % (linesCount))
    if args.recur_arg:
        RecurveDirMain(args.recur_arg)
    if args.ccb_arg:
        CCBCountMain(args.ccb_arg)


def CharCount(fileName):
    """
    统计字符数,不包括空白字符，包括空格、制表符、换页符等
    :param:
        fileName: 统计的文件
    :return: 字符的数量
    """
    charsCount = 0
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                match = re.findall(r'[\s]+', line)
                for i in match:
                    line = line.replace(i, '')
                charsCount += len(line)
        return charsCount
    except IOError:
        print("打开文件失败！请检查路径是否正确")


def WordCount(fileName):
    """
    统计单词数
    :param:
        fileName: 统计的文件
    :return: 单词的数量
    """
    wordsCount = 0
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                match = re.findall(r'[a-zA-Z-\']+', line)
                wordsCount += len(match)
        return wordsCount
    except IOError:
        print("文件打开失败！请检查路径是否正确")


def check_import_modules(file_name):
    """
    import sys
    import fibo, sys
    import defusedxml.ElementTree as ET
    from sound.effects import echo
    from fibo import fib, fib2
    ###################
    # Ignore the following usages：
    from . import echo
    from .. import formats
    from ..filters import equalizer

    :param file_name:
    :return:
    """
    word_dir = {}
    k_dir = {}
    try:
        with open(file_name, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                line = line.split("as")[0]
                line = line.strip()

                wd_list = []
                if line.startswith('import'):
                    t_list = line.split()
                    line_num = len(t_list)
                    if line_num == 2:
                        # import sys
                        t = t_list[1].split(".")[0]
                        wd_list = [t]
                        # update_frequency_dictionary(wd_list, word_dir)
                    elif line_num > 2:
                        # import fibo, sys
                        tt_list = t_list[1:]
                        t = reduce(lambda x, y: x + y, tt_list)
                        t = t.split(".")[0]
                        wd_list = [t]
                        # update_frequency_dictionary([t], word_dir)
                    else:
                        # print("Error 0001!")
                        # print("line=", line)
                        pass

                    if wd_list:
                        update_frequency_dictionary(wd_list, word_dir)

                if line.startswith('from'):
                    t_list = line.split()
                    line_num = len(t_list)
                    if line_num >= 4:
                        if not t_list[1].startswith('.'):
                            # print(f"t_list[1] = {t_list[1]}  ")
                            wd_list = t_list[1].split(".")
                            # print(f"wd_list = {wd_list}  ")
                            t_first = wd_list[0]
                            # print(f"wd_list[0] = {t_first}  ")
                            update_frequency_dictionary([t_first], word_dir)
                    else:
                        # print("Error 0002!")
                        # print("line=", line)
                        pass

        k_dir[file_name] = word_dir
        return k_dir
    except IOError:
        print("文件打开失败！请检查路径是否正确")


def print_frequency_dictionary(word_count):
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):
        print(key, value)


def create_frequency_dictionary(word_list):
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


def update_frequency_dictionary(word_list, word_dir):
    for word in word_list:
        if word in word_dir:
            word_dir[word] += 1
        else:
            word_dir[word] = 1


def LineCount(fileName):
    """
    统计行数
    :param:
        fileName: 统计的文件
    :return: 单词的数量
    """
    linesCount = 0
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                linesCount += 1
        return linesCount
    except IOError:
        print("文件打开失败！请检查路径是否正确")


def RecurveDir(dirPath):
    """
    递归查找符合条件的文件
    :param:
        dirPath: 目录的路径
    :return: 符合条件的文件
    """
    fileList = []
    pathFileInfo = "*.*"
    pathList = glob.glob(os.path.join(dirPath, '*'))
    for mPath in pathList:
        if fnmatch.fnmatch(mPath, pathFileInfo):
            fileList.append(mPath)
            # print(fileList)
        elif os.path.isdir(mPath):
            # print(mPath)
            fileList += RecurveDir(mPath)
        else:
            pass
    return fileList


def RecurveDirMain(Path):
    """
    递归处理文件主函数
    :param
        Path: 输入的目录路径
    :return: None
    """
    cnt = 0
    path_dir_list = []
    fileList = RecurveDir(Path)
    for file in fileList:
        # print(file)
        if not file.endswith('.py'):
            continue
        cnt += 1
        # if cnt > 10:
        #     break

        if file.find("test_reporting") != -1 or \
            file.find("tests") != -1\
            :
            continue

        # wordsCount = WordCount(file)
        # linesCount = LineCount(file)
        # charsCount = CharCount(file)
        # print("%s 文件信息：\n字符数目：%s\n单词数目：%s\n行数：%s\n" % (file, charsCount, wordsCount, linesCount))

        word_dir = check_import_modules(file)
        print(word_dir)

        t_dict_keys = word_dir.keys()
        # print(t_dict_keys)
        if len(t_dict_keys) != 1:
            continue
        # print(type(t_dict_keys))
        t_k1 = list(t_dict_keys)[0]
        # print(type(t_k1))
        t_v1 = word_dir[t_k1]

        # print(t_v1)
        t_v_len = len(t_v1)
        if t_v_len == 0:
            continue

        path_dir_list.append(t_v1)
        # print(path_dir_list)
        # print_frequency_dictionary(word_dir)
    # print(path_dir_list)

    path_dir_list_len = len(path_dir_list)
    summary_dir = {}
    # Summary results
    for i, val in enumerate(path_dir_list):
        update_frequency_dictionary(val, summary_dir)

    print("Summary:")
    print_frequency_dictionary(summary_dir)


def CCBCountMain(fileName):
    """
    统计文本的代码行，空行，注释行主函数
    :param
        fileName：输入的文件
    :return: None
    """
    # 支持的后缀
    suffixList = ['.py', '.c', '.java', '.js', '.cpp']
    if os.path.isdir(fileName):
        fileList = RecurveDir(fileName)
        for file in fileList:
            suffix = os.path.splitext(file)[1]
            if suffix in suffixList:
                CodeCommentBlankCount(file)
    else:
        CodeCommentBlankCount(fileName)


def CodeCommentBlankCount(fileName):
    """
    统计文本的代码行，空行，注释行处理函数
    :param
        fileName：输入的文件
    :return: None
    """
    blankLines = 0
    commentLines = 0
    codeLines = 0
    isComment = False
    startComment = 0
    try:
        with open(fileName, 'r', encoding='utf-8') as f:
            for index, line in enumerate(f, start=1):
                stripLine = line.strip()
                # 判断多行注释是否开始
                if not isComment:
                    if stripLine.startswith("'''") or stripLine.startswith('"""') or stripLine.startswith('/*'):
                        isComment = True
                        startComment = index
                    # 单行注释，考虑多种情况
                    elif stripLine.startswith('#') or stripLine.startswith('//') or re.findall('^[}]+[\s\S]+[//]+',
                                                                                               stripLine):
                        commentLines += 1
                    elif stripLine == '' or stripLine == '{' or stripLine == '}':
                        blankLines += 1
                    else:
                        codeLines += 1
                # 多行注释已经开始
                else:
                    if stripLine.endswith("'''") or stripLine.endswith('"""') or stripLine.endswith('*/'):
                        isComment = False
                        commentLines += index - startComment + 1
                    else:
                        pass
        print("%s 文件信息：\n文本的代码行数：%s\n文本的空白行数：%s\n文本的注释行数：%s\n" % (fileName, codeLines, blankLines, commentLines))
    except IOError:
        print("文件打开失败！请检查文件路径是否正确")


if __name__ == '__main__':
    main()
