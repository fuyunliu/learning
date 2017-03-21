
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class BaseGeetestCrack:

    def __init__(self, driver, captcha_class, slider_class):
        self.driver = driver
        self.captcha_class = captcha_class
        self.slider_class = slider_class

    def calculate_slider_offset(self):

        img1 = self.crop_captcha_image(name='img1.png')
        self.drag_and_drop(x_offset=5)
        img2 = self.crop_captcha_image(name='img2.png')
        w1, h1 = img1.size
        w2, h2 = img2.size
        assert w1 == w2, h1 == h2

        values = set()
        for i in range(w1):
            for j in range(h1):
                pix1 = img1.load()[i, j]
                pix2 = img2.load()[i, j]
                x = abs(pix1[0] - pix2[0])
                y = abs(pix1[1] - pix2[1])
                z = abs(pix1[2] - pix2[2])
                if x > 60 and y > 60 and z > 60:
                    values.add(i)

        slider_offset = max(values) - 42 - 5
        return slider_offset

    def crop_captcha_image(self, element_class=None, name=None):
        element_class = self.captcha_class
        ele = self.driver.find_element_by_class_name(element_class)
        location = ele.location
        size = ele.size
        left = int(location['x'])
        top = int(location['y'])
        right = left + int(size['width'])
        bottom = top + int(size['height'])

        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))

        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def drag_and_drop(self, x_offset, y_offset=0, element_class=None):

        element_class = self.slider_class
        dragger = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
        time.sleep(5)

    def crack(self):
        x_offset = self.calculate_slider_offset()
        print(x_offset)
        self.drag_and_drop(x_offset)
        self.drag_and_drop(x_offset + 5)
        self.drag_and_drop(x_offset - 5)


def main():
    url = "http://www.geetest.com/exp_embed"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get(url)
    time.sleep(5)
    cracker = BaseGeetestCrack(driver, 'gt_cut_fullbg', 'gt_slider_knob')
    cracker.crack()
    driver.quit()


if __name__ == "__main__":
    main()
