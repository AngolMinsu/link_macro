from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from userdata import data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import easyocr

# 드라이버 설정 및 생성
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)

# 브라우저 사이즈
driver.set_window_size(1900, 1000)

# 웹페이지가 로드될 때까지 2초를 대기
driver.implicitly_wait(time_to_wait=2)

# 웹 페이지로 연결 및 로그인
def start():
    # 웹 페이지 연결
    driver.get(url="https://www.ticketlink.co.kr/home")
    time.sleep(2)

# 로그인
def login():
    driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/header/div[1]/div/div[2]/ul/li[1]/a').click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)
    driver.find_element(By.ID,'id').send_keys(data.id)
    driver.find_element(By.ID,'pw').send_keys(data.pw)
    driver.find_element(By.ID,'loginBtn').click()
    
def search():
    ticket_name = data.ticket_name
    search = driver.find_element(By.ID,"search")
    search.send_keys(ticket_name)
    search.send_keys(Keys.ENTER)

start()
login()
time.sleep(100)
search()