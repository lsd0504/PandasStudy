from turtle import width
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df_AVO = pd.read_excel('./AVO_testdata1.xlsx')
# df_AVB = pd.read_excel('./AVB_testdata1.xlsx')
# df_AVF = pd.read_excel('./AVF_testdata1.xlsx')
# df_AVK = pd.read_excel('./AVK_testdata1.xlsx')
df_AVG = pd.read_excel('./AVG_testdata1.xlsx')
# df_AVY = pd.read_excel('./AVY_testdata1.xlsx')

df = df_AVG
cond_sugN = (df['AI Suggested Accuracy'] == 'N')&(df['Data Type'] != 'Transfer')
df_sugN = df[cond_sugN]
#.reset_index()
cnt_near = 0
cnt_far = 0
# print(df_sugN)
for i in range(len(df_sugN)):
    sug_Loc = df_sugN.loc[i, 'AI Suggested Locator']
    act_Loc = df_sugN.loc[i, 'Actual Putaway Locator']
    # print(sug_Loc[3:5])
    if sug_Loc[3:5] == act_Loc[3:5] :
        cnt_near += 1
    else :
        cnt_far += 1

print('같은 창고 내 적치 :' , cnt_near)
print('다른 창고 내 적치 :' , cnt_far)

result = ['Same Loc', 'Wrong Loc']
values = [cnt_near, cnt_far]
explode = [0.05, 0.05]

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}% ({v:d})'.format(p=pct, v=val)
    return my_autopct
    
plt.pie(values, labels = result, explode = explode, autopct= make_autopct(values))

plt.show()