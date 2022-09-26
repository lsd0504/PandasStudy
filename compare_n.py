from ast import Or
from dataclasses import asdict
from turtle import width
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# iwms_AVO = pd.read_excel('./AVO_testdata2.xlsx')
# iwms_AVB = pd.read_excel('./AVB_testdata2.xlsx')
iwms_AVF = pd.read_excel('./AVF_testdata2.xlsx')
# iwms_AVK = pd.read_excel('./AVK_testdata2.xlsx')
iwms_AVG = pd.read_excel('./AVG_testdata2.xlsx')
# iwms_AVY = pd.read_excel('./AVY_testdata2.xlsx')
# iwms_CNZ = pd.read_excel('./CNZ_testdata.xlsx')
# iwms_NPX = pd.read_excel('./NPX_testdata2.xlsx')
# iwms_NPY = pd.read_excel('./NPY_testdata2.xlsx')

mldl_AVO = pd.read_csv('./AVO.csv')
mldl_AVO_1 = pd.read_csv('./AVO_1.csv')
mldl_AVO_2 = pd.read_csv('./AVO_2.csv')
mldl_AVB = pd.read_csv('./AVB.csv')
mldl_AVB_1 = pd.read_csv('./AVB_1.csv')
mldl_AVB_2 = pd.read_csv('./AVB_2.csv')
mldl_AVF = pd.read_csv('./AVF.csv')
mldl_AVF_1 = pd.read_csv('./AVF_1.csv')
mldl_AVF_2 = pd.read_csv('./AVF_2.csv')
mldl_AVK = pd.read_csv('./AVK.csv')
mldl_AVK_1 = pd.read_csv('./AVK_1.csv')
mldl_AVK_2 = pd.read_csv('./AVK_2.csv')
mldl_AVG = pd.read_csv('./AVG.csv')
mldl_AVG_1 = pd.read_csv('./AVG_1.csv')
mldl_AVG_2 = pd.read_csv('./AVG_2.csv')
mldl_CNZ = pd.read_csv('./CNZ.csv')
mldl_CNZ_1 = pd.read_csv('./CNZ_1.csv')
mldl_CNZ_2 = pd.read_csv('./CNZ_2.csv')
# mldl_NPX = pd.read_csv('./NPX.csv')
# mldl_NPX_1 = pd.read_csv('./NPX_1.csv')
# mldl_NPX_2 = pd.read_csv('./NPX_2.csv')
# mldl_NPY = pd.read_csv('./NPY.csv')
# mldl_NPY_1 = pd.read_csv('./NPY_1.csv')
# mldl_NPY_2 = pd.read_csv('./NPY_2.csv')
# mldl_AVY = pd.read_csv('./AVY.csv')

def comp_n(iwms, mldl, mldl_1, mldl_2):
    date_change(mldl)
    
    Org = iwms.loc[2,'Org Code']
    Date = iwms.loc[2,'Suggesstion Date']
        
    cond_sugN = (iwms['AI Suggested Accuracy'] == 'N') & (iwms['Data Type'] != 'Transfer')
    iwms_sugN = iwms[cond_sugN].reset_index()
    iwms_comp = iwms_sugN[['Part No', 'AI Suggested Locator']]
    mldl_comp = mldl[['PART_NO', 'LOCATOR']]
    
    print('선택한 ORG : ' + Org)
    
    # find_new_loc(iwms_comp, mldl_comp)
    # get_rank(iwms_sugN, mldl_comp)
    new_loc(iwms_sugN, mldl_1,mldl_2)


def new_loc(iwms, mldl_1, mldl_2):
    cnt_a = 0
    cnt_b = 0
    cnt_c = 0
    cnt_d = 0
    cnt_e = 0
    for index, row in iwms.iterrows():
        mldl_vc_1 = pd.DataFrame(mldl_1[mldl_1['PART_NO'] == row['Part No']].value_counts()).reset_index()
        mldl_vc_2 = pd.DataFrame(mldl_2[mldl_2['PART_NO'] == row['Part No']].value_counts()).reset_index()
        len_old = len(mldl_vc_1[mldl_vc_1['LOCATOR'] == row['AI Suggested Locator']])
        len_b = len(mldl_vc_1[mldl_vc_1['LOCATOR'] == row['Actual Putaway Locator']])

        if (len_old > 0) and (len_b == 0) :
            cnt_a += 1
        elif (len_old > 0) and (len_b > 0) :
            cnt_b += 1
        elif (len_old == 0) and (len_b == 0) :
            cnt_c += 1
        else :
            cnt_e += 1
          
               
    print('AI Sug Loc가 데이터에 존재하고 Actual이 학습 시점 이후에 존재 : ' , cnt_a)    
    print('AI Sug Loc가 데이터에 존재, Actual도 학습 전에 존재, 우선순위 오류 : ' , cnt_b)
    print('AI Sug Loc가 데이터상 존재 X, 클래스코드 통해 추천해준 경우 : ', cnt_c)
                              
            
def date_change(mldl):
    for i in range(len(mldl)):
        mldl.loc[i,'DATE'] = mldl.loc[i,'DATE'][:10]
        
 
def drop_same(df):
    for i, row in df.iterrows():
        try:
            ai_su = row['AI Suggested Locator']
            actual = row['Actual Putaway Locator']
            
            if ai_su[3:5] == actual[3:5]:
                df.drop(i, inplace = True)
        except:
            pass
    return df.reset_index(drop=True)

# comp_n(iwms_AVK,mldl_AVK)
# comp_n(drop_same(iwms_AVF),mldl_AVF, mldl_AVB_1, mldl_AVF_2)
comp_n(drop_same(iwms_AVG), mldl_AVG, mldl_AVG_1, mldl_AVG_2)
# comp_n(iwms_CNZ,mldl_CNZ)

