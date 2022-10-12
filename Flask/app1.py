# Flask 관련 모듈
from flask import Flask, render_template, request

# OCR 관련 모듈
import easyocr
import cv2
import math

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
      return render_template('/urlerror.html')
  
  # 동영상 정보추출
    # 1. pafy 라이브러리 사용
      # 추출 정보 : 동영상 제목, 채널명, 재생시간, 좋아요 수
  # video_info = pafy.new(input_url)

    # 2. 유튜브 크롤링
      # 추출 정보 : 동영상 채널 프로필사진, 구독자 수
  driver = webdriver.Chrome('C:/ChromeDriver_exe/chromedriver_105.exe')
  url = input_url
  driver.get(url)
  time.sleep(1)
  html = driver.page_source
  soup = bs(html, 'html.parser')
  
  profile_img = soup.select('#avatar #img')[1]['src']
  subscriber = soup.select_one('#upload-info #owner-sub-count').text.strip()
  # name = soup.select_one('#upload-info tp-yt-paper-tooltip #tooltip').text.strip()
  

  # contents = soup.select_one('yt-formatted-string[class="content style-scope ytd-video-secondary-info-renderer"]').text
  
  
    # 3. 유튜브 API
      # 추출 정보 : 썸네일 이미지
  DEVELOPER_KEY = 'AIzaSyDxkYbaXSkh7n-auPor6ZWUHBWRD3L75O8'
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

  req = youtube.videos().list(
      id = video_id,
      part = 'snippet, contentDetails, statistics'
  )

  res = req.execute()

  ch_id = res['items'][0]['snippet']['channelId']
  ch_title = res['items'][0]['snippet']['channelTitle']
  vi_title = res['items'][0]['snippet']['title']
  description =[]
  for i in range(len(res['items'][0]['snippet']['description'].split('\n'))):
    description.append(res['items'][0]['snippet']['description'].split('\n')[i])
  view_count = res['items'][0]['statistics']['viewCount']
  like_count = res['items'][0]['statistics']['likeCount']
  duration = res['items'][0]['contentDetails']['duration'].replace('PT', '').replace('H','시간 ').replace('M','분 ').replace('S','초')
  
  # ------------------------------------------------------------------------
  # 추천영상
  doru = requests.get(input_url)
  doru_text = bs(doru.text)
  doc = doru_text.select_one('meta[name="keywords"][content]')['content']


  search_response = youtube.search().list(
          q = doc,
          order = "relevance",
          part = "snippet",
          maxResults = 50
          ).execute()
          
  reco_url = []
  for i in range(0,10) :
      id = list(search_response['items'][i]['id'].values())[1]
      if list(search_response['items'][i]['id'])[1] == 'videoId' :
          reco_url.append(("https://www.youtube.com/watch?v={}".format(id)))
      else :
          reco_url.append(("https://www.youtube.com/watch?v={}".format(id)))
          # reco_url.append(("https://www.youtube.com/playlist?list={}".format(id)))
                  
  reco_title = []
  for i in range(0,10) :
          id = search_response['items'][i]['snippet']['title']
          reco_title.append(id)
                  
  reco_thumbnails = []
  for i in range(0,10) :
          id = search_response['items'][i]['snippet']['thumbnails']['medium']['url']
          reco_thumbnails.append(id)
  
  
    # 파일링 파일 불러오기
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


  return render_template('/learning.html', 
                        video_id=video_id, ch_id=ch_id, ch_title=ch_title, vi_title= vi_title, description=description,
                        view_count=view_count, like_count=like_count, duration=duration, subscriber=subscriber, 
                        profile_img=profile_img, df_list=df_list, 
                        reco_url=reco_url, reco_thumbnails=reco_thumbnails, reco_title=reco_title)
  # return render_template('/learning.html', context)

# ------------------------------------------------------------------------
# URL오류 화면
@app.route('/main') # 접속하는 url
def url_error():
  return render_template('/urlerror.html')
# ------------------------------------------------------------------------

# # 동영상 OCR테스트
# @app.route('/learning', methods = ['POST', 'GET']) # 접속하는 url
# def learning():
#   if request.method == 'POST':
#     input_url = request.form.get('url')
#     try :
#       if input_url.split('/')[2] == 'youtu.be':
#         video_id = input_url.split('/')[3]
#       elif input_url.split('?')[0] == 'https://www.youtube.com/watch': 
#         video_id = input_url.split('=')[1].split('&')[0]
        
