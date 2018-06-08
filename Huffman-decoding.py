# -*- coding: utf-8 -*-
import json
from PIL import Image
from struct import *

with open('bian_ma_biao.json', 'r') as fb:
    js = fb.read()
    bian_ma_biao = json.loads(js)


def zi_jie_du_qu(qqqq):
    """
    根据霍夫曼编码生成的txt文件读取其中的字节恢复为字符串形式的编码结果
    :param qqqq:
    :return:
    """
    with open('result.txt', 'r') as p:
        pppp = p.readlines()[0].strip('\n')

    with open('huffman_decomressed.txt', 'w') as fff:
        l = ((pppp.__len__() - pppp.__len__() % 8) / 8) + 2
        list = []
        for i in range(l):
            with open(str(qqqq), "rb") as file:
                file.seek(i)  #
                (a,) = unpack("B", file.read(1))
                list.append(a)
        result = ''
        for i in range(len(list) - 2):
            buling = ''
            for j in range(8 - len(bin(list[i])[2:])):
                buling = buling + '0'
            erjinzhi = buling + bin(list[i])[2:]
            result = result + erjinzhi
        yu_shu = 8 - list[-1]
        last = bin(list[-2])[2:]
        if last.__len__() != yu_shu:
            buling = ''
            for j in range(8 - yu_shu - last.__len__()):
                buling = buling + '0'
            erjinzhi = buling + bin(list[-2])[2:]
            result = result + erjinzhi
        if last.__len__() == yu_shu:
            result = result + bin(list[-2])[2:]
        fff.write(result)


def binary_huffman_decode(kuan, gao):
    """
    二元霍夫曼译码的主函数，通过调用其他函数来还原原始的bmp图像
    :param kuan:
    :param gao:
    :return:
    """
    with open('huffman_decomressed.txt', 'r') as f:
        zifuchuan = f.readlines()[0].strip('\n')
    i = 0
    sao_miao = ''
    huan_yuan_xiang_su = []
    while i != zifuchuan.__len__():  # 利用编码表进行译码
        sao_miao = sao_miao + zifuchuan[i]
        for key in bian_ma_biao.keys():
            if sao_miao == bian_ma_biao[key]:
                huan_yuan_xiang_su.append(key)
                sao_miao = ''
                break
        i += 1
    x = kuan
    y = gao
    c = Image.new('L', (x, y))
    k = 0
    for i in range(x):
        for j in range(y):
            c.putpixel((i, j), (int(huan_yuan_xiang_su[k])))
            k += 1
    c.save('huffman_restore_photo' + '.bmp')
    print "您的译码已经完成：" + "图片存储为huffman_restore_photo.bmp"


if __name__ == '__main__':
    file = raw_input("请您输入进行二元霍夫曼译码的文件名：")
    zi_jie_du_qu(file)
    kuan = int(raw_input("请您输入需要还原的图片的宽："))
    gao = int(raw_input("请您输入需要还原的图片的高："))
    binary_huffman_decode(kuan, gao)
