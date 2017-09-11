#!/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'skyeagle'

import re
from collections import deque


class CifFile(object):
    """
    读取cif文件中的data block
    """

    @classmethod
    def from_string(cls, string):
        # 一个cif文件中可能有多个data block（block的开头固定为data_)
        # 下面的循环通过正则表达式将多个data block分开
        for x in re.split("^\s*data_", string, flags=re.MULTILINE | re.DOTALL)[1:]:
            # 包含powder_pattern的data block没有包含任何结构信息，跳过这个data block
            if 'powder_pattern' in re.split("\n", x, 1)[0]:
                continue
            c = CifBlock.from_string("data_" + x)

    @classmethod
    def from_file(cls, filename):
        f = open(filename)
        string = f.read()
        f.close()
        return cls.from_string(string)


class CifBlock(object):
    @classmethod
    def from_string(cls, string):
        cls._process_string(string)

    @classmethod
    def _process_string(cls, string):
        # 移除cif中的评论语句，用空白替代,由于其中的\n也被替代，所以相当于删除此行
        # 正则表达式的意思是：非显示字符后面（回车等）或一行开头为#，
        # 后面为“\r\n”之外的任何单个字符，匹配多次，直到这一行的结尾
        string = re.sub("(\s|^)#.*$", "", string, flags=re.MULTILINE)
        # 删除非ａｓｃＩＩ字符
        string = "".join(i for i in string if ord(i) < 128)
        # 删除空白行(只有个回车?)
        string = re.sub("^\s*\n", "", string, flags=re.MULTILINE)

        q = deque()
        multiline = False
        ml = []

        p = re.compile(r'''([^'"\s)][\S]*)|'(.*?)'(?!\S)|"(.*?)"(?!\S)''')

        for l in string.splitlines():
            print(l)
            if multiline:
                if l.startswith(";"):
                    multiline = False
                    q.append(('', '', ''.join(ml)))
                    ml = []
                    l = l[1:].strip()
                else:
                    ml.append(l)
                    continue
            if l.startswith(";"):
                multiline = True
                ml.append(l[1:].strip())
            else:
                for s in p.findall(l):
                    print(s)
                    q.append(s)



CifFile.from_file("Bi2Se3.cif")
