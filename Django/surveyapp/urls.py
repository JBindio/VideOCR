from django.urls import path
from . import views as sur

urlpatterns = [
    path('test/', sur.test),
    path('main/', sur.main),
    path('part1_01/', sur.part1_01),
    path('part1_02/', sur.part1_02),
    path('part1_03/', sur.part1_03),
    path('part2_01/', sur.part2_01),
    path('part2_02/', sur.part2_02),
    path('part3_01/', sur.part3_01),
    path('part3_02/', sur.part3_02),
    path('survey_form/', sur.survey_form),
    path('survey_create/', sur.createTable),
    path('survey_employer_insert/', sur.set_Survey_Employer_Insert),
    path('survey_worker_insert/', sur.set_Survey_Worker_Insert),
    path('survey_end/', sur.view_Survey_End),
    path('survey_employer/', sur.survey_employer),
    path('survey_worker/', sur.survey_worker),
    path('survey_result/', sur.view_Survey_Result),
    
]
