import pandas as pd

df_AVO = pd.read_excel('./AVO_testdata.xlsx')
df_AVB = pd.read_excel('./AVB_testdata.xlsx')
df_AVF = pd.read_excel('./AVF_testdata.xlsx')
df_AVK = pd.read_excel('./AVK_testdata.xlsx')
df_AVG = pd.read_excel('./AVG_testdata.xlsx')
df_AVY = pd.read_excel('./AVY_testdata.xlsx')

def cnt_acc(dataframe) :
    df = dataframe
    Org = df.loc[2,'Org Code']
    Res_all = len(df)
    Res_NaN = len(df.loc[df['AI Suggested Accuracy'] == -1])
    Res_y = len(df.loc[df['AI Suggested Accuracy'] == 'Y'])
    Res_n = len(df.loc[df['AI Suggested Accuracy'] == 'N'])
    
    print('ORG Code :', Org)
    print('전체 예측 횟수 :', Res_all)    
    print('오류(-1) 횟수 :',Res_NaN)
    print('예측 성공 횟수 :',Res_y)
    print('예측 실패 횟수 :', Res_n)
    print('----------------------------------------------')

cnt_acc(df_AVO)
cnt_acc(df_AVB)
cnt_acc(df_AVF)
cnt_acc(df_AVK)
cnt_acc(df_AVG)
cnt_acc(df_AVY)
