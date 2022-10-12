
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
from pyparsing import col
import seaborn as sns
from seaborn.distributions import distplot
import platform
from scipy import stats

from .model_survey import survey

# -------------------------------------------------------------------------------------------
# 테스트 페이지
def test(request):
    return render(request,
           'surveyapp/test.html',
           {})
# -------------------------------------------------------------------------------------------
# 메인 페이지
def main(request):
    return render(request,
           'surveyapp/main.html',
           {})
# -------------------------------------------------------------------------------------------
# Part1_01 연도별 최저임금 현황
def part1_01(request):
    return render(request,
           'surveyapp/part1_01.html',
           {})
# -------------------------------------------------------------------------------------------
# Part1_02 연도별 물가 현황    
def part1_02(request):
    return render(request,
           'surveyapp/part1_02.html',
           {})
# -------------------------------------------------------------------------------------------
# Part1_01 연도별 GDP 현황
def part1_03(request):
    return render(request,
           'surveyapp/part1_03.html',
           {})
# -------------------------------------------------------------------------------------------
# Part2_01 연도별 서비스직 근로자수 현황
def part2_01(request):
    return render(request,
           'surveyapp/part2_01.html',
           {})
# -------------------------------------------------------------------------------------------
# Part2_02 연도별 서비스직 근로시간 현황
def part2_02(request):
    return render(request,
           'surveyapp/part2_02.html',
           {})
# -------------------------------------------------------------------------------------------
# Part3_01 전년도 만족도 현황
def part3_01(request):
    return render(request,
           'surveyapp/part3_01.html',
           {})
# -------------------------------------------------------------------------------------------
# Part3_02 인력대체기술 현황현황
def part3_02(request):
    return render(request,
           'surveyapp/part3_02.html',
           {})
# -------------------------------------------------------------------------------------------
# 설문조사 폼
def survey_form(request):
    return render(request,
           'surveyapp/survey_form.html',
           {})
# -------------------------------------------------------------------------------------------
# 설문조사 고용주
def survey_employer(request):
    return render(request,
           'surveyapp/survey_employer.html',
           {})
# -------------------------------------------------------------------------------------------
# 설문조사 근로자
def survey_worker(request):
    return render(request,
           'surveyapp/survey_worker.html',
           {})
# -------------------------------------------------------------------------------------------
# 설문 DB TABLE 생성
def createTable(request):
    survey.createTableSurvey()
    
    return HttpResponse("Create OK")
# -------------------------------------------------------------------------------------------
# 입력한 고용주 설문 DB 저장
def set_Survey_Employer_Insert(request) :
    peco = request.POST.get("eco")
    page = request.POST.get("age")
    pgender = request.POST.get("gender")
    pQ1 = request.POST.get("Q1")
    pQ1_1 = request.POST.get("Q1_1")
    pQ1_2 = request.POST.get("Q1_2")
    pQ2 = request.POST.get("Q2")
    pQ3 = request.POST.get("Q3")
    pQ4 = request.POST.get("Q4")
    pQ5 = request.POST.get("Q5")
    pQ6 = request.POST.get("Q6")
    
    rs = survey.setSurveyEmployerInsert(peco, page, pgender, pQ1,pQ1_1,pQ1_2,pQ2,pQ3,pQ4,pQ5,pQ6)
    
    msg = ""
    if rs == "OK" :
        msg = """<script>
                    alert('설문에 참여해 주셔서 감사합니다')
                    location.href = '/survey/survey_end'
                    </script>"""
    else: 
        msg = """<script>
                    alert('실패')
                    history.go(-1)
                    </script>"""
    return HttpResponse(msg)
