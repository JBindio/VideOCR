# app.py
from re import I
from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------------------------------------------------------------
# 메인 화면
@app.route('/main') # 접속하는 url
def main():
  return render_template('main1.html')
# ------------------------------------------------------------------------

@app.route('/main2') # 접속하는 url
def main2():
  return render_template('main2.html')
# ------------------------------------------------------------------------

@app.route('/result', methods =['GET','POST']) # 접속하는 url
def result():
    if request.method == 'GET':
        tt = request.args.get('tt')
    elif request.method =='POST':
        tt = request.form.get('tt')
        
    return render_template('result.html', tt=tt)
# ------------------------------------------------------------------------

if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)
  
  
@app.route('/get2', methods = ['POST', 'GET'] ) # 접속하는 url
def get2():
    if request.method == 'GET':
      url = request.args.get('id')
      return render_template("get2.html", url = url)
# ------------------------------------------------------------------------