from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json

browser = webdriver.Chrome()
browser.get("https://passport.bilibili.com/login")
flag = True
print("等待登录...")
while flag:
    try:
        browser.find_element(By.XPATH,
                             "//div[@class='user-con signin']|//ul[@class='right-entry']"
                             "//a[@class='header-entry-avatar']")
        flag = False
    except NoSuchElementException as e:
        time.sleep(3)
print("已登录，现在为您保存cookie...")
with open('cookie_xiaohao.txt', 'w', encoding='u8') as f:
    json.dump(browser.get_cookies(), f)
browser.close()
print("cookie保存完成，游览器已自动退出...")
