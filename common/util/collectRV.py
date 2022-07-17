from selenium.webdriver.common.by import By
from common.util.findingText import find_and_add

# 리뷰 페이지에서 아이디, 리뷰내용, 날짜 수집
def reviewDatacollect(information_group):
    ids_group = []
    reviews_group = []
    dates_group = []
    exps_group = []
    collection = ['.id','.txt_inner','.date','.score_area']
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

        elif i == '.score_area':
            for x in ext:
                if x.find_elements(By.CSS_SELECTOR, '.ico_oyGroup'):
                    exps_group.append('False')
                elif x.find_elements(By.CSS_SELECTOR, '.ico_offlineStore'):
                    exps_group.append('True')
                else:
                    exps_group.append('True')
    

    returnData = [ids_group, reviews_group, dates_group, exps_group]
    return returnData