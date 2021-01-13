# 저희가 해야하는 것은

# 데이터 수집해서 비교
# 수집한 데이터 메일로 보내주기

# 이 중에서 데이터 수집 비교와 메일로 보내주기는 했으니, 메일에 수집한 데이터를 추가해주는 것을 해봐야하는데
# 여러개의 데이터가 있는데 이 친구들을 한번씩 찾아볼게요
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

# 크롤링 데이터를 넣을 DB 연결하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

#유저들이 입력한 이메일 주소 db에 저장하기
db_data = list(db.users.find().limit(1))

# 기존 db에 저장되어있던 가방들 최신값 가져오기
db_data = list(db.bags.find().limit(1))
# 가져온 값들 중 productID 리스트로 만들기
list1 = db_data[0]['productId']
print("여기는 list1")
print(list1)

# datadimenstion17 18은 뭔가요??
# 색상/무늬 텍스트 정보예요! 아 알겠습니다~
# ?! 차이나는 값의 productId, datadimension17, datadimension18, img 이메일로 보내주기
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendMail(a,b,c,d) :
    all_users = list(db.users.find({}))
    for user in all_users:
        all_emails = user['email']

    me = "brandnewsth@gmail.com"
    my_password = "spartacoding"
    you = all_emails

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "BRANDNEW HAWAII FIVE-O has arrived!"
    msg['From'] = me
    msg['To'] = you

    html = '<html><body><p>' + str(d) + '<br>' + '<h1 style="margin-top: 16px"> CLICK THE LINK TO GET IT! : https://www.freitag.ch/ko/f41?productID=' + str(a) + '</h1></p></body></html>'
    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()

# 새로 크롤링하기 (newBags 리스트 만들기)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.freitag.ch/ko/f41?items=showall',headers=headers)
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
path = "./chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.freitag.ch/ko/f41?items=showall")
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
bags = soup.select('#products-selector > ul > li')
productId = []
dataDimension17 = []
dataDimension18 = []
img = []
for bag in bags:
    productId.append(bag['data-product-id'])
    dataDimension17.append(bag['data-dimension17'])
    dataDimension18.append(bag['data-dimension18'])
    img.append(bag.select_one('img'))
# 혹시 메모장 켤 수 있나요????
list2 = productId

newBags = {'productId': productId}
print("여기는newBags")
print(newBags)

# ?! 기존 db에서 가져온 리스트 (dbBags) - 새로 크롤링한 리스트 (newBags) 비교하기
updated = list(set(list2) - set(list1))
print(list2)
print("결과값!!!!@#!@#!@#!@$!@$!@")
print(updated)
# 지금 updated에 데이터가 여러가 있고 이 productid 에 해당되는 demention과 img를 보내줘야하는데
# 저희가 알고 있는 값은 productid 밖에 없으니 이 친구를 이용해서 찾아보도록 하겠습니다.
# 일단 productid 를 하나씩 뽑아보면
for productid_list in updated :
    print("proudctid :" + productid_list)
    # 여기에서 productid 가 몇번째 있는지를 알아야 저 이미지와 색상 등이 몇번째 있는지 찾을 수 있겠죠?????
    # index를 이용해서 한다고 정보를 얻었습니다! 자 그러면
    print(productId.index(productid_list))
    index = productId.index(productid_list)
    print(productId[index])
    print(dataDimension17[index])
    print(dataDimension18[index])
    print(img[index])

if len(updated) == 0 :
    print("no change")
else :
    print("변한게 있어서 메일 보내줘야함!!!!")

    for productid_list in updated :
        print("proudctid :" + productid_list)
        # 여기에서 productid 가 몇번째 있는지를 알아야 저 이미지와 색상 등이 몇번째 있는지 찾을 수 있겠죠?????
        # 크롬을 한번 켜주실래용??
        # index를 이용해서 한다고 정보를 얻었습니다! 자 그러면
        print(productId.index(productid_list))
        index = productId.index(productid_list)
        # 정유님 혹시 번호가...? ㅋㅋㅋ 010 2550 82
        # 저기 밑에 숫자들이 117035 라는 프러덕트 아이디를 가지고 있는 친구가 17번쨰에 있으면
        print(productId[index])
        print(dataDimension17[index])
        print(dataDimension18[index])
        print(img[index])
        sendMail(productId[index], dataDimension17[index], dataDimension18[index], img[index])
#db.bags.insert_one(newBags)
driver.quit()