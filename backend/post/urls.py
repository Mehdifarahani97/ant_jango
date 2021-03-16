from django.urls import path

from . import views
from . import indicators
from . import indicatorsGoldfor
from . import indicatorWTI
from . import indicatorBond10
from . import indicatorBond2
from . import indicatorDolleridx
from . import indicatorEurusd
from . import indicatorUsdgdp
from . import indicatorUsdcny
from . import indicatorUsdjpy
from . import indicatorBitcoin
from . import indicatorCorr
from . import usdkrwCorr
from . import corrExe
from . import corr1
from . import corr2
from . import moment
from . import rsi

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('<int:pk>/', views.DetailPost.as_view()),
    path('requestUsdkrw/', indicators.usdkrw.as_view()),
    path('requestGoldfor/', indicatorsGoldfor.goldfor.as_view()),
    path('requestWTI/', indicatorWTI.wti.as_view()),
    path('requestBond10/', indicatorBond10.Bond10.as_view()),
    path('requestBond2/', indicatorBond2.Bond2.as_view()),
    path('requestDolleridx/', indicatorDolleridx.Dolleridx.as_view()),
    path('requestEurusd/', indicatorEurusd.Eurusd.as_view()),
    path('requestUsdgdp/', indicatorUsdgdp.Usdgdp.as_view()),
    path('requestUsdcny/', indicatorUsdcny.Usdcny.as_view()),
    path('requestUsdjpy/', indicatorUsdjpy.Usdjpy.as_view()),
    path('requestBitcoin/', indicatorBitcoin.Bitcoin.as_view()),
    path('requestCorr/', indicatorCorr.Corr.as_view()),
    path('requestCorr2', usdkrwCorr.DetailPost.as_view()),
    path('corrExe', corrExe.DetailPost.as_view()),
    path('corr1', corr1.DetailPost.as_view()),
    path('corr2', corr2.DetailPost.as_view()),
    path('moment', moment.DetailPost.as_view()),
    path('rsi', rsi.DetailPost.as_view())
]