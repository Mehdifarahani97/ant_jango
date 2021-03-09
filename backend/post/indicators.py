
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
import math
import time
from datetime import date, timedelta


class usdkrw(APIView):
    def get(self, request, format=None):
        print('시작')
        apikey = "KDqozvh7wMKStFfUb4EGLkI5iXqgLB8i"

        api = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={key}&searchdate={date}&data=AP01"
        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        cursor2 = conn.cursor()
        sql2 = "SELECT dates FROM usdkrw ORDER BY dates desc LIMIT 1"
        cursor2.execute(sql2)
        rows = cursor2.fetchall()
        print("최근날짜",rows[0]['dates'])

        today = date.today();
        print('today is ', str(today).replace("-", ""))
        print("날짜의 차 test", str(rows[0]['dates'] - today)[0])
        if(str(rows[0]['dates'] - today)[0] != '0'):

            mydate = datetime.strptime(str(today).replace("-", ""), '%Y%m%d')
            dates = []
            for i in range(1, int(str(rows[0]['dates'] - today).split('-')[1].split(' ')[0])):
                beforemonth = mydate + relativedelta(days=-i)
                strdate = beforemonth.strftime("%Y%m%d")
                dates.append(strdate)

            print(dates)

            for i in dates:
                url = api.format(date=i, key=apikey)
                res = requests.get(url)
                data = json.loads(res.text)
                print("데이터 확인", data)
                if (len(data) != 0):

                    year = i[:4]
                    month = i[4:6]
                    day = i[-2:]
                    alldate = "{}-{}-{}".format(year, month, day)
                    print(alldate)

                    cursor = conn.cursor()
                    sql = "insert into usdkrw(price, dates) values({}, '{}')".format(
                        data[-1]["deal_bas_r"].replace(",", ""), alldate)

                    print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    data = json.dumps(cursor.fetchall(), cls=DjangoJSONEncoder)

                    cursor.close()

                    time.sleep(1)

        else:
            data = []
        data = []
        cursor3 = conn.cursor()

        # 테이블 변경
        sql3 = "select * from usdkrw order by dates asc"
        cursor3.execute(sql3)
        data2 = cursor3.fetchall()
        cursor3.close()

        prev = 0
        result = []
        for idx, n in enumerate(data2):
            if (idx == 0):
                prev = n['price']
                continue
            rates = round(((n['price'] - prev) / prev) * 100, 3)
            prev = n['price']
            temp = dict(dates=n['dates'], changedate=rates)
            result.append(temp)

        cursor4 = conn.cursor()

        for n in result:
            # 테이블 변경
            sql4 = "update usdkrw set changedate = {} where dates = '{}'".format(n['changedate'], n['dates'])

            cursor4.execute(sql4)
            print(sql4)
            conn.commit()
        cursor4.close()

        conn.close()
        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)
        print("test")

        return Response(serializer.data);

