from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from . import models
from . import serializers
from scipy.stats import pearsonr

import pymysql
import json
from django.core.serializers.json import DjangoJSONEncoder


class DetailPost(APIView):
    def post(self, request, *args, **kwargs):
        data1 = ["bitcoin", "bond10", "bond2", "dolleridx", "goldfor", "wti", "usdkrw"]
        data2 = ["EURUSD", "USDJPY", "USDCNY", "USDGBP"]
        corr = []

        listsymbol = []
        datas = []
        listindi = []

        data = json.loads(request.body.decode('utf-8'))
        print(data)

        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor,read_timeout=80)
        cursor = conn.cursor()
        # data1
        sql = "SELECT price FROM exechangerate where symbol='" + data[1] + "' ORDER BY dates LIMIT  "+ str(data[0])
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            listsymbol.append(row['price'])

        print(listsymbol)

        #data1
        for i in data1:
            cursor2 = conn.cursor()
            sql2 = "select price from " + i + " order by dates limit " + str(data[0])
            cursor2.execute(sql2)
            rows = cursor2.fetchall()
            print(rows)
            for row in rows:
                listindi.append(row['price'])

            correlation = pearsonr(listsymbol, listindi)

            a, b = correlation
            corr.append(a)
            listindi.clear()

        # data2
        for i in data2:
            cursor3 = conn.cursor()
            sql3 = "select dates, price from exechangerate where symbol='" + i + "' order by dates limit " + str(data[0])
            cursor3.execute(sql3)
            rows = cursor3.fetchall()
            for row in rows:
                listindi.append(row['price'])
            correlation = pearsonr(listsymbol, listindi)
            a, b = correlation
            corr.append(a)
            if a > 0.999999999:
                corr.remove(a)
            listindi.clear()

        for i in data1:
            a = ""
            if i == "bitcoin":
                a = "비트코인"
            elif i == "bond10":
                a = "미 10년 채권수익률"
            elif i == "bond2":
                a = "미 2년 채권수익률"
            elif i == "dolleridx":
                a = "달러인덱스"
            elif i == "goldfor":
                a = "국제 금"
            elif i == "wti":
                a = "WTI"
            elif i == "usdkrw":
                a = "원/달러"

            corr.append(a)

        for i in data2:

            a = ""
            if i == "EURUSD":
                a = "달러/유로"
            elif i == "USDJPY":
                a = "엔/달러"
            elif i == "USDCNY":
                a = "위안/달러"
            elif i == "USDGBP":
                a = "파운드/달러"
            corr.append(a)
            if i == data[1]:
                corr.remove(a)

        datas = corr
        print(datas)
        question = models.Question(data=datas)
        serializer = serializers.QuestionSerializer(question)
        return Response(serializer.data);
