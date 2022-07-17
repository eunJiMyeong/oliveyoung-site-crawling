from selenium import webdriver

def chromeOpen(browser):
    # 에러메시지 출력 삭제
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 브라우저 생성
    browser = webdriver.Chrome(r'C:/chromedriver.exe',options=options) 