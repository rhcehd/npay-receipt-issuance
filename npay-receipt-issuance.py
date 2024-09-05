import os
import time
from datetime import datetime

import pyautogui
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait, POLL_FREQUENCY
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver: webdriver.Chrome
wait: WebDriverWait
base_url = "https://order.pay.naver.com/home"
download_path = os.path.join(os.path.join(os.getcwd(), "pdf"))

def initialize_driver():
    global driver, wait
    # Chrome 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    settings = {
        "recentDestinations": [
            {
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    prefs = {
        'printing.print_preview_sticky_settings.appState': settings,
        'savefile.default_directory': download_path  # PDF 파일이 저장될 경로
    }

    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')  # 인쇄 대화상자 자동 확인

    driver_path = ChromeDriverManager().install()
    service = ChromeService(os.path.join(os.path.dirname(driver_path), "chromedriver.exe"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 10)


def start_driver(url: str):
    driver.get(url)
    global current_url
    current_url = driver.current_url


def move_to_last_window():
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[len(window_handles) - 1])


def wait_for_login():
    while True:
        if driver.current_url != current_url:
            break
        time.sleep(1)


def set_filter():
    try:
        search_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.TwoStagedLayoutWrapper-module_container__-NuVi > div > div.TwoStagedLayoutWrapper-module_content-left__2eGzo.PcHome_content-left__1Sj2x > div.PaymentCategoryAndSearchButton_article__3lLC7 > div > div.PaymentCategoryAndSearchButton_area-button__3G-wX > button")
        search_btn.click()
        is_search_modal_showing = True
        while is_search_modal_showing:
            try:
                driver.find_element(By.XPATH, "//*[contains(@id, 'portal__')]/div/div[1]/div[2]/div[5]/button")
            except NoSuchElementException:
                search_tags = driver.find_elements(By.XPATH, "//*[@id='root']/div/div[2]/div/div[1]/div[1]/div/div[2]/div/ul")
                if len(search_tags) != 0:
                    is_search_modal_showing = False
                time.sleep(1)
        return True
    except NoSuchElementException as e:
        return False


def credit_card_receipt():
    purchase_receipt_btn = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div/div[2]")
    purchase_receipt_btn.click()
    time.sleep(1)

    datetime_raw = driver.find_element(By.XPATH, "//*[@id='container']/div/ul/li[2]").text
    date = datetime.strptime(datetime_raw.split('\n')[1], "%Y.%m.%d %H:%M:%S").strftime("%m%d")
    price = driver.find_element(By.XPATH, "//*[@id='container']/div/ul/li[4]/span").text.replace("원", "")
    receipt_count = 1

    receipt_path = os.path.join(download_path, f"{date}_{price}")
    if not os.path.exists(receipt_path):
        os.mkdir(receipt_path)

    print_btn = driver.find_element(By.XPATH, "//*[@id='container']/div/div/button")
    print_btn.click()
    time.sleep(1)
    pyautogui.write(message=f"{receipt_path}\\{date}_{price}_{receipt_count}")
    pyautogui.press('enter')
    pyautogui.press('y')
    receipt_count += 1

    time.sleep(1)
    back_btn = driver.find_element(By.XPATH, "//*[@id='header']/div/a")
    back_btn.click()
    time.sleep(1)
    card_receipt_btns = driver.find_elements(By.CLASS_NAME, "button_area")
    card_receipt_btns = card_receipt_btns[1:]
    for card_receipt_btn in card_receipt_btns:
        card_receipt_btn.find_element(By.XPATH, "a").click()
        time.sleep(1)
        # print_btn = driver.find_element(By.XPATH, "//*[@id='receipt']/div/div[2]/div[2]/button")
        print_btns = driver.find_elements(By.TAG_NAME, "button")
        for btn in print_btns:
            if btn.text == "인쇄하기":
                btn.click()
        time.sleep(1)
        pyautogui.write(message=f"{receipt_path}\\{date}_{price}_{receipt_count}")
        pyautogui.press('enter')
        pyautogui.press('y')
        receipt_count += 1
        time.sleep(1)
        back_btn = driver.find_element(By.XPATH, "//*[@id='receipt']/header/div/div/button")
        back_btn.click()
        time.sleep(1)


def cash_receipt():
    datetime_raw = driver.find_element(By.XPATH, "//*[@id='receipt']/div[2]/div[1]/div[1]/dl/div[5]/dd").text
    date = datetime.strptime(datetime_raw, "%Y.%m.%d %H:%M:%S").strftime("%m%d")
    price = driver.find_element(By.XPATH, "//*[@id='receipt']/div[2]/div[1]/div[4]/div").text

    receipt_path = os.path.join(download_path, f"{date}_{price}")
    if not os.path.exists(receipt_path):
        os.mkdir(receipt_path)

    purchase_receipt_btn = driver.find_element(By.XPATH, "//*[@id='receipt']/div[2]/div[2]/div[2]")
    purchase_receipt_btn.click()
    time.sleep(1)
    pyautogui.write(message=f"{receipt_path}\\{date}_{price}")
    pyautogui.press('enter')
    pyautogui.press('y')


def show_detail():
    receipt_btn = driver.find_element(By.XPATH, "//*[@id='content']/div/div[2]/div/div/button")
    receipt_btn.click()
    time.sleep(1)
    move_to_last_window()
    time.sleep(1)

    element_id = driver.find_element(By.XPATH, "/html/body/div[1]").get_attribute("id")
    if "__next" in element_id:
        cash_receipt()
    elif "header" in element_id:
        credit_card_receipt()
    else:
        NoSuchElementException(msg="detail: neither credit card nor cash")
    time.sleep(1)

    driver.close()
    move_to_last_window()


def a():
    is_filter_set = False
    while not is_filter_set:
        time.sleep(1)
        is_filter_set = set_filter()
    time.sleep(1)

    while True:
        try:
            # show_more_btn = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div[1]/div[3]/div[2]/button")
            show_more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[2]/div/div[1]/div[3]/div[2]/button")))
            show_more_btn.click()
            time.sleep(1)
        except TimeoutException:
            break
        # except NoSuchElementException:
        #     break
        # except StaleElementReferenceException:
        #     time.sleep(1)
    time.sleep(1)

    order_no_set = set()
    items = driver.find_elements(By.XPATH, "//*[@id='root']/div/div[2]/div/div[1]/div[3]/div[1]/ul/li")
    time.sleep(1)
    for item in items:
        retry_count = 0
        is_failure = False
        while retry_count < 5:
            try:
                item_class_name = item.get_attribute('class')
                if 'ListBanner' in item_class_name:
                    break
                item_detail = item.find_element(By.XPATH, "div/div[2]")
                order_no = item_detail.find_element(By.XPATH, "div[2]/span[1]").text
                if order_no in order_no_set:
                    break
                order_no_set.add(order_no)
                time.sleep(1)
                ActionChains(driver) \
                    .key_down(Keys.CONTROL) \
                    .click(item_detail) \
                    .key_up(Keys.CONTROL) \
                    .perform()
                time.sleep(1)
                move_to_last_window()
                time.sleep(1)
                show_detail()
                time.sleep(1)
                driver.close()
                move_to_last_window()
                time.sleep(1)
            except NoSuchElementException as e:
                print(e)
                is_failure = True
            except StaleElementReferenceException as e:
                print(e)
                is_failure = True
            finally:
                while len(driver.window_handles) != 1:
                    driver.close()
                    move_to_last_window()
                    time.sleep(1)
                if is_failure:
                    is_failure = False
                    retry_count += 1
                    print(f"retry...{retry_count}")
                else:
                    break


def hey():
    while True:
        time.sleep(10)


initialize_driver()
start_driver(url=base_url)
wait_for_login()
a()
hey()
