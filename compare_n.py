from ast import Or
from turtle import width
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

iwms_AVO = pd.read_excel('./AVO_testdata2.xlsx')
iwms_AVB = pd.read_excel('./AVB_testdata2.xlsx')
iwms_AVF = pd.read_excel('./AVF_testdata2.xlsx')
iwms_AVK = pd.read_excel('./AVK_testdata2.xlsx')
iwms_AVG = pd.read_excel('./AVG_testdata2.xlsx')
# iwms_AVY = pd.read_excel('./AVY_testdata2.xlsx')

mldl_AVO = pd.read_csv('./AVO.csv')
mldl_AVB = pd.read_csv('./AVB.csv')
mldl_AVF = pd.read_csv('./AVF.csv')
mldl_AVK = pd.read_csv('./AVK.csv')
mldl_AVG = pd.read_csv('./AVG.csv')
# mldl_AVY = pd.read_csv('./AVY.csv')

def comp_n(iwms,mldl):
    date_change(mldl)
    Org = iwms.loc[2,'Org Code']
    Date = iwms.loc[2,'Suggesstion Date']    
    cond_sugN = (iwms['AI Suggested Accuracy'] == 'N')&(iwms['Data Type'] != 'Transfer')
    iwms_sugN = iwms[cond_sugN].reset_index()
    iwms_comp = iwms_sugN[['Part No', 'AI Suggested Locator']]
    mldl_comp = mldl[['PART_NO', 'LOCATOR']]
    
    print('선택한 ORG : ' + Org)
    drop_dup(mldl, Date)
    
    find_new_loc(iwms_comp, mldl_comp)
    
            
def find_new_loc(iwms, mldl):
    iwms_unique = iwms['AI Suggested Locator'].unique()
    mldl_unique = mldl['LOCATOR'].unique()
    
    new_loc = list(set(iwms_unique).difference(mldl_unique))
    print('AI 추천 locator가 데이터 상에서는 보이지만, 처음으로 들어간 경우 : ')
    
    if len(new_loc) < 1:
        print('해당 없음')
    else:
        for i in new_loc:
            same_loc = mldl['LOCATOR'] == i
            print(same_loc)
             
    
def drop_dup(mldl, Date):
    iwms_month = Date[5:7]
    iwms_day = Date[8:]
          
    for i in range(len(mldl)):
        if iwms_month < mldl.loc[i,'DATE'][5:7]:
            mldl = mldl.drop(i)
        elif iwms_month == mldl.loc[i,'DATE'][5:7]:
            if iwms_day <= mldl.loc[i,'DATE'][8:]:
                mldl = mldl.drop(i)
                    
            
def date_change(mldl):
    for i in range(len(mldl)):
        mldl.loc[i,'DATE'] = mldl.loc[i,'DATE'][:10]
        
              
# comp_n(iwms_AVB,mldl_AVB)
# comp_n(iwms_AVF,mldl_AVF)
comp_n(iwms_AVG, mldl_AVG)
