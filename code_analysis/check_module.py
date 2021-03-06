# -*- coding: utf-8 -*-

import operator
import re
import os
import glob
import fnmatch
import argparse
from collections import Counter
from functools import reduce

# 156
g_builtins_list = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
                   'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
                   'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
                   'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError',
                   'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError',
                   'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
                   'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
                   'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented',
                   'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError',
                   'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
                   'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
                   'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
                   'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
                   'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_',
                   '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__',
                   '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
                   'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict',
                   'dir', 'divmod', 'enumerate', 'eval', 'exec', 'execfile', 'exit', 'filter', 'float', 'format',
                   'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int',
                   'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview',
                   'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr',
                   'reversed', 'round', 'runfile', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
                   'super', 'tuple', 'type', 'vars', 'zip']

# 35
g_kwlist = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']


def main():
    same_iterm = [x for x in g_kwlist if x in g_builtins_list]
    if same_iterm:
        print("same_iterm:", same_iterm)

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
        print("????????????????????????%s" % (charsCount))
    if args.word_arg:
        wordsCount = WordCount(args.word_arg)
        print("????????????????????????%s" % (wordsCount))
    if args.line_arg:
        linesCount = LineCount(args.line_arg)
        print("??????????????????%s" % (linesCount))
    if args.recur_arg:
        RecurveDirMain(args.recur_arg)
    if args.ccb_arg:
        CCBCountMain(args.ccb_arg)


def CharCount(fileName):
    """
    ???????????????,???????????????????????????????????????????????????????????????
    :param:
        fileName: ???????????????
    :return: ???????????????
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
        print("????????????????????????????????????????????????")


def WordCount(fileName):
    """
    ???????????????
    :param:
        fileName: ???????????????
    :return: ???????????????
    """
    wordsCount = 0
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                match = re.findall(r'[a-zA-Z-\']+', line)
                print("match:", match)  # debug
                wordsCount += len(match)
        return wordsCount
    except IOError:
        print("????????????????????????????????????????????????")


def word_count(fileName):
    """
    ???????????????
    :param:
        fileName: ???????????????
    :return: ???????????????
    """
    words_list = []
    # print("fileName:", fileName)  # debug
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                # skipped blank line
                if line == '\n':
                    continue
                # print("line:{}<len> {}".format(line, len(line)))  # debug
                # skipped comment line
                if line.startswith('#'):
                    continue
                # Naming rules
                match = re.findall(r'[a-zA-Z_]+[\w]*', line)
                if match:
                    # print("match:", match)  # debug
                    words_list.extend(match)
        return words_list
    except IOError:
        print("????????????????????????????????????????????????")


def check_import_modules(file_name):
    """
    import sys
    import fibo, sys
    import defusedxml.ElementTree as ET
    from sound.effects import echo
    from fibo import fib, fib2
    ###################
    # Ignore the following usages???
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
                # import _strptime  # workaround python bug ref: https://stackoverflow.com/a/22476843/2514803
                l_index = line.find('#')
                line = line[:l_index]
                line = line.strip()
                # skipped line, eg import apis.system.basic as basic_obj
                line = line.split(" as")[0]
                line = line.strip()

                wd_list = []

                # skipped some line, eg: import_file_path(path, 1)
                if line.startswith('import '):
                    # print("import line:", line)
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
                        wd_list = t.split(",")
                        for i, val in enumerate(wd_list):
                            wd_list[i] = val.split(".")[0]
                        # update_frequency_dictionary([t], word_dir)
                    else:
                        # print("Error 0001!")
                        # print("line=", line)
                        pass

                    if wd_list:
                        update_frequency_dictionary(wd_list, word_dir)

                # skipped some line, eg from_name = "D{}".format(from_index)
                # from 5 minutes to 1 minute, then restart Monit service with delaying 10 seconds.
                if line.startswith('from ') and line.find('import') > 7:
                    # print("from line:", line)
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
        print("????????????????????????????????????????????????")


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
    ????????????
    :param:
        fileName: ???????????????
    :return: ???????????????
    """
    linesCount = 0
    try:
        with open(fileName, "r", encoding='utf-8') as f:
            for line in f:
                linesCount += 1
        return linesCount
    except IOError:
        print("????????????????????????????????????????????????")


def RecurveDir(dirPath):
    """
    ?????????????????????????????????
    :param:
        dirPath: ???????????????
    :return: ?????????????????????
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
    ???????????????????????????
    :param
        Path: ?????????????????????
    :return: None
    """
    cnt = 0
    path_dir_list = []
    g_wd_list = []
    fileList = RecurveDir(Path)
    for file in fileList:
        # print(file)
        if not file.endswith('.py'):
            continue
        cnt += 1
        # if cnt > 10:
        #     break

        # if file.find("test_reporting") != -1:
        #         # or file.find("tests") != -1:
        #     continue

        # if file.find("tests") != -1:
        #     pass
        # else:
        #     continue

        # wordsCount = WordCount(file)
        # linesCount = LineCount(file)
        # charsCount = CharCount(file)
        # print("%s ???????????????\n???????????????%s\n???????????????%s\n?????????%s\n" % (file, charsCount, wordsCount, linesCount))
        wd_list = word_count(file)
        # print("wd_list:", wd_list)  # debug
        g_wd_list.extend(wd_list)

        word_dir = check_import_modules(file)
        # print(word_dir)

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

    print("Summary module:")
    print_frequency_dictionary(summary_dir)

    # wd_dir = Counter(g_wd_list)
    # print(wd_dir)
    summary_wd_dir = {}
    update_frequency_dictionary(g_wd_list, summary_wd_dir)
    # print("Summary word:")
    # print_frequency_dictionary(summary_wd_dir)

    print("keyword:")
    kw_dir = {}
    for i, val in enumerate(g_kwlist):
        tmp_val = summary_wd_dir.get(val)
        if tmp_val:
            kw_dir[val] = tmp_val
    print(kw_dir)

    print("builtins:")
    builtins_dir = {}
    for i, val in enumerate(g_builtins_list):
        tmp_val = summary_wd_dir.get(val)
        if tmp_val:
            builtins_dir[val] = tmp_val
    print(builtins_dir)


def CCBCountMain(fileName):
    """
    ??????????????????????????????????????????????????????
    :param
        fileName??????????????????
    :return: None
    """
    # ???????????????
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
    ?????????????????????????????????????????????????????????
    :param
        fileName??????????????????
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
                # ??????????????????????????????
                if not isComment:
                    if stripLine.startswith("'''") or stripLine.startswith('"""') or stripLine.startswith('/*'):
                        isComment = True
                        startComment = index
                    # ?????????????????????????????????
                    elif stripLine.startswith('#') or stripLine.startswith('//') or re.findall('^[}]+[\s\S]+[//]+',
                                                                                               stripLine):
                        commentLines += 1
                    elif stripLine == '' or stripLine == '{' or stripLine == '}':
                        blankLines += 1
                    else:
                        codeLines += 1
                # ????????????????????????
                else:
                    if stripLine.endswith("'''") or stripLine.endswith('"""') or stripLine.endswith('*/'):
                        isComment = False
                        commentLines += index - startComment + 1
                    else:
                        pass
        print("%s ???????????????\n????????????????????????%s\n????????????????????????%s\n????????????????????????%s\n" % (fileName, codeLines, blankLines, commentLines))
    except IOError:
        print("??????????????????????????????????????????????????????")


if __name__ == '__main__':
    main()
