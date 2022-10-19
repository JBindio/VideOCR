# Flask 관련 모듈
from flask import Flask, render_template, request

# OCR 관련 모듈
import easyocr
import cv2
import math
from hanspell import spell_checker
import pandas as pd
import numpy as np
import re
import pafy
import matplotlib.pyplot as plt
import csv
from string import Template
from typing import Iterable, List, Tuple, Optional, Dict, Callable, Union, TextIO
import threading
import queue
import logging
import math
import sys
from skimage.metrics import structural_similarity as ssim
from glob import glob

from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images, write_scene_list_html
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.platform import (tqdm, get_and_create_path, get_cv2_imwrite_params)
from scenedetect.video_stream import VideoStream
from scenedetect.stats_manager import StatsManager, FrameMetricRegistered
from scenedetect.scene_detector import SceneDetector, SparseSceneDetector
from scenedetect.thirdparty.simpletable import (SimpleTableCell, SimpleTableImage, SimpleTableRow,
                                                SimpleTable, HTMLPage)
logger = logging.getLogger('pyscenedetect')

# 크롤링 관련 모듈
import pafy
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

# Youtube API 관련 모듈
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# 해시태그 관련 모듈
import itertools
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from ckonlpy.tag import Twitter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from konlpy.tag import Okt

# STT 질의응답 관련 모듈
import requests
from konlpy.tag import Okt
import speech_recognition as sr
import glob
from pydub import AudioSegment

# ------------------------------------------------------------------------
#Flask 객체 인스턴스 생성
app = Flask(__name__)
# ------------------------------------------------------------------------
# ajax 테스트
@app.route('/ajax1') # 접속하는 url
def ajax1():
  return render_template('test/ajax1.html')

@app.route('/ajax2') # 접속하는 url
def ajax2():
  result = request.args.get('val')
  return render_template('test/ajax2.html', result=result)
# ------------------------------------------------------------------------
# 메인 화면
@app.route('/main') # 접속하는 url
def main():
  return render_template('/main.html')

# ------------------------------------------------------------------------
# 동영상 화면
@app.route('/learning', methods = ['POST', 'GET']) # 접속하는 url
def learning():
  # POST 형식 request
  if request.method == 'POST':
    # 동영상 url 주소 받아오기 
    input_url = request.form.get('url')
    # 동영상 id 추출하기
    try :
      # url 타입1 - youtu.be 형식 (공유)
      if input_url.split('/')[2] == 'youtu.be':
        video_id = input_url.split('/')[3]
      # url 타입2 - watch 형식 (주소창 복사)
      elif input_url.split('?')[0] == 'https://www.youtube.com/watch': 
        video_id = input_url.split('=')[1].split('&')[0]
    except:
      # 잘못된 url입력시 처리
      return render_template('/urlerror.html')
  
