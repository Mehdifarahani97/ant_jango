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
        data1 = ["bitcoin", "bond10", "bond2", "dolleridx", "goldfor", "wti"]
        data2 = ["EURUSD", "USDJPY", "USDCNY", "USDGBP"]
        corr = []
        listcorr = []
        listusdkrw = []
        datas = []
        data = json.loads(request.body.decode('utf-8'))
        print("확인",type(data))
        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        sql = "select price from usdkrw order by dates limit " + str(data)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            listusdkrw.append(row['price'])

        cursor.close()
        #data1
        for i in data1:
            cursor2 = conn.cursor()
            sql2 = "select price from " + i + " order by dates limit " + str(data)
            cursor2.execute(sql2)
            rows = cursor2.fetchall()
            for row in rows:
                listcorr.append(row['price'])
            correlation = pearsonr(listusdkrw, listcorr)
            a, b = correlation
            corr.append(a)
            listcorr.clear()
        print(corr)
        cursor2.close()

        # data2
        for i in data2:
            cursor3 = conn.cursor()
            sql3 = "select dates, price from exechangerate where symbol='" + i + "' order by dates limit " + str(data)
            cursor3.execute(sql3)
            rows = cursor3.fetchall()
            for row in rows:
                listcorr.append(row['price'])
            correlation = pearsonr(listusdkrw, listcorr)
            a, b = correlation
            corr.append(a)
            listcorr.clear()

        cursor3.close()
        datas = corr
        print(datas)
        question = models.Question(data=datas)
        serializer = serializers.QuestionSerializer(question)
        return Response(serializer.data);
