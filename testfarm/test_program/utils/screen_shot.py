#!/usr/bin/env python
# coding=utf-8
import os
import tempfile
import shutil
from functools import reduce
import math
import operator
import time
from PIL import Image

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


class ScreenShot(BasePage):
    def __init__(self):
        self.screen_path = gv.SCREENSHOT_ROOT

    @teststeps
    def get_screenshot_by_element(self, element):
        # 先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        # 获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        # 截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    @teststeps
    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        # 自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    @teststeps
    def write_to_file(self, dirPath, imageName, form="png"):
        # 将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)

        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))

    @teststeps
    def load_image(self, image_path):
        # 加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" % image_path)

    @teststeps
    def same_as(self, load_image, percent):
        """对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大"""

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2,
                                                         histogram1, histogram2))) / len(histogram1))
        if differ <= percent:  # 图片相同
            return True
        else:  # 图片不同
            return False

    @teststeps
    def get_screenshot(self, element):
        """获取元素截图
        :param element:元素
        """
        img_name = 'img_' + date_time
        if not os.path.exists(self.screen_path):
            os.mkdir(self.screen_path)

        self.get_screenshot_by_element(element).write_to_file(self.screen_path, img_name)
        os.path.isfile(self.screen_path + img_name)

        return self.screen_path + img_name

    @teststeps
    def same_as_screenshot(self, element, image, form="png"):
        """获取修改后元素截图
        :param element:元素
        :param image: 修改前的截图
        """
        img = image + "." + form
        load = self.load_image(img)
        # 要求百分百相似
        result = self.get_screenshot_by_element(element).same_as(load, 0)
        if result:
            print('两截图相同')
        else:
            print('两截图不同')

        return result
