
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pymysql

from django.core.serializers.json import DjangoJSONEncoder
import requests
import json

import time


class usdkrw(APIView):
    def get(self, request, format=None):
        print('시작')
        apikey = "KDqozvh7wMKStFfUb4EGLkI5iXqgLB8i"

        nal = '20210128'
        mydate = datetime.strptime(nal, '%Y%m%d')
        dates = []
        for i in range(1, 10):
            beforemonth = mydate + relativedelta(days=-i)
            strdate = beforemonth.strftime("%Y%m%d")
            dates.append(strdate)
        print(dates)

        api = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={key}&searchdate={date}&data=AP01"
        conn = pymysql.connect(host='15.165.162.193', user='root', password='admin1234', db='springyun', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        print('연결성공')

        for i in dates:
            url = api.format(date=i, key=apikey)
            res = requests.get(url)
            data = json.loads(res.text)

            if (len(data) != 0):
                print('  수치 :', data[-1]["deal_bas_r"].replace(",", ""))
                print('  날짜 :', i)
                year = i[:4]
                month = i[4:6]
                day = i[-2:]
                alldate = "{}-{}-{}".format(year, month, day)
                print(alldate)

                cursor = conn.cursor()
                sql = "insert into usdkrw(rates, dates) values({}, '{}')".format(
                    data[-1]["deal_bas_r"].replace(",", ""), alldate)

                print(sql)
                cursor.execute(sql)
                conn.commit()
                data = json.dumps(cursor.fetchall(), cls=DjangoJSONEncoder)
                cursor.close()

                time.sleep(1)
        conn.close()
        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)
        print("test")
        return Response(serializer.data);

