#coding:utf-8
import hashlib
import urllib2
import json
import requests;
import time;
import datetime;
now = datetime.datetime.now()
minute = int(now.minute)
second = int(now.second)
if minute<10:
    minute = minute + 8;
if second<10:
    second = second + 10;
nowtime = '%s-%s-%s%%20%s:%s:%s' % (now.year,now.month,now.day,now.hour,minute,second)
md5time = '%s-%s-%s %s:%s:%s' % (now.year,now.month,now.day,now.hour,minute,second)
status = 'WAIT_BUYER_SEND_GOODS'
md5str = '4cb6087161a245f8dd1a1689de727234app_id92a427da5aab584f5eformatjsonmethodkdt.trades.sold.getsign_methodmd5statusWAIT_BUYER_CONFIRM_GOODStimestamp%sv1.04cb6087161a245f8dd1a1689de727234' % (md5time)
md5 = hashlib.md5(md5str.encode('utf-8')).hexdigest()
i = 21
while 1:
    try:
        url = 'https://open.koudaitong.com/api/entry?sign=%s&timestamp=%s&v=1.0&app_id=92a427da5aab584f5e&method=kdt.trades.sold.get&sign_method=md5&format=json&status=WAIT_BUYER_CONFIRM_GOODS' % (md5,nowtime)
        html = urllib2.urlopen(r'%s' % url)
        hjson = json.loads(html.read())
        total_re = int(hjson['response']['total_results'])
        print total_re
        phone = int(hjson['response']['trades'][0]['orders'][0]['buyer_messages'][1]['content'])
        name = str(hjson['response']['trades'][0]['orders'][0]['buyer_messages'][0]['content'].encode('utf-8'))
        num = str(hjson['response']['trades'][0]['tid'])
        product = hjson['response']['trades'][0]['orders'][0]['title']
        uproduct = str(product.encode('utf-8'))
        msg = '%s,您好！您已成功在放学嗨平台购买了%s，订单编号：%s,在开场前一小时内凭此短信到厦门市工人体育馆正门口领取入场门票，如有疑问，请联系放学嗨客服：0592-2042105。【放学嗨】' % (name,uproduct,num)
        if total_re >= i:
            i += 1
            def send_messag_example():
                resp = requests.post(("http://sms-api.luosimao.com/v1/send.json"),
                auth=("api", "key-76ac37b65840cb9b4260fd79fb78c7d7"),
                data={
                "mobile": phone,
                "message": msg,
                },timeout=3 , verify=False);
                result =  json.loads( resp.content )
                print '已经发送成功！'
        else:
            print '等待新用户'
    except:
    	print 'error happend'
    time.sleep(30)
