#coding:utf-8
import MySQLdb as mdb;
import sys;
import requests;
import json;
import time;
#连接数据库
con = mdb.connect('IP','user','password','table');
cur = con.cursor()
list1 = []
while 1:
    cur.execute("SET @id = (SELECT user_id FROM xy_q_ticket_record ORDER BY id DESC LIMIT 1)")
    #查询活动表中最后的那条数据
    cur.execute("SELECT a.id, a.user_id, b.id, b.phone from xy_q_ticket_record a, xy_member b where a.user_id = b.id and b.id = @id")
    #关联查询，获取用户手机号码
    last_phone_str = cur.fetchone()[3]
    last_phone = last_phone_str
    last_phone_int = int(last_phone_str)
    cur.execute("SET @id = (SELECT user_id FROM xy_q_ticket_record ORDER BY id DESC LIMIT 1)")
    #查询活动表中最后的那条数据
    cur.execute("SELECT a.id, a.user_id, b.id, b.phone from xy_q_ticket_record a, xy_member b where a.user_id = b.id and b.id = @id")
    #关联查询，获取用户ID
    last_id_int = int(cur.fetchone()[2])
    last_id_str = str(last_id_int)
    cur.execute("SELECT user_id FROM fangxuehai.xy_aqiyi_record")
    send_id = cur.fetchall()
    cur.execute("SELECT id FROM fangxuehai.xy_aqiyi_record ORDER BY id DESC LIMIT 1")
    n = int(cur.fetchone()[0])
    for i in range(len(send_id)) :
        for j in range(len(send_id[i])):
            list1.append(send_id[i][j])
    if last_id_str in list1:
        last_phone = '0',
        print '已经给该用户发送过了'
    if last_id_int < 7000:
        last_phone = '0'
        print '用户不是新注册，程序中断。'
    cur.execute("SELECT * FROM xy_aqiyi where id = %s" % (n))
    all_aqiyi = cur.fetchone()
    aqiyi_user = all_aqiyi[1]
    aqiyi_password = all_aqiyi[2]
    msg = "您的专属爱奇账号为：%s,密码为：%s【放学嗨】" % (aqiyi_user,aqiyi_password)
    def send_messag_example():
        resp = requests.post(("http://sms-api.luosimao.com/v1/send.json"),
        auth=("api", "KEY-luosimao "),
        data={
        "mobile": last_phone,
        "message": msg,
        },timeout=3 , verify=False);
        result =  json.loads( resp.content )
        print result
        global n
        if result == {u'msg': u'ok', u'error': 0}:
            n += 1
            value = [last_id_int ,last_phone_int ,aqiyi_user ,aqiyi_password, n]
            cur.execute("INSERT INTO xy_aqiyi_record VALUES %s", (value,))
            con.commit()
            print '已经给用户id=%s的发送了一条短信,账号：%s,密码：%s' % (last_id_int,aqiyi_user,aqiyi_password)
        else:
            print '当前n = %s。' % n
    if __name__ == "__main__":
            send_messag_example();
    time.sleep(30)
