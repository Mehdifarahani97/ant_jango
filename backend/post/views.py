from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from . import models
from . import serializers

import pymysql
import json
from django.core.serializers.json import DjangoJSONEncoder


class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class QuestionDetail(APIView):
    def get(self, request, format=None):
        conn = pymysql.connect(host='3.34.96.149', user='root', password='1234', db='indicators', charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        print('연결성공')

        cursor = conn.cursor()
        sql = "select * from usdkrw"
        cursor.execute(sql)
        data = json.dumps(cursor.fetchall(), cls=DjangoJSONEncoder)
        # pymysql로 받은 데이터는 tuple이 기본형이다. .connect 메소드에 설정한 cursorclass와 json.dumps의 cls=DjangoJSONEncoder로 data를 JSON 객체로 파싱하면 React에서 데이터를 받을 때 추가 파싱 없이 JSON 객체로 쓸 수 있다.

        print(data)
        print(type(data))

        cursor.close()
        conn.close()

        question = models.Question(data=data)
        serializer = serializers.QuestionSerializer(question)

        return Response(serializer.data)
# Create your views here.
