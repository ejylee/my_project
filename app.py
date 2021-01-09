# 저희가 해야하는 것은

# 데이터 수집해서 비교
# 수집한 데이터 메일로 보내주기

# 이 중에서 데이터 수집 비교와 메일로 보내주기는 했으니, 메일에 수집한 데이터를 추가해주는 것을 해봐야하는데
# 여러개의 데이터가 있는데 이 친구들을 한번씩 찾아볼게요
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

# 크롤링 데이터를 넣을 DB 연결하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

#유저들이 입력한 이메일 주소 db에 저장하기
db_data = list(db.users.find().limit(1))
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/index', methods=['POST'])
def email_received():
    # 클라이언트로부터 데이터 받기
    email_receive = request.form['user_email']  # 클라이언트로부터 url을 받는 부분
    # mongoDB에 데이터를 넣기
    email = {"email": email_receive}
    db.users.insert_one(email)

    return jsonify({'result': 'success'})

@app.route('/delete', methods=['POST'])
def delete_star():
    email_receive = request.form['user_email']
    email = {"email": email_receive}
    db.users.delete_one(email)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)