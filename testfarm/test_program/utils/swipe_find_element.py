#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
from selenium.common.exceptions import WebDriverException

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps
from testfarm.test_program.utils.get_element_bounds import Element


class SwipeFindElement(BasePage):
    """滑屏找元素 操作"""

    def __init__(self):
        self.ele = Element()

    @teststeps
    def _find_element_by_swipe(self, direction, locator, value, element=None, steps=10, max_swipe=6):
        """
        滑屏找到元素
        :param direction: 滑屏方向
        :param locator:  By元素定位方式 "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value:  By元素定位参数，即元素属性
        :param element: 指定待滑动元素
        :param steps: 一次滑动持续时间ms
        :param max_swipe: 滑屏操作最大执行时长
        :return: 元素
        """
        times = max_swipe

        stability_width = 0
        stability_height = 0
        for i in range(times):
            try:
                ele = self.driver.find_element(locator, value)

                width = ele.size['width']
                height = ele.size['height']
                if stability_width != width or stability_height != height:
                    stability_width = width
                    stability_height = height
                    raise WebDriverException
                else:
                    return ele
            except WebDriverException:
                if direction == 'up':
                    self.swipe_up_ele(element=element, steps=steps)
                elif direction == 'down':
                    self.swipe_down_ele(element=element, steps=steps)
                elif direction == 'left':
                    self.swipe_left_ele(element=element, steps=steps)
                elif direction == 'right':
                    self.swipe_right_ele(element=element, steps=steps)

                if i == times - 1:
                    raise WebDriverException

    @teststeps
    def find_element_by_swipe_up(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe up
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('up', locator, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def find_element_by_swipe_down(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe down
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('down', locator, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def find_element_by_swipe_left(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe left
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('left', locator, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def find_element_by_swipe_right(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe right
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('right', locator, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def find_element_on_horizontal(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element on horizontal
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        try:
            return self.find_element_by_swipe_left(locator, value,
                                                   element=element, steps=steps, max_swipe=max_swipe)
        except WebDriverException:
            pass

        return self.find_element_by_swipe_right(locator, value,
                                                element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def find_element_on_vertical(self, locator, value, element=None, steps=10, max_swipe=6):
        """
        find element on vertical
        :param locator: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        try:
            return self.find_element_by_swipe_up(locator, value,
                                                 element=element, steps=steps, max_swipe=max_swipe)
        except WebDriverException:
            pass

        return self.find_element_by_swipe_down(locator, value,
                                               element=element, steps=steps, max_swipe=max_swipe)

    @teststeps
    def swipe_up_ele(self, element=None, steps=10):
        """
        向上滑动元素或者滑屏
        :param element: 待滑动的元素
        :param steps: 持续时间ms
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.ele.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_center
            to_y = y_up
        else:
            x, y = self.get_window_size()
            from_x = 0.5 * x
            from_y = 0.5 * y
            to_x = 0.5 * x
            to_y = 0.25 * y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    @teststeps
    def swipe_down_ele(self, element=None, steps=10):
        """
        向下滑动元素或者滑屏
        :param element: 待滑动的元素
        :param steps: 持续时间ms
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.ele.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_center
            to_y = y_down
        else:
            x, y = self.get_window_size()
            from_x = 0.5 * x
            from_y = 0.5 * y
            to_x = 0.5 * x
            to_y = 0.75 * y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    @teststeps
    def swipe_left_ele(self, element=None, steps=10):
        """
         向左侧滑动元素或者滑屏
        :param element: 待滑动的元素
        :param steps: 持续时间ms
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.ele.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_left
            to_y = y_center
        else:
            x, y = self.get_window_size()
            from_x = 0.5 * x
            from_y = 0.5 * y
            to_x = 0.25 * x
            to_y = 0.5 * y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    @teststeps
    def swipe_right_ele(self, element=None, steps=10):
        """
         向右侧滑动元素或者滑屏
        :param element: 待滑动的元素
        :param steps: 持续时间ms
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.ele.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_right
            to_y = y_center
        else:
            x, y = self.get_window_size()
            from_x = 0.5 * x
            from_y = 0.5 * y
            to_x = 0.75 * x
            to_y = 0.5 * y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

