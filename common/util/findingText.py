# 리뷰 페이지에서 원하는 내용 텍스트로 스크래핑하는 함수
def find_and_add(x):  
    for i in x:
        yield i.text