#       embed_url = 'https://www.youtube.com/embed/' + video_id
#     except:
#       return render_template('/urlerror.html')
    
#   video_info = pafy.new(input_url)
#   video_path = video_info.getbest(preftype="mp4")

#   frame_images=[]
#   vidcap = cv2.VideoCapture(video_path.url)
#   fps = vidcap.get(cv2.CAP_PROP_FPS)
#   timestamps = [vidcap.get(cv2.CAP_PROP_POS_MSEC)]
#   calc_timestamps = [0.0]

#   count=0
#   success=True

#   # 1) 비디오 프레임 추출
#   while(vidcap.isOpened()):
#     vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
#     success, image = vidcap.retrieve()

#     # print('{}.sec reading a new frame: {}'.format(count, success))

#     frame_exists, curr_frame = vidcap.read()
#     if frame_exists:
#         timestamps.append(vidcap.get(cv2.CAP_PROP_POS_MSEC))
#         calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
#     else:
#         break

#     # 이미지 잘라서 저장
#     frame_images.append(image[95:1030,:])

#     # 프레임 추출을 위한 초 간격 설정
#     count += 1

#   vidcap.release()
  
#   # 2) 프레임 타임스탬프 생성
#   times = []

#   for t in timestamps :
#     sec = t/1000
#     times.append('{}:{:02d}'.format(math.trunc(sec/60), math.ceil(sec%60)))
  
#   # 이미지 자르기
#   # frame_image_crop = []
#   # for i in range(len(frame_images)):
#   #   frame_image_crop.append(frame_images[i][95:1030,:])

#   # 3) 이미지 유사도 측정
#   g_image = []
#   for i in range(len(frame_images)-1):
#     g_image.append(cv2.cvtColor(frame_images[i], cv2.COLOR_BGR2GRAY))

#   image_index = []
#   for i in range(len(g_image)-1):

#     image_A = g_image[i]
#     image_B = g_image[i+1]

#     # ssim : 두 이미지의 휘도, 대비, 구조 비교
#     (score, diff) = ssim(image_A, image_B, full=True)
    
#     # 유사도 스코어 조정
#     if score >= 0.975 :
#       image_index.append(i+1)
#     else :
#       pass

#   for i in sorted(image_index, reverse = True) :
#     del frame_images[i]
#     del times[i]
    
#   # 4) 텍스트 추출_EasyOCR
#   reader = easyocr.Reader(['ko','en'], gpu=True)
    
#   result = {}
#   for i in range(len(frame_images)):
#     # (변경전) result[times[i]] = reader.readtext(frame_images[i], detail = 0)
#     # paragraph 매개변수 추가 : 결과를 단락으로 정리하여 출력
#     # batch_size 매개변수 추가 : 속도 및 정확도 향상
#     result[times[i]] = reader.readtext(frame_images[i], detail = 0, paragraph=True, batch_size = 10)
  
#   return render_template('/learning.html', video_id = video_id, video_info = video_info, result = result)



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
                text_dict = qna_bot(r.recognize_google(audio, language='ko-KR'))
                row_list = []
                for key, val in text_dict.items():
                    temp_dict = {'key' : key, 'txt' : val[0], 'lnk' : val[1]}
                    row_list.append(temp_dict)

            except :
                pass

    except KeyboardInterrupt:
        pass

    return row_list

# 녹음 테스트
@app.route('/record') # 접속하는 url
def record():
  return render_template('/record.html')


# 질의응답 결과화면
@app.route('/qnaresult') # 접속하는 url
def qna_result():

  df = voice()
  
  return render_template('/qnaresult.html', df=df)





# ------------------------------------------------------------------------
# GET 테스트1
@app.route('/get1') # 접속하는 url
def get1():
    return render_template("get1.html")
# ------------------------------------------------------------------------
# POST 테스트2
@app.route('/get2', methods = ['POST', 'GET'] ) # 접속하는 url
def get2():
    if request.method == 'GET':
      url = request.args.get('id')
      return render_template("get2.html", url = url)
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
      return render_template("post2.html", url = url)
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
#테스트
@app.route('/test') # 접속하는 url
def test():
  return render_template("test.html")
# ------------------------------------------------------------------------

if __name__=="__main__":
  # app.run(host="192.168.0.60", port="5000", debug=True)
  # app.run(host="192.168.0.60", port="5000", debug=True, ssl_context='adhoc')
  # host 등을 직접 지정하고 싶다면
  app.run(host="127.0.0.1", port="5000", debug=True)
  
  
