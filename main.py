from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from userdata import data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
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

ticket_name = data.ticket_name
day = data.day

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
    
    # 이 방법으로는 새로운 브라우저에서 로그인 시도가 안뜸. 단 매 번 QR코드를 인식하는 번거로움이 있음
def QR_login():
    driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/header/div[1]/div/div[2]/ul/li[1]/a').click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.ID,'appLoginBtn').click()
    time.sleep(10)
    
def search(ticket_name):
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.title)
    search = driver.find_element(By.ID,"search")
    search.send_keys(ticket_name)
    search.send_keys(Keys.ENTER)
    driver.find_element(By.CLASS_NAME,'img_box').click()
    
def select_date(day):
    # role="option"을 배열로 받음
    month_elements = driver.find_elements(By.CSS_SELECTOR, '[role="option"]')
    # 하위 요소 중 원하는 값을 입력받아 클릭
    for element in month_elements:
        # element에서 텍스트를 추출하여 day_number와 일치하는지 확인
        if element.text == str(day):
            element.click()
            print(f"{day}을(를) 선택했습니다.")

def reserve_button(): 
    try:
        button = driver.find_element(By.CSS_SELECTOR, '.common_btn')
        while button.get_attribute('aria-disabled') == 'true':
            print("아직 판매 예정입니다.")
            time.sleep(0.8)
            driver.refresh()
            button = driver.find_element(By.CSS_SELECTOR, '.common_btn')
    
        print("판매중 입니다. 날짜 고르기")
        select_date(day)
        # WebDriverWait(driver,1).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR,'.produect_time_btn'))
        # 여기를 좀 다듬고 싶은데 좋은 아이디어가 없나...
        time.sleep(0.6)
        button.click()
    
    except Exception as e :
        if e == NoSuchWindowException:
            print("윈도우 창이 꺼졌습니다.")
        if e == KeyboardInterrupt:
            print("키보드 인터럽이 들어왔습니다.")

def selected_seat():
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn_full.ng-scope"))
    )
        print("초기화 버튼이 나타남!")
        next_button = driver.find_element(By.CSS_SELECTOR,'a.btn.ng-binding.btn_full')
        next_button.click()
    except :
        pass
        
def captcha():
    driver.switch_to.window(driver.window_handles[-1])
    # 부정예매방지문자 OCR 생성
    reader = easyocr.Reader(["en"])

    # 부정예매방지 문자 이미지 요소 선택
    try:
        captchaPng = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.ID, "captcha_img"))
        )

        # 부정예매방지문자 입력
        while captchaPng:
            result = reader.readtext(captchaPng.screenshot_as_png, detail=0)
            capchaValue = (
                result[0]
                .replace(" ", "")
                .replace("5", "S")
                .replace("0", "O")
                .replace("$", "S")
                .replace(",", "")
                .replace(":", "")
                .replace(".", "")
                .replace("+", "T")
                .replace("'", "")
                .replace("`", "")
                .replace("1", "L")
                .replace("e", "Q")
                .replace("3", "S")
                .replace("€", "C")
                .replace("{", "")
                .replace("-", "")
            )

            # 입력
            chapchaText = driver.find_element (By.XPATH,'//*[@id="ipt_captcha"]')
            chapchaText.send_keys(capchaValue)

            # 입력완료 버튼 클릭
            driver.find_element(
                By.XPATH, '//*[@id="wrap_reserve"]/div[4]/div[2]/div/form/fieldset/div/button'
            ).click()

            # 입력이 잘 됐는지 확인하기
            display = driver.find_element(
                By.XPATH, '//*[@id="wrap_reserve"]/div[4]/div[2]/div/form/fieldset/span[2]/span'
            ).is_displayed()
            # 입력 문자가 틀렸을 때 새로고침하여 다시입력
            if display:
                driver.find_element(
                    By.XPATH, '//*[@id="wrap_reserve"]/div[4]/div[2]/div/form/fieldset/button'
                ).click()
            # 입력 문자가 맞으면 select 함수 실행
            else:
                # 좌석 디테일 프레임으로 넘어가기
                selected_seat()
                break
    except:
        selected_seat()
    pass

start()
QR_login()
search(ticket_name)
reserve_button()
captcha()
selected_seat()
time.sleep(100)