# ------------------------------------------------------------------------
  

    
  
  # ------------------------------------------------------------------------
  # 유튜브 정보 크롤링
  
  # pafy 라이브러리
  # video_info = pafy.new(input_url)

  #  유튜브 사이트 크롤링
  # driver = webdriver.Chrome('C:/ChromeDriver_exe/chromedriver_105.exe')
  # url = input_url
  # driver.get(url)
  # time.sleep(1)
  # html = driver.page_source
  # soup = bs(html, 'html.parser')
  
  # profile_img = soup.select('#avatar #img')[1]['src']
  # subscriber = soup.select_one('#upload-info #owner-sub-count').text.strip()
  # name = soup.select_one('#upload-info tp-yt-paper-tooltip #tooltip').text.strip()
  # contents = soup.select_one('yt-formatted-string[class="content style-scope ytd-video-secondary-info-renderer"]').text
  
  # 유튜브 API
  # API 정보입력
  DEVELOPER_KEY = 'API Key'
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"

  # API 빌드
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

  # 비디오 정보 API
  videos_res = youtube.videos().list(
      id = video_id,
      part = 'snippet, contentDetails, statistics'
  ).execute()
  
  # 채널아이디, 채널이름, 비디오이름, 비디오설명, 조회수, 좋아요수, 재생시간
  ch_id = videos_res['items'][0]['snippet']['channelId']
  ch_title = videos_res['items'][0]['snippet']['channelTitle']
  vi_title = videos_res['items'][0]['snippet']['title']
  vi_description =[]
  for i in range(len(videos_res['items'][0]['snippet']['description'].split('\n'))):
    vi_description.append(videos_res['items'][0]['snippet']['description'].split('\n')[i])
  vi_view_count = videos_res['items'][0]['statistics']['viewCount']
  vi_like_count = videos_res['items'][0]['statistics']['likeCount']
  vi_duration = videos_res['items'][0]['contentDetails']['duration'].replace('PT', '').replace('H','시간 ').replace('M','분 ').replace('S','초')
  
  # 채널 정보 API
  channels_res = youtube.channels().list(
    id = ch_id,
    part = 'snippet, statistics',
  ).execute()

  # 채널 이미지
  ch_img = channels_res['items'][0]['snippet']['thumbnails']['medium']['url']
  
  # 채널 구독자수(만명, 천명 처리)
  ch_subscriber = channels_res['items'][0]['statistics']['subscriberCount']
  if len(ch_subscriber) >= 7:
    ch_subscriber = ch_subscriber[0:-4]+'만명'
  elif len(ch_subscriber) == 6:
    ch_subscriber = ch_subscriber[0:-4]+'.'+ ch_subscriber[-4:-3]+'만명'
  elif len(ch_subscriber) == 5:
    ch_subscriber = ch_subscriber[0:-4]+'.'+ ch_subscriber[-4:-2]+'만명'
  elif len(ch_subscriber) == 4:
    ch_subscriber = ch_subscriber[0:-3]+'.'+ ch_subscriber[-4:-2]+'천명'
  else :
    ch_subscriber = ch_subscriber +'명'

  # 추천영상
  # 추천영상을 위한 키워드 추출
  reco_url = requests.get(input_url)
  reco_text = bs(reco_url.text)
  reco_keyword = reco_text.select_one('meta[name="keywords"][content]')['content']
  
  # 검색 정보 API
  search_res = youtube.search().list(
          q = reco_keyword,
          order = "relevance",
          part = "snippet",
          maxResults = 50
          ).execute()
  # 키워드 검색 결과 상위 10개 영상 추출
  reco_url = []
  for i in range(0,10) :
      id = list(search_res['items'][i]['id'].values())[1]
      if list(search_res['items'][i]['id'])[1] == 'videoId' :
          reco_url.append(("https://www.youtube.com/watch?v={}".format(id)))
      else :
          reco_url.append(("https://www.youtube.com/watch?v={}".format(id)))
          # reco_url.append(("https://www.youtube.com/playlist?list={}".format(id)))
          
  # 상위 10개 영상 제목
  reco_title = []
  for i in range(0,10) :
          id = search_res['items'][i]['snippet']['title']
          reco_title.append(id)
  
  # 상위 10개 썸네일 이미지
  reco_thumbnails = []
  for i in range(0,10) :
          id = search_res['items'][i]['snippet']['thumbnails']['medium']['url']
          reco_thumbnails.append(id)
  
  # ------------------------------------------------------------------------
  # OCR 파일링
  # 파일링 파일 불러오기
  try:
    df = pd.read_csv('textfile/{}.csv'.format(video_id))
    
    # start timestamps 생성
    start_indexplus_one = ['0:00']

    for i in range(len(df)) :
      min = pd.to_numeric(df['timestamps'].str.split(':')[i][0])
      sec = pd.to_numeric(df['timestamps'].str.split(':')[i][1])

      start = (min*60) + sec + 1
      start_indexplus_one.append('{}:{:02d}'.format(math.trunc(start/60), math.ceil(start%60)))


    df['start_timestamps'] = ''

    for i in range(len(start_indexplus_one)) :
      if i == 0 : 
        df['start_timestamps'].loc[i] = start_indexplus_one[0]
      else:
        df['start_timestamps'].loc[i] = start_indexplus_one[i]


    df_list = []
    for i in range(len(df)):
      df_list.append(dict(df.loc[i]))
  except:
    df_list = [{'timestamps': '0:00',
                'checked': '영상 내 자막을 찾지 못했습니다',
                'start_timestamps': '0:00'
                }]
  
  hash_df = pd.read_csv('textfile/{}.csv'.format(video_id))
  
  hash_test = hash_df["checked"]
  
  hash_doc = list(hash_test)
  
  stopwords = './textfile/stopwords.csv'
  hash_text = pd.read_csv(stopwords)
  hash_text_list = list(np.array(hash_text['불용어'].tolist()))
  twitter = Twitter()
  twitter.add_dictionary(['암묵지','창출','유즈 케이스','유즈케이스','내재화','해결','고려사항','장기적','단기적','사이언티스트','전처리','이상치','결측치',
                          '학습용 데이터','인공지능','텍스트 마이닝','메타버스','키워드','시사점','가속화','선도국','고품질','적극적','투자','불확실성','감소',
                          '중장기','장년층','노년층','상대적','최소화','디지털 리터러시 교육','세대별','맞춤형','어디서나','특성','긍정적','시공간'], 'Noun')
  key_part = []
  tokenized_nouns = []
  tokenized_nouns_11 = []
  result = []
  candidates = []
  
  for i in range(0,len(hash_doc)) :
    key_part.append(twitter.pos(hash_doc[i]))
    tokenized_nouns.append(','.join([word[0] for word in key_part[i] if word[1] == 'Noun']))
    tokenized_nouns_11.append([tokenized_nouns[i]])
    result.append([word for word in tokenized_nouns_11[i] if not word in hash_text_list])

    n_gram_range = (0, 3)
    
    count = CountVectorizer(ngram_range=n_gram_range).fit(result[i])
    temp_ = list(count.get_feature_names_out())
    candidates.append(temp_)
      
  result = []
  
  for i in range(len(candidates)):
    result += candidates[i]
  
  result = list(set(result))  
  model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
  doc_embedding = model.encode([hash_test])
  candidate_embeddings = model.encode(result)
  
  top_n = 5
  distances = cosine_similarity(doc_embedding, candidate_embeddings)
  # keywords = [result[index] for index in distances.argsort()[0][-top_n:]]
  
  # distances = cosine_similarity(doc_embedding, candidate_embeddings)

