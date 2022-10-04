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
    cnt_near = 0
    cnt_far = 0
    for i in range(len(iwms_sugN)):
        sug_Loc = iwms_sugN.loc[i, 'AI Suggested Locator']
        act_Loc = iwms_sugN.loc[i, 'Actual Putaway Locator']
        sug_Loc_slice = sug_Loc[3:5]
        act_Loc_slice = act_Loc[3:5]
    
        if sug_Loc_slice == act_Loc_slice :
            cnt_near += 1
        else :
            cnt_far += 1
    
    # find_new_loc(iwms_comp, mldl_comp)
    # get_rank(iwms_sugN, mldl_comp)
    case_a, case_b, case_c = new_loc(drop_same(iwms_sugN), mldl_1, mldl_2)
    
    print('AI Sug Loc가 데이터에 존재하고 Actual이 학습 시점 이후에 존재 : ' , case_a)    
    print('AI Sug Loc가 데이터에 존재, Actual도 학습 전에 존재, 우선순위 오류 : ' , case_b)
    print('AI Sug Loc가 데이터상 존재 X, 클래스코드 통해 추천해준 경우 : ', case_c)
    
    cnt_acc(iwms, cnt_far, cnt_near, case_a, case_b, case_c)


def new_loc(iwms, mldl_1, mldl_2):
    cnt_a = 0       #ai loc 과거에 존재, actual이 학습 후에 존재
    cnt_b = 0       #우선순위 오류(ai loc, actual 모두 학습 전에 존재)
    cnt_c = 0       #ai loc가 과거에 존재하지 않는 경우(클래스코드 통해 추천)
    
    cnt_e = 0       #에러(0 나오는게 정상)
    for index, row in iwms.iterrows():
        mldl_vc_1 = pd.DataFrame(mldl_1[mldl_1['PART_NO'] == row['Part No']].value_counts()).reset_index()      #iwms 파트넘버로 mldl 벨류카운트
        # mldl_vc_2 = pd.DataFrame(mldl_2[mldl_2['PART_NO'] == row['Part No']].value_counts()).reset_index()
        len_old = len(mldl_vc_1[mldl_vc_1['LOCATOR'] == row['AI Suggested Locator']])       #ai loc와 실제 loc가 동일
        len_b = len(mldl_vc_1[mldl_vc_1['LOCATOR'] == row['Actual Putaway Locator']])       #actual loc와 실제 loc가 동일

        if (len_old > 0) and (len_b == 0) :
            cnt_a += 1
        elif (len_old > 0) and (len_b > 0) :
            cnt_b += 1
        elif (len_old == 0) and (len_b == 0) :
            cnt_c += 1
        else :
            cnt_e += 1
          
    return(cnt_a, cnt_b, cnt_c)           
                              
            
def date_change(mldl):      #mldl, iwms 날짜 포멧 맞추기
    for i in range(len(mldl)):
        mldl.loc[i,'DATE'] = mldl.loc[i,'DATE'][:10]
        
 
def drop_same(df):          #Y값 제거
    for i, row in df.iterrows():
        try:
            ai_su = row['AI Suggested Locator']
            actual = row['Actual Putaway Locator']
            
            if ai_su[3:5] == actual[3:5]:
                df.drop(i, inplace = True)
        except:
            pass
    return df.reset_index(drop=True)

def cnt_acc(df,far, near, a, b, c) :            #실제 변수 넣고 파이차트 함수 돌리는 부분
    Org = df.loc[2,'Org Code']
    
    
    Res_NaN = len(df.loc[(df['AI Suggested Accuracy'] == -1)&(df['AI Suggested Locator']==None)&(df['Data Type'] != 'Transfer')])
    Res_y = len(df.loc[(df['AI Suggested Accuracy'] == 'Y')&(df['Data Type'] != 'Transfer')])
    Res_n = len(df.loc[(df['AI Suggested Accuracy'] == 'N')&(df['Data Type'] != 'Transfer')])
    # Res_case_same = Res_y + near
    # Res_case_far = far    
    # Res_case_a = Res_y + a
    # Res_a_n = Res_n - a
    # Res_plus = Res_case_same + a
    # Res_plus_n = far - a
    
    # make_pie(Org + ' Same Org', Res_NaN, Res_case_same, Res_case_far)       #same ORG 제외
    # make_pie(Org + ' case A', Res_NaN, Res_case_a, Res_a_n)                 #case A(ai loc 과거에 존재, actual이 학습 후에 존재)제외
    # make_pie(Org + ' Same + case A', Res_NaN, Res_plus, Res_plus_n)         #둘 다 제외
    make_pie(Org, near, a, b, c)                        #N값 전체 뽑는 그래프
    

def make_pie(title, near, a, b, c):         #파이차트 그려서 저장하는 함수
    result = ['Same Zone', 'A', 'B', 'C']
    values = [near, a, b, c]
    explode = [0.05, 0.05, 0.05, 0.05]
    
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}% ({v:d})'.format(p=pct, v=val)
        return my_autopct
    
    plt.pie(values, labels = result, explode = explode, autopct= make_autopct(values))
    plt.title(title)
    #plt.show()
    
    plt.savefig("D:/Images/" + title + '.png')
    plt.cla()



# comp_n(iwms_AVK,mldl_AVK)
# comp_n(drop_same(iwms_AVF),mldl_AVF, mldl_AVB_1, mldl_AVF_2)
comp_n(iwms_AVG, mldl_AVG, mldl_AVG_1, mldl_AVG_2)
# comp_n(iwms_CNZ,mldl_CNZ)