# -------------------------------------------------------------------------------------------
# 입력한 근로자 설문 DB 저장
def set_Survey_Worker_Insert(request) :
    peco = request.POST.get("eco")
    page = request.POST.get("age")
    pgender = request.POST.get("gender")
    pQ1 = request.POST.get("Q1")
    pQ1_1 = request.POST.get("Q1_1")
    pQ1_2 = request.POST.get("Q1_2")
    pQ2 = request.POST.get("Q2")
    pQ3 = request.POST.get("Q3")
    pQ4 = request.POST.get("Q4")
    pQ5 = request.POST.get("Q5")
    pQ6 = request.POST.get("Q6")
    pQ7 = request.POST.get("Q7")
    
    rs = survey.setSurveyWorkerInsert(peco, page, pgender, pQ1,pQ1_1,pQ1_2,pQ2,pQ3,pQ4,pQ5,pQ6,pQ7)
    
    msg = ""
    if rs == "OK" :
        msg = """<script>
                    alert('설문에 참여해 주셔서 감사합니다')
                    location.href = '/survey/survey_end/'
                    </script>"""
    else: 
        msg = """<script>
                    alert('실패')
                    history.go(-1)
                    </script>"""
    return HttpResponse(msg)
# -------------------------------------------------------------------------------------------
# 설문종료
def view_Survey_End(request) :
    
    df = survey.getSurveyWorkerList()
    
    # return HttpResponse(df.to_html())
    context = {"df" : df}
    
    return render(
        request,
        "surveyapp/survey_end.html",
        context
    )
# -------------------------------------------------------------------------------------------
#  고용주 만족도 조사 결과 시각화 및 저장하기
def view_Employer_Result_Visualization(result_df) :
    
    ylist = np.arange(0,(result_df[0].max() + 5),5)
    
    plt.figure(figsize=(13,10))
    plt.rc('font', family = 'Malgun Gothic', size = 20)
    
    fig = plt.gcf()
    fig.set_facecolor('#EEEEEE')
    plt.gca().set_facecolor('#EEEEEE')

    plt.title('최저임금에 대한 고용주 만족도',fontsize = 25,loc='center', pad=30, fontweight="bold")

    plt.bar(result_df['index'],result_df[0],width=0.5, color =['navy','darkred','#F2B117'])

    plt.yticks(ylist)

    for i, v in enumerate(result_df['index']):
        plt.text(v, result_df[0][i], result_df[0][i],
                fontsize = 30,
                color='black',
                horizontalalignment='center',  # horizontalalignment (left, center, right)
                verticalalignment='bottom')    # verticalalignment (top, center, bottom)
        
    # 그래프 저장하기
    fig.savefig('surveyapp/static/surveyapp/images/result/employer_result.png')
# -------------------------------------------------------------------------------------------
#  근로자 만족도 조사 결과 시각화 및 저장하기(함수로 처리)
def view_Worker_Result_Visualization(result_df) :
    ylist = np.arange(0,(result_df[0].max() + 5),5)
    
    plt.figure(figsize=(13,10))
    
    plt.rc('font', family = 'Malgun Gothic', size = 20)
    
    fig = plt.gcf()
    fig.set_facecolor('#EEEEEE')
    plt.gca().set_facecolor('#EEEEEE')

    plt.title('최저임금에 대한 근로자 만족도',fontsize = 25,loc='center', pad=30, fontweight="bold")

    plt.bar(result_df['index'],result_df[0],width=0.5, color =['navy','darkred','#F2B117'])

    plt.yticks(ylist)

    for i, v in enumerate(result_df['index']):
        plt.text(v, result_df[0][i], result_df[0][i],
                fontsize = 30,
                color='black',
                horizontalalignment='center',  # horizontalalignment (left, center, right)
                verticalalignment='bottom')    # verticalalignment (top, center, bottom)
        
    # 그래프 저장하기
    fig.savefig('surveyapp/static/surveyapp/images/result/worker_result.png')
# -------------------------------------------------------------------------------------------
# 만족도 조사결과 페이지
def view_Survey_Result(request) :
    
    ## 설문 데이터 조회하기
    employer_df = survey.getSurveyEmployerList()
    worker_df = survey.getSurveyWorkerList()
    
    # 시각화 및 저장(함수로 처리)
    view_Employer_Result_Visualization(employer_df)
    view_Worker_Result_Visualization(worker_df)
        
    return render(
        request,
        'surveyapp/survey_result.html',
        {}
    )
# ----------------------------------------------------------------------------------------------------------