# 각 키워드들 간의 유사도
  distances_candidates = cosine_similarity(candidate_embeddings, 
                                      candidate_embeddings)

# 코사인 유사도에 기반하여 키워드들 중 상위 top_n개의 단어를 pick.
  words_idx = list(distances.argsort()[0][-30:])

  words_vals = [result[index] for index in words_idx]
  distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

  # 각 키워드들 중에서 가장 덜 유사한 키워드들간의 조합을 계산
  min_sim = np.inf
  candidate = None
  
  for combination in itertools.combinations(range(len(words_idx)), top_n):
      sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
      if sim < min_sim:
        candidate = combination
        min_sim = sim
        
  hash_keybert = [words_vals[idx] for idx in candidate]
  hash_youtube = reco_keyword.split(', ')


  return render_template('/learning.html', 
                        video_id=video_id, vi_title= vi_title, vi_description=vi_description,
                        vi_view_count=vi_view_count, vi_like_count=vi_like_count, vi_duration=vi_duration, 
                        ch_id=ch_id, ch_title=ch_title, ch_img=ch_img, ch_subscriber=ch_subscriber,
                        reco_url=reco_url, reco_thumbnails=reco_thumbnails, reco_title=reco_title,
                        df_list=df_list, hash_keybert = hash_keybert, hash_youtube = hash_youtube)
  
# ------------------------------------------------------------------------
# URL오류 화면
@app.route('/main') # 접속하는 url
def url_error():
  return render_template('/urlerror.html')

