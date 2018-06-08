# -*- coding: utf-8 -*-
import json
from PIL import Image
from struct import *

xiang_su_pin_lv = {}
jie_dian_list = []
bian_ma_biao = {}


class node:
    """
    构造用以表示节点的类
    """

    def __init__(self, right=None, left=None, parent=None, weight=0,
                 code=None):  # 节点构造方法
        self.left = left
        self.right = right
        self.parent = parent
        self.weight = weight
        self.code = code


def picture_convert():
    """
    此函数完成将bmp图片转换为灰值图
    :return:
    """
    picture = Image.open('./original_photo.jpg')
    # print '====', picture.mode    # RGBA
    pic = picture.convert('L')
    # L = R * 299/1000 + G * 587/1000+ B * 114/1000 依据此公式将RGBA图像转换为L图像
    pic.save('gray_photo.bmp')
    return pic  # 返回转换后的图片对象


def pixel_frequency_statistics(list):
    """
    统计每个像素出现的次数
    :param list:
    :return:
    """
    global xiang_su_pin_lv
    for i in list:
        if i not in xiang_su_pin_lv.keys():
            xiang_su_pin_lv[i] = 1  # 若此像素点不在字符频率字典里则直接添加
        else:
            xiang_su_pin_lv[i] += 1  # 若存在在字符频率字典里则对应值加一
    return xiang_su_pin_lv


def construct_leaf_nodes(xiang_su_zhi):
    """
    构造叶子节点，分别赋予其像素点的值和像素点的权重
    code = 像素点的值
    weight = 像素点的权重
    :param xiang_su_zhi:
    :return:
    """
    nodes_list = [node(weight=xiang_su_zhi[i][1], code=str(xiang_su_zhi[i][0]))
                  for i in range(len(xiang_su_zhi))]
    # print node_list.__len__()    # 256
    # print node_list[0].code, node_list[0].weight   # 255 26
    return nodes_list


def sort_by_weight(list_node):
    """
    根据每个叶子结点的权重对叶子结点列表进行排序
    :param list_node:
    :return:
    """
    list_node = sorted(list_node, key=lambda node: node.weight)
    return list_node


def huffman_tree(listnode):
    """
    根据叶子结点列表，生成对应的霍夫曼编码树
    :param listnode:
    :return:
    """
    listnode = sort_by_weight(listnode)
    # x = []
    # for i in listnode:
    #     x.append(i.weight)
    # print '我就想看看---', x   # return  [26, 57, 58, 62, 63, 64, 64, 65, ...]
    # print '我就想看看---', sum(x)    # return 252000

    while len(listnode) != 1:
        low_node0, low_node1 = listnode[0], listnode[1]  # 每次取最小权值的两个像素点进行合并
        new_change_node = node()
        new_change_node.weight = low_node0.weight + low_node1.weight
        new_change_node.left = low_node0
        new_change_node.right = low_node1
        low_node0.parent = new_change_node
        low_node1.parent = new_change_node
        # remove() 函数用于移除列表中某个值的第一个匹配项
        listnode.remove(low_node0)
        listnode.remove(low_node1)
        listnode.append(new_change_node)
        listnode = sort_by_weight(listnode)
    return listnode  # 返回头结点


def binary_huffman_encode(picture):
    """
    编码函数，返回编码表以及编码结果
    :param picture:
    :return:
    """
    # print '==size===', picture.size   # 420(width) * 600(height) = 252000
    width = picture.size[0]
    height = picture.size[1]
    im = picture.load()  # 为图像分配内存并从文件中加载它
    print "像素点个数为：{0}(width) * {1}(height) = {2}".format(width, height,
                                                         width * height)

    # 将像素点保存在列表中进行频率统计; im[i, j]表示为像素点的灰色值
    list = [im[i, j] for i in range(width) for j in range(height)]

    # 统计每个像素出现的次数
    xiang_su = pixel_frequency_statistics(list)

    # 以频数从小到大将像素进行排序，频数作为节点的权重 return [(像素， 频数), ()]
    # ########其实此处已经根据权重排序了, sort_by_weight()函数也是做这个事#####
    xiang_su = sorted(xiang_su.items(), key=lambda item: item[1])

    # 构造叶子节点
    leaf_nodes_list = construct_leaf_nodes(xiang_su)

    # 根据叶子结点列表，生成对应的霍夫曼编码树
    head = huffman_tree(leaf_nodes_list)[0]  # 保存编码树的头结点return <node instance>

    # TODO:huffman 编码规则的正确性，不同角度去理解
    global bian_ma_biao
    # 遍历所有的叶子节点，卓一为huffman 树进行编码
    for e in leaf_nodes_list:  # 构造编码表
        new_change_node = e
        bian_ma_biao.setdefault(e.code, "")
        while new_change_node != head:
            if new_change_node.parent.left == new_change_node:
                bian_ma_biao[e.code] = "1" + bian_ma_biao[e.code]
            else:
                bian_ma_biao[e.code] = "0" + bian_ma_biao[e.code]
            new_change_node = new_change_node.parent
    for key in bian_ma_biao.keys():
        print "信源像素点 {0} Huffman编码后的码字为： {1}".format(key, bian_ma_biao[key])
    result = ''  # 编码结果，对每个像素点进行霍夫曼编码
    for i in range(width):
        for j in range(height):
            for key, values in bian_ma_biao.iteritems():
                if str(im[i, j]) == key:
                    result = result + values
    with open('result.txt', 'w') as f:
        f.write(result)
    with open('bian_ma_biao.json', 'w') as fb:
        js = json.dumps(bian_ma_biao)
        fb.write(js)
    print "您的编码表为:", bian_ma_biao


def switch_byte(erjinzhi, char=00000000):
    for j in range(8):
        if erjinzhi[j] == '1':
            if j == 7:
                char += 1
            else:
                char += 1
                char = char << 1
        if erjinzhi[j] == "0":
            if j == 7:
                pass
            else:
                char = char << 1
    return char


def byte_xie_ru():
    """
    由于霍夫曼编码结果为string类型，此时应将其转为byte保存，此函数完成将编码结果的字节存入
    :return:
    """
    with open('result.txt', 'r') as f:
        # 读取文件第一行数据并删除其中的换行符
        p = f.readlines()[0].strip('\n')   # da= f.readlines()返回的是列表；
    str = p
    # print '还想看看===', p.__len__()
    yu_shu = 8 - p.__len__() % 8
    with open("huffman_compress.txt", "wb") as f:
        for i in range(0, str.__len__(), 8):
            if i + 8 > str.__len__():
                erjinzhi = str[i:]
                # print erjinzhi  # return 10010
                # print yu_shu  # return  3
                buling = ''
                for i in range(yu_shu):
                    buling = buling + '0'
                erjinzhi = buling + erjinzhi  # return 00010010
                char = switch_byte(erjinzhi)
                f.write(pack("B", char))
                break
            erjinzhi = str[i:i + 8]
            char = switch_byte(erjinzhi)
            f.write(pack("B", char))
        f.write(pack('B', yu_shu))
    print "您的编码已经完成：二元霍夫曼编码结果已经存到huffman_compress.txt中"


if __name__ == '__main__':
    binary_huffman_encode(picture_convert())
    byte_xie_ru()
