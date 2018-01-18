#-*- coding:utf-8 -*-

from flask import  Flask,request
from flask.ext.script import Manager
from ding import Ding,get_sendurl_with_token

app = Flask(__name__)
manger = Manager(app)

secret = ('corpid',
          'secretid'
         )

token,send_url = get_sendurl_with_token(secret)

@app.route('/api',methods=['POST'])
def redmine():
    data = request.get_data()
    dd = Ding(data,send_url)
    user_result = dd.get_mailaddr()
    if user_result['status']:
        userid = user_result['userid']
        dd.send(userid)
    else:
        print 'Can not search userid by email addres'
    return 'Send finsh'

if __name__ == '__main__':
    manger.run()