# ------------------------------------------------------------------------
# 질의응답 함수
def qna_bot(text):
  word_dic = {}  
  okt = Okt()
  sum_text = ''

  tokenized_doc = okt.pos(text)
  
  for word in tokenized_doc:

    if word[1] == 'Noun':
    
      url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=kdic&query={}'.format(word[0])
      html = requests.get(url)
      soup = bs(html.text, 'html.parser')
      try:
        temp_sum = soup.select('span[class="lnk_sub_tit elss"]')[0].text
      except:
        word_dic[word[0]] = ['키워드 검색결과 없음', url]
        continue
      
      lnk = soup.select('a[class="lnk_tit"]')[0].attrs['href']

      if temp_sum != sum_text:
        sum_text = temp_sum
        word_dic[word[0]] = [sum_text, lnk]
      else:
        word_dic[word[0]] = ['링크에서 내용을 확인해주세요', lnk]
  
  return word_dic

# ------------------------------------------------------------------------
# 질의응답 녹음
def voice():
    try:
        r = sr.Recognizer()
        
        # with sr.Microphone() as source:
        #     print('음성을 입력하세요.')
        #     audio = r.listen(source)
        
        # with open('C:/DEV/STUDY/FinalProject/flasktest/static/wav/qna.wav', "wb") as file:   # open in binary mode
        #   response = requests.get(url)
        #   file.write(response.content)
        with open('C:/Users/admin/Downloads/qna.wav', 'w'):
            pass
        output = glob.glob('C:/Users/admin/Downloads/*.weba')
        
        file = output[-1]
        
        audioSegment = AudioSegment.from_file(file, 'webm')
        
        new_file_path = 'C:/Users/admin/Downloads/qna.wav'
        
        audioSegment.export(new_file_path, format='wav')
        
        row_source = sr.AudioFile(new_file_path)

        with row_source as source:
            audio = r.record(source)
            try:
                print('음성변환 : ' + r.recognize_google(audio, language='ko-KR'))
                recog_text = r.recognize_google(audio, language='ko-KR')
                text_dict = qna_bot(r.recognize_google(audio, language='ko-KR'))
                row_list = []
                for key, val in text_dict.items():
                    temp_dict = {'key' : key, 'txt' : val[0], 'lnk' : val[1]}
                    row_list.append(temp_dict)

            except :
                pass

    except KeyboardInterrupt:
        pass

    return row_list, recog_text
  
# ------------------------------------------------------------------------
# 녹음 테스트
@app.route('/record') # 접속하는 url
def record():
  return render_template('/record.html')

# ------------------------------------------------------------------------
# 질의응답 결과화면
@app.route('/qnaresult') # 접속하는 url
def qna_result():

  df, recog_txt = voice()
  
  return render_template('/qnaresult.html', df=df, recog_txt=recog_txt)

# ------------------------------------------------------------------------




# ------------------------------------------------------------------------
# GET 테스트1
@app.route('/get1') # 접속하는 url
def get1():
  return render_template("test/get1.html")

# ------------------------------------------------------------------------
# POST 테스트2
@app.route('/get2', methods = ['POST', 'GET'] ) # 접속하는 url
def get2():
  if request.method == 'GET':
    url = request.args.get('id')
    return render_template("test/get2.html", url = url)
  
# ------------------------------------------------------------------------
# POST 테스트1
@app.route('/post1') # 접속하는 url
def post1():
  return render_template("post1.html")
  
# ------------------------------------------------------------------------
# POST 테스트2
@app.route('/post2', methods = ['POST', 'GET'] ) # 접속하는 url
def post2():
  if request.method == 'POST':
    url = request.form.get('id')
    return render_template("test/post2.html", url = url)
  
# ------------------------------------------------------------------------
#테스트
@app.route('/test') # 접속하는 url
def test():
  return render_template("test/test.html")

# ------------------------------------------------------------------------

if __name__=="__main__":
  # app.run(host="192.168.0.60", port="5000", debug=True)
  # app.run(host="192.168.0.60", port="5000", debug=True, ssl_context='adhoc')
  # host 등을 직접 지정하고 싶다면
  app.run(host="127.0.0.1", port="5000", debug=True)
