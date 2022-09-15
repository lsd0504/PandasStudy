from cmath import nan
from turtle import width
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df_AVO = pd.read_excel('./AVO_testdata2.xlsx')
df_AVB = pd.read_excel('./AVB_testdata2.xlsx')
df_AVF = pd.read_excel('./AVF_testdata2.xlsx')
df_AVK = pd.read_excel('./AVK_testdata2.xlsx')
df_AVG = pd.read_excel('./AVG_testdata2.xlsx')
# df_AVY = pd.read_excel('./AVY_testdata2.xlsx')

def cnt_acc(dataframe) :
    df = dataframe
    Org = df.loc[2,'Org Code']
    date = '_[0912-0915]'
    title = Org + date
    Res_all = len(df)
    
    Res_NaN = len(df.loc[(df['AI Suggested Accuracy'] == -1)&(df['AI Suggested Locator']==None)&(df['Data Type'] != 'Transfer')])
    Res_y = len(df.loc[(df['AI Suggested Accuracy'] == 'Y')&(df['Data Type'] != 'Transfer')])
    Res_n = len(df.loc[(df['AI Suggested Accuracy'] == 'N')&(df['Data Type'] != 'Transfer')])
    
    print('ORG Code :', Org)
    print('전체 예측 횟수 :', Res_all)    
    print('오류(-1) 횟수 :',Res_NaN)
    print('예측 성공 횟수 :',Res_y)
    print('예측 실패 횟수 :', Res_n)
    print('----------------------------------------------')
    
    result = ['-1', 'Y', 'N']
    values = [Res_NaN, Res_y, Res_n]
    explode = [0.05, 0.05, 0.05]
    
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}% ({v:d})'.format(p=pct, v=val)
        return my_autopct
    
    plt.pie(values, labels = result, explode = explode, autopct= make_autopct(values))
    plt.title(title)
    #plt.show()
    
    plt.savefig("D:/Images/" + Org + '.png')
    plt.cla()
       
   

cnt_acc(df_AVO)
cnt_acc(df_AVB)
cnt_acc(df_AVF)
cnt_acc(df_AVK)
cnt_acc(df_AVG)

# cnt_acc(df_AVY)