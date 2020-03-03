#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from conf.base_page import BasePage
from conf.decorator import teststeps


class Element(BasePage):
    """获取 元素 大小及坐标"""

    @teststeps
    def get_element_size(self, ele):
        """获取元素 width & height"""
        width = ele.size['width']
        height = ele.size['height']
        return width, height

    @teststeps
    def get_element_location(self, ele):
        """获取元素坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    @teststeps
    def get_element_bounds(self, element):
        """获取元素 左上角/中心点/右下角的坐标值"""
        loc = self.get_element_location(element)
        size = self.get_element_size(element)

        x_left = loc[0]
        y_up = loc[1]
        x_center = loc[0] + size[0] / 2
        y_center = loc[1] + size[1] / 2
        x_right = loc[0] + size[0]
        y_down = loc[1] + size[1]

        return x_left, y_up, x_center, y_center, x_right, y_down
