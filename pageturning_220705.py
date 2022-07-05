from distutils.command.sdist import sdist
from tkinter.tix import DirSelectDialog
from docutils import ApplicationError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 엔터 동작 임포트
import time
import os # 수행하고 있는 프로그램의 os 버전 체크
import psutil # 메모리 체크 
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
# # 올리브영 웹사이트 열기 
# browser.get('https://www.oliveyoung.co.kr/store/main/main.do?oy=0')
# browser.implicitly_wait(10) #웹사이트 열 동안 10초까지는 기다려줌(웹사이트 로딩이 느리면 그 다음 열라고 선택한 태그를 찾을 수 없어서 에러남)
# # 카테고리 클릭
# browser.find_element(By.ID, 'btnGnbOpen').click()

# # 스킨케어 > 스킨/로션/올인원 클릭
# browser.find_element(By.XPATH, '//*[@id="gnbAllMenu"]/ul/li[1]/div[1]/ul[1]/li[1]/a').click()
# # 카테고리 내 첫번째 상품 클릭
# browser.find_element(By.XPATH, '//*[@id="Contents"]/ul[2]/li[1]/div').click()
# time.sleep(2)
# # 리뷰 클릭
# browser.find_element(By.CSS_SELECTOR, '.goods_reputation').click()
# time.sleep(2)




browser.get('https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000149425&dispCatNo=100000100010008&trackingCd=Cat100000100010008_Small')
browser.implicitly_wait(10) 
browser.find_element(By.CSS_SELECTOR, '.goods_reputation').click()
time.sleep(2)
# 리뷰 긁어오기
reviewNum = browser.find_element(By.CSS_SELECTOR, 'p.total>em').text
time.sleep(2)
print(reviewNum)
aa = reviewNum.replace(',','')
print(aa)


def find_and_add(x):      # 리뷰 페이지에서 id, review, date 텍스트 스크래핑
    for i in x:
        yield i.text

ids_group = []
reviews_group = []
dates_group = []
exp = []

pagenum = list(range(1,(int(reviewNum)//10) + 2))
for page in pagenum:
    information_group = browser.find_element(By.CSS_SELECTOR, '.inner_list')

    collection = ['.id','.txt_inner','.date']
    for i in collection:
        ext = information_group.find_elements(By.CSS_SELECTOR, f'{i}')
        if i == '.id':
            id = find_and_add(ext)
            ids = [x for x in id]
            ids_group.extend(ids)

        elif i == '.txt_inner':
            review = find_and_add(ext)
            reviews = [x for x in review]
            reviews_group.extend(reviews)

        elif i == '.date':
            date = find_and_add(ext)
            dates = [x for x in date]
            dates_group.extend(dates)
    
    # 체험단 필터링 - 무상으로 제공받은 제품의 경우 False값 부여

    
    for i in range(1,11):

        time.sleep(2)
        filter = browser.find_elements(By.XPATH, f'//*[@id="gdasList"]/li[{i}]/div[2]/div[1]/span[3]')
        time.sleep(2)
        if len(filter) == 0:
            exp.append('True')
        elif filter[0].get_attribute("class") == 'ico_offlineStore':
            exp.append('True')
        else:
            exp.append('False')
    
    print("현재 페이지",page,"page 입니다")
    rvpage = browser.find_element(By.CSS_SELECTOR, '.pageing>a')
    time.sleep(2)
    browser.execute_script("arguments[0].setAttribute('data-page-no',arguments[1])",rvpage, page)
    time.sleep(1)
    rvpage.click()
    time.sleep(2)
    

print(ids_group)
print(reviews_group)
print(dates_group)
print(exp)

# useK = process.memory_info().rss / 1024
# print(str(useK),' KB')
# useM = useK / 1024
# print(str(useM),' MB')
