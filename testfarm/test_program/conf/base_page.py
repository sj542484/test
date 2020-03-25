import time,os,subprocess,re
from selenium.webdriver.support.wait import WebDriverWait
from conf.base_config import GetVariable as gv
import yaml
from utils.get_attribute import GetAttribute


class BasePage(object):

    attr = GetAttribute()

    @classmethod
    def set_assert(cls, base_assert):
        cls.base_assert = base_assert

    def get_assert(self):
        return self.base_assert

    @classmethod
    def set_driver(cls, dri):
        cls.driver = dri

    @classmethod
    def set_user(cls, deviceName):
        """获取用户"""
        cls.deviceName = deviceName

    def get_user_info(self):
        """获取改用户信息"""
        print(os.getcwd())
        fp = open('./testfarm/test_program/conf/user_info.yaml', 'r', encoding='utf-8')
        res = fp.read()
        res = yaml.full_load(res)
        return res['userinfo'][self.deviceName]

    @classmethod
    def set_path(cls, path):
        """报告路径"""
        cls.report_path = path

    def get_driver(self):
        return self.driver

    def get_path(self):
        return self.report_path

    @classmethod
    def id_type(cls):
        return str(gv.ID_TYPE)

    @classmethod
    def set_window_size(cls, uuid):
        """获取当前窗口大小"""
        res = subprocess.Popen('adb -s %s shell dumpsys window displays' % (uuid), shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, close_fds=True)
        result, err = res.communicate()
        a = str(result, 'utf-8')

        cap_one = re.compile('cur=(\d+)x(\d+) ')
        res = cap_one.findall(a)
        cls.window_size = [int(i) for i in res[0]]

    def get_window_size(self):
        # print('获取尺寸：', self.driver.get_window_size())

        return [self.driver.get_window_size()['width'], self.driver.get_window_size()['height']]

    def click_back_up_button(self):
        """以“返回按钮”的class name为依据"""
        time.sleep(1)
        ele = self.driver.find_elements_by_class_name("android.widget.ImageButton")[0]
        ele.click()

    def wait_activity(self):
        """获取当前窗口活动类"""
        activity = self.driver.current_activity
        return activity

    def page_source_android(self):
        """以“获取page_source”的TEXT为依据"""
        print('打开：', self.driver.page_source)

    def screen_swipe_left(self, a, b, c, steps=0.5):
        """向左侧滑动"""
        screen = self.get_window_size()
        x1 = int(int(screen[0]) * a)
        y1 = int(int(screen[1]) * b)
        x2 = int(int(screen[0]) * c)
        self.driver.swipe(x1, y1, x2, y1, steps)

    def screen_swipe_right(self, a, b, c, steps=0.5):
        """向右侧滑动"""
        screen = self.get_window_size()
        x1 = int(int(screen[0]) * a)
        y1 = int(int(screen[1]) * b)
        x2 = int(int(screen[0]) * c)
        self.driver.swipe(x1, y1, x2, y1, steps)

    def screen_swipe_up(self, a, b, c, steps=0.5):
        """向上/向下滑动"""
        screen = self.get_window_size()
        x1 = int(int(screen[0]) * a)
        y1 = int(int(screen[1]) * b)
        y2 = int(int(screen[1]) * c)
        self.driver.swipe(x1, y1, x1, y2, steps)
        print('页面滑动:',x1,y1,x1,y2)
        time.sleep(1)

    def screen_swipe_down(self, a, b, c, steps=0.5):
        """向下滑动"""
        screen = self.get_window_size()
        x1 = int(int(screen[0]) * a)
        y1 = int(int(screen[1]) * b)
        y2 = int(int(screen[1]) * c)
        self.driver.swipe(x1, y1, x1, y2, steps)

    def get_element_location(self, ele):
        """获取元素 顶点坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    def get_element_size(self, ele):
        """获取元素 width & height"""
        width = ele.size['width']
        height = ele.size['height']
        return width, height

    def is_chinese(self, item):
        """判断一个unicode是否是汉字"""
        if u'\u4e00' <= item <= u'\u9fa5':
            return True
        else:
            return False

    def is_alphabet(self, item):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= item <= u'\u005a') or (u'\u0061' <= item <= u'\u007a'):
            return True
        else:
            return False

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

    def swipe_up_ele(self, element=None, steps=10):
        """
        swipe up
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

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

        self.driver \
            .swipe(from_x, from_y, to_x, to_y, steps)

    def swipe_down_ele(self, element=None, steps=10):
        """
        swipe down
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

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

    def swipe_left_ele(self, element=None, steps=10):
        """
        swipe left
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

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

    def swipe_right_ele(self, element=None, steps=10):
        """
        swipe right
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

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

    def find_element(self, element):
        """判断元素是否存在"""
        try:
            self.driver \
                .find_element_by_id(element)
            return True
        except:
            return False

    def get_wait_check_page_result(self, locator, timeout=15):
        """页面检查点判断方法"""
        try:
            WebDriverWait(self.driver, timeout, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    def tearDown(self, ass, my_toast, ass_result):
        """统计错误情况"""
        errors = ass.get_error() + my_toast.get_error()
        if errors:
            ass_result.addFailure(self, errors[0])

