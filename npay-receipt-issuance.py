import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

driver: webdriver.Chrome
base_url = "https://order.pay.naver.com/home"
current_url = ""
date_start = ""
date_end = ""


def initialize_driver():
    global driver
    # Chrome 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


def start_driver(url: str):
    driver.get(url)
    global current_url
    current_url = driver.current_url


def wait_for_login():
    while True:
        if driver.current_url != current_url:
            break
        time.sleep(1)


def a():
    time.sleep(1)
    search_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.TwoStagedLayoutWrapper-module_container__-NuVi > div > div.TwoStagedLayoutWrapper-module_content-left__2eGzo.PcHome_content-left__1Sj2x > div.PaymentCategoryAndSearchButton_article__3lLC7 > div > div.PaymentCategoryAndSearchButton_area-button__3G-wX > button")
    search_btn.click()
    time.sleep(1)
    start_date = driver.find_element(By.XPATH, "//*[contains(@id, 'portal__')]/div/div[1]/div[2]/div[1]/div/div[1]/div[1]")
    end_date = driver.find_element(By.XPATH, "//*[contains(@id, 'portal__')]/div/div[1]/div[2]/div[1]/div/div[3]/div[1]")
    driver.execute_script("arguments[0].childNodes[1].nodeValue = '24. 06. 24';", start_date)
    driver.execute_script("arguments[0].childNodes[1].nodeValue = '24. 07. 01';", end_date)
    # start_date.send_keys("24. 06. 25")
    # end_date.send_keys("2024-07-01")


def hey():
    while True:
        time.sleep(10)


initialize_driver()
start_driver(url=base_url)
wait_for_login()
a()
hey()
