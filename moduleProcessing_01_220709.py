from distutils.command.sdist import sdist
from tkinter.tix import DirSelectDialog
from docutils import ApplicationError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 엔터 동작 임포트
import time
import os # 수행하고 있는 프로그램의 os 버전 체크
import psutil # 메모리 체크 
import common.util.collectRV as COL

# 메모리 측정
# process = psutil.Process(os.getpid())
# useK = process.memory_info().rss / 1024
# print(str(useK),' KB')
# useM = useK / 1024
# print(str(useM),' MB')

# 에러메시지 출력 삭제
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우저 생성
browser = webdriver.Chrome(r'C:/chromedriver.exe',options=options)  # 크롬 브라우저 생성, 크롬드라이브 저장된 경로 입력

# 올리브영 웹사이트 열기 
browser.get('https://www.oliveyoung.co.kr/store/main/main.do?oy=0')
browser.implicitly_wait(10) #웹사이트 열 동안 10초까지는 기다려줌(웹사이트 로딩이 느리면 그 다음 열라고 선택한 태그를 찾을 수 없어서 에러남)
# 카테고리 클릭
browser.find_element(By.ID, 'btnGnbOpen').click()
time.sleep(2)

category_lists = browser.find_elements(By.CSS_SELECTOR, 'ul.all_menu_wrap>li div li a')
product_index = 0

#카테고리 내 소카테고리 클릭
for category in range(10, 11): #원래 (1,103)
    category_lists = browser.find_elements(By.CSS_SELECTOR, 'ul.all_menu_wrap>li div li a')
    time.sleep(2)
    browser.execute_script("arguments[0].click();", category_lists[category]) 
    time.sleep(2)
    # 상품 페이지 수 계산
    product_pages = browser.find_element(By.CSS_SELECTOR, '.cate_info_tx>span').text
    product_pages = product_pages.replace(',','')
    product_pages_num = (int(product_pages)//24)+1

    # 상품 페이지만큼 클릭
    for product_page in range(1,2): # 원래 range(1,int(product_pages_num)+1)
        products_pg_bttn = browser.find_element(By.CSS_SELECTOR, '.pageing>a') 
        time.sleep(2)
        browser.execute_script("arguments[0].setAttribute('data-page-no',arguments[1])",products_pg_bttn, product_page)
        time.sleep(1)
        products_pg_bttn.click()
        time.sleep(2)
        
        # 상품 페이지 내에 있는 상품들 순서대로 클릭
        for x in range(2,3): # 원래 (2,8)
            for y in range(1,3): #원래 (1,5)
                if browser.find_element(By.XPATH, f'//*[@id="Contents"]/ul[{x}]/li[{y}]/div'):
                    time.sleep(2)
                    browser.find_element(By.XPATH, f'//*[@id="Contents"]/ul[{x}]/li[{y}]/div').click()
                    time.sleep(2)

                    product_index = product_index + 1
                    productData = {'name':'',
                                    'seq': product_index,
                                    'reviewData':[[],[],[],[]]
                                    }
                    productData['name'] = browser.find_element(By.CSS_SELECTOR, '.prd_name').text


                    # 리뷰 창 클릭
                    browser.find_element(By.CSS_SELECTOR, '.goods_reputation').click()
                    time.sleep(2)


                    # 리뷰 수 계산
                    review_pages = browser.find_element(By.CSS_SELECTOR, 'p.total>em').text
                    time.sleep(2)
                    review_pages = review_pages.replace(',','')
                    review_pages_num = (int(review_pages)//10) + 1
                    
                    # 리뷰수가 아무리 많아도 리뷰 페이지는 100페이지까지만 노출됨
                    if review_pages_num <= 100:
                        review_pages_num = review_pages_num
                    else:
                        review_pages_num = 100

                    # 리뷰페이지 수만큼 클릭
                    for review_page in range(1,3): # 원래 range(1,int(review_pages_num)+1)
                        review_pg_bttn = browser.find_element(By.CSS_SELECTOR, '.pageing>a') 
                        time.sleep(2)
                        browser.execute_script("arguments[0].setAttribute('data-page-no',arguments[1])",review_pg_bttn, review_page)
                        time.sleep(1)
                        review_pg_bttn.click()
                        time.sleep(2)

                        # 리뷰 페이지에서 아이디, 리뷰내용, 날짜, 체험단YN 수집
                        information_group = browser.find_element(By.CSS_SELECTOR, '.inner_list')
                        time.sleep(2)
                        rD = COL.reviewDatacollect(information_group)
                        productData['reviewData'][0].extend(rD[0])
                        productData['reviewData'][1].extend(rD[1])
                        productData['reviewData'][2].extend(rD[2])
                        productData['reviewData'][3].extend(rD[3])


print(productData)


# useK = process.memory_info().rss / 1024
# print(str(useK),' KB')
# useM = useK / 1024
# print(str(useM),' MB')
