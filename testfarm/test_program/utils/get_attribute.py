#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep


class GetAttribute(BasePage):
    """获取元素属性"""

    @teststep
    def class_name(self, var):
        """元素 class_name属性值"""
        value = var.get_attribute("className")
        return value

    @teststep
    def resource_id(self, var):
        """元素 resource-id属性值"""
        value = var.get_attribute("resourceId")
        return value

    @teststep
    def selected(self, var):
        """元素 selected属性值"""
        value = var.get_attribute('selected')
        return value

    @teststep
    def checked(self, var):
        """元素 checked属性值"""
        value = var.get_attribute('checked')
        return value

    @teststep
    def enabled(self, var):
        """元素 enabled属性值"""
        value = var.get_attribute('enabled')
        return value

    @teststep
    def description(self, var):
        """元素 content_description属性值"""
        value = var.get_attribute('contentDescription')
        return value
