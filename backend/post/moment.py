from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from . import models
from . import serializers
from scipy.stats import pearsonr
import datetime
import backtrader as bt
import pymysql
import json
from django.core.serializers.json import DjangoJSONEncoder

listdata = []
listdate = []
listall = []

class Momentum(bt.Strategy):
    params = dict(
        pfast=10,
        pslow=20
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.smaSlow = bt.ind.SimpleMovingAverage(period=self.p.pslow)
        self.smaFast = bt.ind.SimpleMovingAverage(period=self.p.pfast)
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        print(self.datas[0].datetime.date(0).strftime('%Y-%m-%d'))
        listdate.append(self.datas[0].datetime.date(0).strftime('%Y-%m-%d'))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Size: {1:8.2f} Cost: {2:8.2f}, Comm: {3:8.2f}'.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm
                ))
                listdata.append((order.executed.value-10000000)/10000000)
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            else:
                self.log('SELL EXECUTED, {0:8.2f}, Size:{1:8.2f} Cost: {2:8.2f}, Comm: {3:8.2f} '.format(
                    order.executed.price,
                    order.executed.size,
                    order.executed.value,
                    order.executed.comm
                ))
                listdata.append((order.executed.value-10000000)/10000000)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
        self.order = None

    def next(self):
        cash = self.broker.get_cash()
        value = self.broker.get_value()
        size = int(cash / self.data.close[0])
        if self.order:
            return

        if not self.position:
            if self.smaSlow < self.data.close[0]:
                self.order = self.buy(size=size)
        elif self.getposition().size > 0:
            if self.smaSlow > self.data.close[0]:
                self.order = self.sell(size=self.getposition().size)

def run(args=None):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000000)

    data = bt.feeds.YahooFinanceData(dataname='005930.KS',
                                         fromdate=datetime.datetime(2019, 1, 1),
                                         todate=datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    cerebro.addstrategy(Momentum)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print(type(cerebro))

class DetailPost(APIView):
    def post(self, request, *args, **kwargs):

        datas = []

        from datetime import datetime
        data = json.loads(request.body.decode('utf-8'))
        print("처음 확인",data)
        if (data[0]['category'] == '회사명'):
            datan = data[0]['condition'].split('(')[1].replace(")",".KS")
            fd = datetime.strptime(data[1]['condition'].split('(')[1].split('~')[0], '%Y.%m.%d')
            td = datetime.strptime(data[1]['condition'].split('(')[1].split('~')[1].split(')')[0], '%Y.%m.%d')
        else:
            datan = data[1]['condition'].split('(')[1].replace(")", ".KS")
            fd = datetime.strptime(data[0]['condition'].split('(')[1].split('~')[0], '%Y.%m.%d')
            td = datetime.strptime(data[0]['condition'].split('(')[1].split('~')[1].split(')')[0], '%Y.%m.%d')

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(10000000)

        data = bt.feeds.YahooFinanceData(dataname=datan,
                                         fromdate=fd,
                                         todate=td)
        cerebro.adddata(data)
        cerebro.addstrategy(Momentum)
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        print("마지막")

        for i in listdate:
            listall.append(i)

        for i in listdata:
            listall.append(i)
        #print(listdata)
        listdate.clear()
        listdata.clear()
        listfinal = []
        for i in listall:
            listfinal.append(i)
        listall.clear()

        print(listfinal)
        question = models.Question(data=listfinal)
        serializer = serializers.QuestionSerializer(question)


        return Response(serializer.data);