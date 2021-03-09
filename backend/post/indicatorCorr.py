
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers

from scipy.stats import pearsonr

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

data1 = ["bitcoin", "bond10", "bond2", "dolleridx", "goldfor", "usdkrw", "wti"]
data2 = ["EURUSD", "USDJPY", "USDCNY", "USDGBP"]
list1 = []
list2 = []

class Corr(APIView):

    def get(self, request, format=None, ):
        data = []
        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)

        # data1 - data1
        for i in data1:
            for v in data1:
                print(i, v)
                cursor = conn.cursor()
                sql = "select r.dates, r.price x, e.price y from " + i + " r inner join " + v + " e WHERE r.dates = e.dates order by r.dates asc"

                print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("확인")
                print(rows)
                for row in rows:
                    print(row['x'])
                    print(row['y'])
                    list1.append(row['x'])
                    list2.append(row['y'])
                # print(rows)
                conn.commit()
                cursor.close()

                time.sleep(3)
                correlation = pearsonr(list1, list2)
                print(correlation)
                a, b = correlation
                print('최종')
                print(a)
                a = str(a)
                sql2 = "UPDATE corr SET " + i + "=" + a + " WHERE indicator='" + v + "'"
                print(sql2)
                cursor2 = conn.cursor()

                cursor2.execute(sql2)
                conn.commit()
                cursor2.close()

                list1.clear()
                list2.clear()
                print(list1)
                print(list2)

        # data2 - data1
        for i in data1:
            for v in data2:
                print(i, v)
                cursor = conn.cursor()
                sql = "select r.dates, r.price x, e.price y from (select dates, price from " + i + ")  r inner join (select dates, price from exechangerate where symbol='" + v + "') e WHERE r.dates = e.dates order by r.dates asc"

                print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    print(row['x'])
                    print(row['y'])
                    list1.append(row['x'])
                    list2.append(row['y'])
                        # print(rows)
                conn.commit()
                cursor.close()

                time.sleep(3)
                correlation = pearsonr(list1, list2)
                print(correlation)
                a, b = correlation
                print('최종')
                print(a)
                a = str(a)
                sql2 = "UPDATE corr SET " + i + "=" + a + " WHERE indicator='" + v + "'"
                print(sql2)
                cursor2 = conn.cursor()

                cursor2.execute(sql2)
                conn.commit()
                cursor2.close()

                sql3 = "UPDATE corr SET " + v + "=" + a + " WHERE indicator='" + i + "'"
                print(sql3)
                cursor3 = conn.cursor()

                cursor3.execute(sql3)
                conn.commit()
                cursor3.close()

                list1.clear()
                list2.clear()
                print(list1)
                print(list2)
        # data2 - data2
        for i in data2:
            for v in data2:
                print(i, v)
                cursor = conn.cursor()
                sql = "select r.dates, r.price x, e.price y from (select dates, price from exechangerate where symbol='" + i + "')  r inner join (select dates, price from exechangerate where symbol='" + v + "') e WHERE r.dates = e.dates order by r.dates asc"

                print(sql)
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    print(row['x'])
                    print(row['y'])
                    list1.append(row['x'])
                    list2.append(row['y'])
                    # print(rows)
                conn.commit()
                cursor.close()

                time.sleep(3)
                correlation = pearsonr(list1, list2)
                print(correlation)
                a, b = correlation
                print('최종')
                print(a)
                a = str(a)
                sql2 = "UPDATE corr SET " + i + "=" + a + " WHERE indicator='" + v + "'"
                print(sql2)
                cursor2 = conn.cursor()

                cursor2.execute(sql2)
                conn.commit()
                cursor2.close()

                list1.clear()
                list2.clear()
                print(list1)
                print(list2)
        conn.close()

        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)
        print("testindi2")

        return Response(serializer.data);

