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
    Org = iwms.loc[2,'Org Code']
    cond_sugN = (iwms['AI Suggested Accuracy'] == 'N')&(iwms['Data Type'] != 'Transfer')
    iwms_sugN = iwms[cond_sugN].reset_index()
    iwms_comp = iwms_sugN[['Part No', 'AI Suggested Locator', 'Actual Putaway Locator']]
    df_mldl = mldl['PART_NO'].value_counts()
    
    # print(iwms_comp)
    for i in range(len(iwms_comp)):
        pNo_iwms = iwms_comp.loc[i,'Part No']
        ailoc_iwms = iwms_comp.loc[i,'AI Suggested Locator']
        actloc_iwms = iwms_comp.loc[i,'Actual Putaway Locator']
        # print(pNo_iwms , df_mldl[pNo_iwms])
        # print(df_mldl)
        
        if df_mldl[pNo_iwms] < 3:
            print('AI 추천 locator가 데이터 상에서는 보이지만, 처음으로 들어간 경우')
            print('Part No : ' + pNo_iwms + ', AI Sug Loc : ' + ailoc_iwms + ', Actual Loc : ' + actloc_iwms)
        
    
    
# comp_n(iwms_AVB,mldl_AVB)
comp_n(iwms_AVF,mldl_AVF)