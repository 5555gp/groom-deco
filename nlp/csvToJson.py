# -*- coding: utf-8 -*-
#  将读取的xls格式PIO信息转换成JSON,方便后面使用
# 2018.6.5 Pearl
import json
import os
import csv
import pandas as pd


def csvToJson(filePath):
    """
    将读取的xls格式PIO信息转换成JSON，调整格式
    :param filePath: PIO表格文件的地址
    :return:返回存储文件的地址
    """
    resultJSON = {}  # 整篇文章转换成JSON的结果
    resContent = []  # 参考文献列表（PIO的内容）
    strLine = []  # 当前这一行内容
    strNow = {}  # 当前读取的参考文献的所有PIO内容
    strKeyNow = ''

    try:
        rd = csv.reader(open(filePath, encoding='utf-8'))
    except:
        rd = csv.reader(open(filePath))
    filename = os.path.splitext(filePath)
    resultJSON['filename'] = filename

    i = 0  # 标记文件中包含的参考文献数量
    for strLine in rd:
        if strLine[1] is '' and strNow:  # 当前行的value值为空，且strNow不为空，将strNow添加到参考文献列表中
            resContent.append(strNow)
            i += 1
            strNow = {}
        if strLine[0] is not '' and strLine[1] is not '':  # 当前行key不为空，创建一个新的键值对
            strNow[strLine[0]] = strLine[1]
            strKeyNow = strLine[0]
        if strLine[0] is not '' and strLine[1] is '':  # 当前行key值不为空，value值为空 ，则该行是文章title
            strNow['Title'] = strLine[0]
            strKeyNow = 'Title'
        elif strLine[0] is '':  # 当前行key为空，将value拼接到上一个value
            strNow[strKeyNow] += strLine[1]

    resContent.append(strNow)
    i += 1

    resultJSON['content'] = resContent
    json_str = json.dumps(resultJSON)
    resultPath = filePath + '.json'
    with open(resultPath, "w") as f:
        f.write(json_str)
    print(resultPath)
    return resultPath




if __name__ == '__main__':
    filePath = 'C:\\Users\TenYun\Desktop\groom\papers\\25935004.csv'
    csvToJson(filePath)
