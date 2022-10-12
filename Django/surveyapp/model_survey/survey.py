# django 가상환경에서 cx_Oracle 설치해야합니다.
# 설치 : 가상환경 프롬프트 > pip install cx_oracle
from unittest import result
import cx_Oracle
import pandas as pd

# -------------------------------------------------------------------------------------------
# 오라클 연결 및 접속하기
def getConnection() :
    #오라클 연결하기
    dsn = cx_Oracle.makedsn('localhost', 1521, service_name = 'orcl')
    # 오라클 접속하기
    conn = cx_Oracle.connect(user = "busan_06", password = "dbdb", dsn = dsn)
    return conn

# 커서받기
def getCursor(conn) :
    cursor = conn.cursor()
    return cursor

# 접속 정보 및 커서반납
def dbClose(cursor, conn) :
    # 커서반납 먼저
    cursor.close()
    # 마지막에 접속정보 반납
    conn.close()
    
# -------------------------------------------------------------------------------------------
# 설문조사 테이블 생성하기
def createTableSurvey() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    survey_employer="""create Table survey_employer
                        (EMPLOYER_ID number(15) not null,
                        ECO varchar2 (20) not null,
                        AGE varchar2 (20) not null,
                        GENDER varchar2 (20) not null,
                        Q1 varchar2 (20) not null,
                        Q1_1 varchar2 (20),
                        Q1_2 varchar2 (20),
                        Q2 varchar2 (20) not null,
                        Q3 varchar2 (20) not null,
                        Q4 varchar2 (20) not null,
                        Q5 varchar2 (20) not null,
                        Q6 varchar2 (100),
                            
                        Constraint pk_EMPLOYER_ID Primary key(EMPLOYER_ID))"""
                        
    survey_worker="""create Table survey_worker
                        (WORKER_ID number(15) not null,
                        ECO varchar2 (20) not null,
                        AGE varchar2 (20) not null,
                        GENDER varchar2 (20) not null,
                        Q1 varchar2 (20) not null,
                        Q1_1 varchar2 (20),
                        Q1_2 varchar2 (20),
                        Q2 varchar2 (20) not null,
                        Q3 varchar2 (20) not null,
                        Q4 varchar2 (20) not null,
                        Q5 varchar2 (20) not null,
                        Q6 varchar2 (20) not null,
                        Q7 varchar2 (100),
                            
                        Constraint pk_WORKER_ID Primary key(WORKER_ID))"""

    cursor.execute(survey_employer)
    cursor.execute(survey_worker)
    dbClose(cursor,conn)
# -------------------------------------------------------------------------------------------  
# 고용주 설문 입력하기
def setSurveyEmployerInsert(peco,page,pgender,pQ1,pQ1_1,pQ1_2,pQ2,pQ3,pQ4,pQ5,pQ6) : 
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """SELECT nvl(max(EMPLOYER_ID)+1, 1) as max_no
               FROM survey_employer"""
    cursor.execute(sql)
    rs_max_no = cursor.fetchone()
    no = rs_max_no[0]
    
    # 저장하기
    sql = """INSERT INTO survey_employer(
                EMPLOYER_ID, ECO, AGE, GENDER, Q1,Q1_1,Q1_2,Q2,Q3,Q4,Q5,Q6
            ) VALUES (
                :EMPLOYER_ID, :ECO, :AGE, :GENDER, :Q1,:Q1_1,:Q1_2,:Q2,:Q3,:Q4,:Q5,:Q6
            )"""
    cursor.execute(sql,
                   EMPLOYER_ID = no,
                   ECO = peco,
                   AGE = page,
                   GENDER = pgender,
                   Q1 = pQ1,
                   Q1_1 = pQ1_1,
                   Q1_2 = pQ1_2,
                   Q2 = pQ2,
                   Q3 = pQ3,
                   Q4 = pQ4,
                   Q5 = pQ5,
                   Q6 = pQ6
                   
                   )
    conn.commit()
    
    dbClose(cursor, conn)
    return "OK"     
# -------------------------------------------------------------------------------------------
# 근로자 설문 입력하기
def setSurveyWorkerInsert(peco,page,pgender,pQ1,pQ1_1,pQ1_2,pQ2,pQ3,pQ4,pQ5,pQ6,pQ7) : 
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """SELECT nvl(max(WORKER_ID)+1, 1) as max_no
               FROM survey_worker"""
    cursor.execute(sql)
    rs_max_no = cursor.fetchone()
    no = rs_max_no[0]
    
    # 저장하기
    sql = """INSERT INTO survey_worker(
                WORKER_ID, ECO, AGE, GENDER, Q1,Q1_1,Q1_2,Q2,Q3,Q4,Q5,Q6,Q7
            ) VALUES (
                :WORKER_ID, :ECO, :AGE, :GENDER, :Q1,:Q1_1,:Q1_2,:Q2,:Q3,:Q4,:Q5,:Q6,:Q7
            )"""
    cursor.execute(sql,
                   WORKER_ID = no,
                   ECO = peco,
                   AGE = page,
                   GENDER = pgender,
                   Q1 = pQ1,
                   Q1_1 = pQ1_1,
                   Q1_2 = pQ1_2,
                   Q2 = pQ2,
                   Q3 = pQ3,
                   Q4 = pQ4,
                   Q5 = pQ5,
                   Q6 = pQ6,
                   Q7 = pQ7
                   
                   )
    conn.commit()
    
    dbClose(cursor, conn)
    return "OK"     
# -------------------------------------------------------------------------------------------  
# 고용주 설문조사 리스트
def getSurveyEmployerList() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql ="""SELECT q1
              FROM survey_employer
            """
    cursor.execute(sql)
    
    row = cursor.fetchall()
# 컬럼명 조회하기
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0].lower())
    
    dbClose(cursor, conn)

# 오라클 데이터 > 데이터 프레임
    df = pd.DataFrame(row, columns = col)
    df = df.astype(int)
    # df_list = [1,2,3,4,5,2,1,2,3,4,3,3,2,3,5,3,2,3,2,1,2,5,4,3,2,2,1,1,3,4,5,4,4,3,3,1,2,3,4]
    # df = pd.DataFrame(columns=['q1'])
    # df['q1'] = df_list
    
# 만족도 결과 데이터 프레임 생성  
    df_col = ['만족','불만족','보통']
    result_df = pd.DataFrame(columns = df_col)
    result_df['불만족'] = [len(df[df['q1']<=2])]
    result_df['만족'] = [len(df[df['q1']>=4])]
    result_df['보통'] = [len(df[df['q1']==3])]
    
    result_df = result_df.T.reset_index()
    
    return result_df
# -------------------------------------------------------------------------------------------  
# 근로자 설문조사 리스트
def getSurveyWorkerList() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql ="""SELECT q1
              FROM survey_worker
            """
    cursor.execute(sql)
    
    row = cursor.fetchall()
# 컬럼명 조회하기
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0].lower())
    
    dbClose(cursor, conn)
    
# 오라클 데이터 > 데이터 프레임
    df = pd.DataFrame(row, columns = col)
    df = df.astype(int)
# 만족도 결과 데이터 프레임 생성  
    df_col = ['만족','불만족','보통']
    result_df = pd.DataFrame(columns = df_col)
    result_df['불만족'] = [len(df[df['q1']<=2])]
    result_df['만족'] = [len(df[df['q1']>=4])]
    result_df['보통'] = [len(df[df['q1']==3])]
    
    result_df = result_df.T.reset_index()
    
    return result_df
# -------------------------------------------------------------------------------------------  