import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import keyboard
import requests
import json
import threading


def browser_initial(id):
    """"
    进行浏览器初始化
    """
    url = get_info_url(id)
    browser = webdriver.Chrome()
    goal_url = url  # 未携带cookies打开网页
    browser.get('https://live.bilibili.com/24978909?live_from=84002&spm_id_from=333.337.0.0')
    return goal_url, browser


def start_web(id):
    tur = browser_initial(id)
    goal_url = tur[0]
    browser = tur[1]
    with open('cookie_xiaohao.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    for cookie in listCookies:
        cookie_dict = {
            'domain': 'bilibili.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'path': '/',
            "expires": '',
            'sameSite': 'None',
            'secure': cookie.get('secure')
        }
        browser.add_cookie(cookie_dict)
    # 更新cookies后进入目标网页
    browser.get(goal_url)
    time.sleep(4)
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="live-player"]/div[10]'))
    )
    element.click()

    while check_live(id):
        print(f'{id}正在直播')
        begin_recode()
        time.sleep(180)

    end_recode()


recording_started = None


def begin_recode():
    global recording_started
    if not recording_started:
        pyautogui.press('F6')
        recording_started = True


def end_recode():
    global recording_started
    recording_started = False
    pyautogui.press('F6')


def get_info_url(id):
    url = f'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie': 'buvid_fp_plain=undefined; i-wanna-go-back=-1; buvid4=3A8B56F1-EDA5-71EF-4695-376711789D2885279-022101300-3SvbbFkocEboIDHoVtJIDA%3D%3D; is-2022-channel=1; DedeUserID=12310947; DedeUserID__ckMd5=99ff7d744bdbd759; hit-new-style-dyn=1; _uuid=4E4EFBA7-9B2D-C25E-1483-6DE48710F7B8E42648infoc; enable_web_push=DISABLE; header_theme_version=CLOSE; buvid3=37A8CC2D-25BD-E2A9-32C5-DC9E919079F867049infoc; b_nut=1699776965; LIVE_BUVID=AUTO5817028189331843; rpdid=|(J|)Y)RJ~k|0J\'u~|JuJmm|Y; hit-dyn-v2=1; CURRENT_BLACKGAP=0; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1721915756,1722090799,1722200745,1722201812; SESSDATA=066ec50f%2C1737915515%2Ca0c98%2A71CjBQTt97-5dX1-S7ovnlYiLvrfx63TeYtmSJ8NoGED6QqmCBuMMVoGvDbIeJbFxZ3g8SVmtSQ1VFV3h3OWpwSGhWVURHT2dCNS1xZFBXRWZ4OTY3elhZaEVaQ25LYXY0OGVNbDVhc085UmlfdVpXVkhvcHN0eE5hODN6dkJQMklacFhqbXBFeTJRIIEC; bili_jct=9f56f20e78e1adb4329cbf02d5363623; sid=7mupwl6f; fingerprint=79e15e94b2668d44896fd326b7d83e5e; CURRENT_FNVAL=16; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI4MDkyMTgsImlhdCI6MTcyMjU0OTk1OCwicGx0IjotMX0.urmNEJ4Les-dEQhEATSYHOI63f3a9Hj8SiPeFlxSlkI; bili_ticket_expires=1722809158; browser_resolution=1327-754; home_feed_column=4; CURRENT_QUALITY=80; bp_t_offset_12310947=961084526883241984; buvid_fp=79e15e94b2668d44896fd326b7d83e5e; PVID=8; b_lsid=426C436D_191138F6297'
    }
    r = requests.get(url, headers=headers)
    rs = r.json()
    return rs["data"]['link']


def check_live(id):
    url = f'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie': 'buvid_fp_plain=undefined; i-wanna-go-back=-1; buvid4=3A8B56F1-EDA5-71EF-4695-376711789D2885279-022101300-3SvbbFkocEboIDHoVtJIDA%3D%3D; is-2022-channel=1; DedeUserID=12310947; DedeUserID__ckMd5=99ff7d744bdbd759; hit-new-style-dyn=1; _uuid=4E4EFBA7-9B2D-C25E-1483-6DE48710F7B8E42648infoc; enable_web_push=DISABLE; header_theme_version=CLOSE; buvid3=37A8CC2D-25BD-E2A9-32C5-DC9E919079F867049infoc; b_nut=1699776965; LIVE_BUVID=AUTO5817028189331843; rpdid=|(J|)Y)RJ~k|0J\'u~|JuJmm|Y; hit-dyn-v2=1; CURRENT_BLACKGAP=0; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1721915756,1722090799,1722200745,1722201812; SESSDATA=066ec50f%2C1737915515%2Ca0c98%2A71CjBQTt97-5dX1-S7ovnlYiLvrfx63TeYtmSJ8NoGED6QqmCBuMMVoGvDbIeJbFxZ3g8SVmtSQ1VFV3h3OWpwSGhWVURHT2dCNS1xZFBXRWZ4OTY3elhZaEVaQ25LYXY0OGVNbDVhc085UmlfdVpXVkhvcHN0eE5hODN6dkJQMklacFhqbXBFeTJRIIEC; bili_jct=9f56f20e78e1adb4329cbf02d5363623; sid=7mupwl6f; fingerprint=79e15e94b2668d44896fd326b7d83e5e; CURRENT_FNVAL=16; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI4MDkyMTgsImlhdCI6MTcyMjU0OTk1OCwicGx0IjotMX0.urmNEJ4Les-dEQhEATSYHOI63f3a9Hj8SiPeFlxSlkI; bili_ticket_expires=1722809158; browser_resolution=1327-754; home_feed_column=4; CURRENT_QUALITY=80; bp_t_offset_12310947=961084526883241984; buvid_fp=79e15e94b2668d44896fd326b7d83e5e; PVID=8; b_lsid=426C436D_191138F6297'
    }
    r = requests.get(url, headers=headers)
    rs = r.json()
    if rs["data"]["liveStatus"] == 1:
        return True
    else:
        print(rs["data"])
        return None


from datetime import datetime


def main_check(id):
    while True:
        current_time = datetime.now()
        hour = current_time.hour

        if 0 <= hour < 7:
            # 晚上0点到10点，每3小时检测一次
            print(f'当前时间：{current_time}, 晚上0点到10点，每3小时检测一次')
            if check_live(id):
                start_web(id)
            else:
                print(f'{id}未开播')
                time.sleep(3 * 60 * 60)  # 3小时，单位是秒

        elif 7 <= hour < 23:
            # 早上10点到晚上23点，每5分钟检测一次
            print(f'当前时间：{current_time}, 早上10点到晚上23点，每5分钟检测一次')
            if check_live(id):
                start_web(id)
            else:
                print(f'{id}未开播')
                time.sleep(5 * 60)  # 5分钟，单位是秒

        else:
            # 其余时间，每1小时检测一次
            print(f'当前时间：{current_time}, 其余时间，每1小时检测一次')
            if check_live(id):
                start_web(id)
            else:
                print(f'{id}未开播')
                time.sleep(60 * 60)  # 1小时，单位是秒


if __name__ == '__main__':
    print('tmkk 1096034982')
    print('taf 1265680561')
    id = input()
    main_check(id)

    # tmkk 1096034982
    # taf 1265680561
