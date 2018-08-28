#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/6/5'
# ----------Dragon be here!----------
              ┏━┓      ┏━┓
            ┏━┛ ┻━━━━━━┛ ┻━━┓
            ┃       ━       ┃
            ┃  ━┳━┛   ┗━┳━  ┃
            ┃       ┻       ┃
            ┗━━━┓      ┏━━━━┛
                ┃      ┃神兽保佑
                ┃      ┃永无BUG！
                ┃      ┗━━━━━━━━━┓
                ┃                ┣━┓
                ┃                ┏━┛
                ┗━━┓ ┓ ┏━━━┳━┓ ┏━┛
                   ┃ ┫ ┫   ┃ ┫ ┫
                   ┗━┻━┛   ┗━┻━┛
"""
from PIL import Image


# 等比例压缩图片
def resizeImg(**args):
	args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 75}
	arg = {}
	for key in args_key:
		if key in args:
			arg[key] = args[key]
	im = Image.open(arg['ori_img'])
	ori_w, ori_h = im.size
	widthRatio = heightRatio = None
	ratio = 1
	if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
		if arg['dst_w'] and ori_w > arg['dst_w']:
			widthRatio = float(arg['dst_w']) / ori_w  # 正确获取小数的方式
		if arg['dst_h'] and ori_h > arg['dst_h']:
			heightRatio = float(arg['dst_h']) / ori_h

		if widthRatio and heightRatio:
			if widthRatio < heightRatio:
				ratio = widthRatio
			else:
				ratio = heightRatio

		if widthRatio and not heightRatio:
			ratio = widthRatio
		if heightRatio and not widthRatio:
			ratio = heightRatio

		newWidth = int(ori_w * ratio)
		newHeight = int(ori_h * ratio)
	else:
		newWidth = ori_w
		newHeight = ori_h

	im.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])

if __name__ == '__main__':

	# 源图片
	ori_img = 'E:/html/lianxi/img/DSC_1867.JPG'
	# 目标图片
	dst_img = 'E:/html/lianxi/img/ys/ys.png'
	# 目标图片大小
	dst_w = 94
	dst_h = 94
	# 保存的图片质量
	save_q = 35
	# 等比例压缩
	resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
