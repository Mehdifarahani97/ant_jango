
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
import json
from datetime import date
url = 'https://kr.investing.com/instruments/HistoricalDataAjax'

class Eurusd(APIView):

    def get(self, request, format=None, ):
        data = []
        print('eurusd 확인')

        # url 지정
        api = "https://api.exchangeratesapi.io/history?start_at={date1}&end_at={date2}&base={country}"

        # 국가 지정
        cont = "EUR"

        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)

        cursor = conn.cursor()
        sql = "SELECT dates FROM exechangerate where exechange_name='달러/유로' ORDER BY dates desc LIMIT 1"
        cursor.execute(sql)
        rows = cursor.fetchall()

        today = date.today();
        todays = datetime.strptime(str(today), '%Y-%m-%d')
        mydate = datetime.strptime(str(rows[0]['dates']), '%Y-%m-%d')
        finaldate = mydate + relativedelta(days=+1)
        todaydate = todays + relativedelta(days=+0)
        print("날짜 마지막 확인")

        print(str(finaldate - todaydate))
        dates = [str(finaldate)[:10], str(today)]
        print(dates)
        print(str(finaldate - todaydate)[0])
        if (str(finaldate - todaydate)[0] != '0'):
            url = api.format(date1=dates[0], date2=dates[1], country=cont)
            print(url)
            res = requests.get(url)
            data = json.loads(res.text)
            print(data)

            print("시작")
            print('  환율 :', data["rates"])
            for i in data["rates"]:
                print(i)

                cursor = conn.cursor()
                sql = "insert into exechangerate(dates, exechange_name, symbol, price) values('{}', '달러/유로', 'EURUSD', {})".format(
                    i, data["rates"][i]['USD'])

                print(sql)
                cursor.execute(sql)
                conn.commit()
                cursor.close()

                time.sleep(3)

        sql = "SELECT dates FROM eurusd ORDER BY dates desc LIMIT 1"
        cursor2 = conn.cursor()
        cursor2.execute(sql)
        rows = cursor2.fetchall()
        mydate = datetime.strptime(str(rows[0]['dates']), '%Y-%m-%d')
        finaldate = mydate + relativedelta(days=+1)

        print(str(finaldate)[:10].replace("-", "/"))
        start_date = str(finaldate)[:10].replace("-", "/")
        today = date.today();
        end_date = str(today).replace("-", "/")
        url = 'https://kr.investing.com/instruments/HistoricalDataAjax'
        if (str(rows[0]['dates'] - today)[0] != '0'):


            data = {
                'curr_id': '1',
                'smlID': '106682',
                'header': 'EUR/USD 내역',
                'st_date': start_date,
                'end_date': end_date,
                'interval_sec': 'Daily',
                'sort_col': 'date',
                'sort_ord': 'DESC',
                'action': 'historical_data'
            }

            res = requests.post(url, data, headers={'X-Requested-With': 'XMLHttpRequest',
                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}).content
            soup = BeautifulSoup(res, 'html.parser')

            items = soup.find('table', id='curr_table').find('tbody').find_all('tr')

            for item in items:
             # 아래 두 줄은 앞에 탭을 입력하셔야 합니다...
                l = item.find_all('td')
                datekor = l[0].text
                dates = datekor.replace('년', '-').replace('월', '-').replace('일', '').replace(' ', '')
                print(l[0].text, '/', l[1].get('data-real-value'), '/', l[2].get('data-real-value'), '/',
                          l[3].get('data-real-value'), '/', l[4].get('data-real-value'))

                cursor3 = conn.cursor()

                sql = "insert into eurusd(dates, price, open, high, low, keyword) values('{}', {}, {}, {}, {}, '{}')".format(
                        dates, l[1].get('data-real-value'), l[2].get('data-real-value'), l[3].get('data-real-value'),
                        l[4].get('data-real-value'), "유로/달러/유로달러")

                print(sql)
                cursor3.execute(sql)
                conn.commit()
                cursor3.close()

                time.sleep(3)
        cursor4 = conn.cursor()

            # 테이블 변경
        sql3 = "select * from eurusd order by dates asc"
        cursor4.execute(sql3)
        data2 = cursor4.fetchall()
        cursor4.close()

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

        cursor5 = conn.cursor()

        for n in result:
            # 테이블 변경
            sql4 = "update eurusd set changedate = {} where dates = '{}'".format(n['changedate'], n['dates'])

            cursor5.execute(sql4)
            print(sql4)
            conn.commit()
        cursor5.close()

        conn.close()


        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)
        print("testindi2")

        return Response(serializer.data);

