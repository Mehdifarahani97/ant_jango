
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pymysql

import requests
from bs4 import BeautifulSoup
import pymysql
import time

from django.core.serializers.json import DjangoJSONEncoder
import requests

from datetime import date
url = 'https://kr.investing.com/instruments/HistoricalDataAjax'

class Bond2(APIView):

    def get(self, request, format=None, ):
        data = []
        print('시작')
        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        sql = "SELECT dates FROM bond2 ORDER BY dates desc LIMIT 1"
        cursor.execute(sql)
        rows = cursor.fetchall()
        mydate = datetime.strptime(str(rows[0]['dates']), '%Y-%m-%d')
        finaldate = mydate + relativedelta(days=+1)

        print(str(finaldate)[:10].replace("-","/"))
        start_date = str(finaldate)[:10].replace("-","/")
        today = date.today();
        end_date = str(today).replace("-", "/")

        print("날짜의 차",  str(rows[0]['dates'] - today)[0])

        if (str(rows[0]['dates'] - today)[0] != '0'):
            data = {
                'curr_id': '23701',
                'smlID': '200602',
                'header': '미국 2년 채권 수익률 내역',
                'st_date': start_date,
                'end_date': end_date,
                'interval_sec': 'Daily',
                'sort_col': 'date',
                'sort_ord': 'DESC',
                'action': 'historical_data'
            }

            res = requests.post(url, data, headers={'X-Requested-With': 'XMLHttpRequest',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}).content
            #print(data)
            soup = BeautifulSoup(res, 'html.parser')

            items = soup.find('table', id='curr_table').find('tbody').find_all('tr')
            #print(items)
            for item in items:
            # 아래 두 줄은 앞에 탭을 입력하셔야 합니다...
                l = item.find_all('td')
                datekor = l[0].text
                dates = datekor.replace('년','-').replace('월','-').replace('일','').replace(' ','')
                print(l[0].text, '/', l[1].get('data-real-value'), '/', l[2].get('data-real-value'), '/', l[3].get('data-real-value'), '/', l[4].get('data-real-value'))

                cursor = conn.cursor()

                sql = "insert into bond2(dates, price, open, high, low, keyword) values('{}', {}, {}, {}, {}, '{}')".format(
                dates, l[1].get('data-real-value'), l[2].get('data-real-value'), l[3].get('data-real-value'),
                l[4].get('data-real-value'), "미국/채권/2년")

                print(sql)
                cursor.execute(sql)
                conn.commit()
                cursor.close()

                time.sleep(3)

        cursor3 = conn.cursor()

        # 테이블 변경
        sql3 = "select * from bond2 order by dates asc"
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
            sql4 = "update bond2 set changedate = {} where dates = '{}'".format(n['changedate'], n['dates'])

            cursor4.execute(sql4)
            print(sql4)
            conn.commit()
        cursor4.close()

        conn.close()
        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)
        print("testindi2")

        return Response(serializer.data);

