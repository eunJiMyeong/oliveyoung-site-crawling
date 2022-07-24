# 파싱한 데이터를 엑셀로 저장
import pandas as pd

def saving_excel(pageInfo):
    for i in range(0,3):
        new = pd.DataFrame({'mother_category':pageInfo['product_info'][i]['m_category_name'],
                            'child_category': pageInfo['product_info'][i]['c_category_name'],
                            'productName':pageInfo['product_info'][i]['name'],
                            'productSeq':pageInfo['product_info'][i]['seq'],
                            'id' : pageInfo['product_info'][i]['reviewData'][0],
                            'con' : pageInfo['product_info'][i]['reviewData'][1],
                            'data': pageInfo['product_info'][i]['reviewData'][2],
                            'expYN': pageInfo['product_info'][i]['reviewData'][3]})
        if i == 0:
            RV_Datas = new
        else:
            RV_Datas = RV_Datas.append(new)
            
    RV_Datas.to_excel('RV_Datas.xlsx')
