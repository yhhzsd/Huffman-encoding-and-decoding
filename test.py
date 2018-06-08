# -*- coding: utf-8 -*-
from PIL import Image


def merge(im1, im2):
    width = min(im1.size[0], im2.size[0])
    height = min(im1.size[1], im2.size[1])
    im_new = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            r1, g1, b1 = im1.getpixel((x, y))
            r2, g2, b2 = im2.getpixel((x, y))
            r = r1 + r2
            g = g1 + g2
            b = b1 + b2
            im_new.putpixel((x, y), (r, g, b))
    im_new.save('hecheng_photo' + '.bmp')
    print '合成成功！！'


im1 = Image.open('./original_photo.jpg')
pic1 = im1.convert('L')
pic1.save('1.bmp')
im2 = Image.open('./2.jpg')
pic2 = im2.convert('L')
pic2.save('2.bmp')
merge(pic1, pic2)
