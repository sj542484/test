#!/usr/bin/env python
# encoding:UTF-8


def get_size(self):
    x = self.driver.get_window_size()['width']
    y = self.driver.get_window_size()['height']
    return x, y


def click_bounds(self, location_x, location_y):
    # 获取当前手机屏幕大小X,Y
    screen = get_size(self)
    # 设定系数
    a = location_x / screen[0]
    b = location_y / screen[1]
    # 屏幕坐标乘以系数即为用户要点击位置的具体坐标
    self.driver.tap([(a * screen[0], b * screen[1])])


def ClickBounds(self, location_x, location_y, screen_x=375, screen_y=667):
    # 获取当前手机屏幕大小X,Y
    screen = get_size(self)
    # 设定系数
    a = location_x / screen[0]
    b = location_y / screen[1]
    # 屏幕坐标乘以系数即为用户要点击位置的具体坐标
    self.driver.tap([(a * screen[0], b * screen[1])])


def games_keyboard(self, key):
    """小键盘 q w e等字母"""
    key = key.lower()
    keyboard = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
                'c', 'v', 'b', 'n', 'm', "'", ' ']
    if key in keyboard:
        i = keyboard.index(key.lower())
        if i < 10:
            click_bounds(self, 24 + i * 40, 550)
        elif i in range(10, 19):
            click_bounds(self, 45 + (i - 10) * 40, 600)
        elif i in range(19, 26):
            click_bounds(self, 85 + (i - 19) * 40, 650)
        elif i == 26:  # '
            click_bounds(self, 310, 700)
        elif i == 27:
            click_bounds(self, 205, 705)


def guess_keyboard(self, key):
    """小键盘 q w e等字母"""
    screen = get_size(self)
    keyboard = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'd', 'k', 'l', 'z', 'x',
                'c', 'v', 'b', 'n', 'm']
    if key in keyboard:
        i = keyboard.index(key.lower())
        if i < 10:
            click_bounds(self, 25 + i * 40, 605)
        elif i in range(10, 19):
            click_bounds(self, 45 + (i - 10) * 40, 657)
        elif i in range(19, 26):
            click_bounds(self, 85 + (i - 19) * 40, 710)
