from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium
import time
import common.util.collectRV as COL

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chomeDriverPath = 'C:\Python\chromedriver\chromedriver.exe'
browser = webdriver.Chrome(chomeDriverPath, options=options)
browser.get('https://www.oliveyoung.co.kr/store/main/main.do?oy=0')

pageInfo = {
    # catCount: 0,  # 현재 카테고리
    # totalCatCount: 0,  # 전체 카테고리 카운트

    'categoryIndex': 0,  # 현재 소 카테고리
    'totalCategoryCount': 0,  # 전체 소 카테고리 카운트

    'productIndex': 0,  # 현재 상품 번호
    'totalProductCount': 0,  # 전체 상품 카운트 (선택한 카테고리 하위에 상품수)

    'product_pages_num': 0,  # 상품
}

for testX in range(0, 2):  # 테스트용 두개 상품
    # 카테고리 클릭
    browser.find_element(By.ID, 'btnGnbOpen').click()
    time.sleep(2)

    # 전체 소 카테고리 수
    category_lists = browser.find_elements(
        By.CSS_SELECTOR, 'ul.all_menu_wrap>li div li a')
    pageInfo['totalCategoryCount'] = len(category_lists)   # 전체 카테고리 수 설정

    browser.execute_script("arguments[0].click();",
                           category_lists[pageInfo['categoryIndex']])
    time.sleep(2)

    # 상품 페이지 수 계산
    product_pages = browser.find_element(
        By.CSS_SELECTOR, '.cate_info_tx>span').text
    product_pages = product_pages.replace(',', '')
    product_pages_num = (int(product_pages)//24)+1

    pageInfo['totalProductCount'] = product_pages  # 현 카테고리의 상품 카운트 수

    # 상품이 현재 페이지가 아니면 다음 상품페이지로 이동 하는 함수 추가

    pointX = (pageInfo['productIndex'] % 4) + 1
    pointY = (pageInfo['productIndex'] // 4) + 2

    # 기능 추가
    # 상품의 개수가 24개를 넘어가면 다음페이지의 상품을 클릭할 수 있도록 기능 추가
    # 다음페이지의 상품을 클릭하려면 pointY 의 숫자를 조절해주어야한다

    # products_pg_bttn = browser.find_element(By.CSS_SELECTOR, '.pageing>a')
    # time.sleep(2)
    # browser.execute_script(
    #     "arguments[0].setAttribute('data-page-no',arguments[1])", products_pg_bttn, 0) # TODO 상품 페이지 넘어가는거 추가해야함
    # time.sleep(1)
    # products_pg_bttn.click()
    # time.sleep(2)

    productData = {'name': '',
                   'seq': pageInfo['productIndex'],
                   'reviewData': [[], [], [], []]
                   }

    # 상품을 클릭
    browser.find_element(
        By.XPATH, f'//*[@id="Contents"]/ul[{pointY}]/li[{pointX}]/div').click()
    time.sleep(2)

    # 리뷰 창 클릭
    browser.find_element(
        By.CSS_SELECTOR, '.goods_reputation').click()
    time.sleep(2)

    # 리뷰 수 계산
    review_pages = browser.find_element(
        By.CSS_SELECTOR, 'p.total>em').text
    time.sleep(2)
    review_pages = review_pages.replace(',', '')
    review_pages_num = (int(review_pages)//10) + 1

    # 리뷰수가 아무리 많아도 리뷰 페이지는 100페이지까지만 노출됨
    if review_pages_num <= 100:
        review_pages_num = review_pages_num
    else:
        review_pages_num = 100

    # 리뷰페이지 수만큼 클릭
    # 원래 range(1,int(review_pages_num)+1)
    for review_page in range(1, 3):
        review_pg_bttn = browser.find_element(
            By.CSS_SELECTOR, '.pageing>a')
        time.sleep(2)
        browser.execute_script(
            "arguments[0].setAttribute('data-page-no',arguments[1])", review_pg_bttn, review_page)
        time.sleep(1)
        review_pg_bttn.click()
        time.sleep(2)

        # 리뷰 페이지에서 아이디, 리뷰내용, 날짜, 체험단YN 수집
        information_group = browser.find_element(
            By.CSS_SELECTOR, '.inner_list')
        time.sleep(2)
        rD = COL.reviewDatacollect(information_group)
        productData['reviewData'][0].extend(rD[0])
        productData['reviewData'][1].extend(rD[1])
        productData['reviewData'][2].extend(rD[2])
        productData['reviewData'][3].extend(rD[3])

    # 리뷰를 전부 크롤링했다면
    # 마지막 상품이 아니라면 다음 상품
    if (pageInfo['productIndex'] != pageInfo['totalProductCount']):
        pageInfo['productIndex'] = pageInfo['productIndex'] + \
            1         # 상품번호 + 1
    else:  # 상품이 마지막 상품이면
        pageInfo['categoryIndex'] = pageInfo['categoryIndex'] + \
            1       # 카테고리 + 1
        # 상품번호 = 0 (초기화)
        pageInfo['productIndex'] = 0
